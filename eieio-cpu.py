import rumps
import psutil
import os
from collections import deque

from AppKit import NSAttributedString, NSImage
from PyObjCTools.Conversion import propertyListFromPythonCollection
from Cocoa import NSFont, NSFontAttributeName
from Foundation import NSData

from bmp import SimpleBMP

class DynamicMenubarApp(object):
    def __init__(self):
        font = NSFont.fontWithName_size_("Menlo", 14.0)
        self.attributes = propertyListFromPythonCollection({NSFontAttributeName: font}, conversionHelper=lambda x: x)

        self.cpu_samples = deque(maxlen=25)  # keep the last 25 samples
        self.nprocs = 5
        self.app = rumps.App("Menubar App")
        self.set_up_menu()
        self.update_menu()

    def set_up_menu(self):
        self.cpu_item = rumps.MenuItem(title="CPU usage:", callback=self.do_nothing)
        self.load_avg_item = rumps.MenuItem(title="Load Avg:", callback=self.do_nothing)
        self.procs = [rumps.MenuItem(" ") for x in range(self.nprocs)]
        self.open_activity_monitor = rumps.MenuItem("Open Activity Monitor", callback=self.open_activity_monitor_action)
        proctitle = rumps.MenuItem("PID    COMMAND      %CPU")
        string = NSAttributedString.alloc().initWithString_attributes_(proctitle.title, self.attributes)
        proctitle._menuitem.setAttributedTitle_(string)
        self.app.menu = [self.cpu_item, self.load_avg_item, rumps.separator, proctitle] + self.procs + [rumps.separator, self.open_activity_monitor]
        self.app.title = "asn"
    
    def update_menu(self, sender=None):
        # CPU usage
        ct = psutil.cpu_times_percent()
        user = ct.user + ct.nice
        sys = ct.system
        idle = ct.idle
        cpu_percent = user + sys
        self.cpu_samples.append(cpu_percent)
        self.cpu_item.title = f"CPU usage: {user:.2f}% user, {sys:.2f}% sys, {idle:.2f}% idle"

        # Load Average
        load_avg = os.getloadavg()
        self.load_avg_item.title = f"Load Avg: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"

        # Top 5 CPU hogs
        all_processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent']))
        valid_processes = [p for p in all_processes if p.info['cpu_percent'] is not None]
        processes = sorted(valid_processes, key=lambda p: p.info['cpu_percent'], reverse=True)[:self.nprocs]
        
        for i in range(self.nprocs):
            process = processes[i]
            procinfo = f"{process.info['pid']:<6} {process.info['name'][:12]:<12} {process.info['cpu_percent']:.2f}%"
            string = NSAttributedString.alloc().initWithString_attributes_(procinfo, self.attributes)
            self.procs[i]._menuitem.setAttributedTitle_(string)

        # Update the icon
        bmp = self.create_cpu_bar_icon(self.cpu_samples)
        self.app._icon_nsimage = bmp_bytes_to_nsimage(bmp)
        try:
            self.app._nsapp.setStatusBarIcon()
        except AttributeError:
            pass

    def create_cpu_bar_icon(self, cpu_samples):
        # This function should create and return an icon (image path) representing the CPU usage bars
        width, height = 25, 16
        line_height = height - 3
        bgcol = (0, 0, 0, 0)
        fgcol = (22, 22, 22, 255)
        img = SimpleBMP(width, height)
        img.fill_rect(0, 0, width - 1, height - 1, bgcol)
        img.fill_rect(0, 0, width - 1, 2, fgcol)
        img.draw_hline(0, width - 1, height - 1, fgcol)
        startx = width - len(cpu_samples)
        starty = 2
        for i, cpu in enumerate(cpu_samples):
            cpu_height = int(cpu * line_height / 100)
            img.draw_vline(startx + i, starty, starty + cpu_height, fgcol)
        return img.export()

    def open_activity_monitor_action(self, sender):
        os.system('open -a "Activity Monitor"')

    def do_nothing(self, sender):
        pass


    def run(self):
        rumps.Timer(self.update_menu, 5).start()  # Update the menu every 5 seconds
        self.app.run()

# Convert the BMP byte data to an NSImage
def bmp_bytes_to_nsimage(bmp_data):
    data = NSData.dataWithBytes_length_(bmp_data, len(bmp_data))
    ns_image = NSImage.alloc().initWithData_(data)
    return ns_image

if __name__ == '__main__':
    app = DynamicMenubarApp()
    app.run()
