import rumps
import psutil
import os
from collections import deque

from utils import App, MenuItem, fixed_width_font, disable_dock_icon
from bmp import SimpleBMP

class CPUMenubarApp(App):
    def __init__(self):
        super(CPUMenubarApp, self).__init__("CPU Monitor")
        self.cpu_samples = deque(maxlen=25)  # keep the last 25 samples
        self.nprocs = 5
        self.set_up_menu()
        self.update_menu()

    def set_up_menu(self):
        self.cpu_item = MenuItem(title="CPU usage:", callback=self.do_nothing)
        self.load_avg_item = MenuItem(title="Load Avg:", callback=self.do_nothing)
        self.procs = [MenuItem(" ") for x in range(self.nprocs)]
        self.open_activity_monitor = MenuItem("Open Activity Monitor", callback=self.open_activity_monitor_action)
        proctitle = MenuItem("PID    COMMAND      %CPU")
        proctitle.set_attr_title(proctitle.title, fixed_width_font)
        self.menu = [self.cpu_item, self.load_avg_item, rumps.separator, proctitle] + self.procs + [rumps.separator, self.open_activity_monitor]
    
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
            self.procs[i].set_attr_title(procinfo, fixed_width_font)
            
        # Update the icon
        bmp = self.create_bar_icon(self.cpu_samples)
        self.set_icon(bmp)

    def open_activity_monitor_action(self, sender):
        os.system('open -a "Activity Monitor"')

    def do_nothing(self, sender):
        pass

    @staticmethod
    def create_bar_icon(cpu_samples):
        # This function should create and return an icon (BMP image bytes) representing the CPU usage bars
        width, height = 25, 16
        line_height = height - 2
        bgcol = (0, 0, 0, 0)
        bordercol = (22, 22, 22, 255)
        fgcol = (22, 22, 22, 128)
        img = SimpleBMP(width, height)
        img.fill_rect(0, 0, width - 1, height - 1, bgcol)
        img.draw_hline(0, width - 1, 0, bordercol)
        img.draw_hline(0, width - 1, height - 1, bordercol)
        startx = width - len(cpu_samples)
        starty = 1
        for i, cpu in enumerate(cpu_samples):
            cpu_height = int(cpu * line_height / 100)
            img.draw_vline(startx + i, starty, starty + cpu_height, fgcol)
        return img.export()

def main():
    disable_dock_icon()
    app = CPUMenubarApp()
    rumps.Timer(app.update_menu, 5).start()  # Update the menu every 5 seconds
    app.run()
    

if __name__ == '__main__':
    main()