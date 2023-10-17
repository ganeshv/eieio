import rumps
import psutil
from collections import deque
from AppKit import NSAttributedString

from utils import bmp_bytes_to_nsimage, fixed_width_font, multiline_font, disable_dock_icon
from bmp import SimpleBMP

class NetworkMenubarApp(rumps.App):
    def __init__(self):
        super(NetworkMenubarApp, self).__init__("Network Monitor")
        self.samples = {}  # Stores the last 25 byte counts for each interface
        self.speeds = {}  # Stores the computed speeds for each interface
        self.selected_interface = "en0"
        self.set_up_menu()
        

    def add_interface(self, interface):
        item = rumps.MenuItem(title=f"{interface}: ", callback=self.select_interface)
        item.state = 0
        self.interface_items[interface] = item
        self.samples[interface] = deque(maxlen=25)
        self.speeds[interface] = deque(maxlen=25)

    def set_up_menu(self):
        self.interface_items = {}
        net_io_counters = psutil.net_io_counters(pernic=True)
        # We want to only add interfaces where there has been some traffic, to avoid cluttering the menu
        # en0 is always added, active or not.
        for interface in net_io_counters.keys():
            net_io = net_io_counters.get(interface, None)
            if interface == "en0" or (net_io and (net_io.bytes_sent > 0 or net_io.bytes_recv > 0)):
                self.add_interface(interface)

        self.menu = list(self.interface_items.values()) + [rumps.separator]
        self.select_interface(self.interface_items["en0"])

    def select_interface(self, sender):
        self.selected_interface = sender.title.split(":")[0]
        
        # Update the state of menu items to show the tick
        for interface, item in self.interface_items.items():
            item.state = 1 if interface == self.selected_interface else 0
        
        self.update_menu()

    def update_menu(self, sender=None):
        net_io_counters = psutil.net_io_counters(pernic=True)
        for interface, net_io in net_io_counters.items():
            item = self.interface_items.get(interface, None)
            if item is None and (net_io.bytes_sent > 0 or net_io.bytes_recv > 0):
                self.add_interface(interface)
                item = self.interface_items[interface]
                self.menu.insert_before(rumps.separator, item)
            
            if item is not None:
                # Store the byte counts in the samples deque
                self.samples[interface].append((net_io.bytes_sent, net_io.bytes_recv))
                
                # If we have at least two samples, compute the speed and store it
                if len(self.samples[interface]) > 1:
                    prev_sent, prev_recv = self.samples[interface][-2]
                    curr_sent, curr_recv = self.samples[interface][-1]
                    upload_speed = (curr_sent - prev_sent) / 5
                    download_speed = (curr_recv - prev_recv) / 5
                    self.speeds[interface].append((upload_speed, download_speed))
                    
                    human_upload = self.human_readable_speed(upload_speed)
                    human_download = self.human_readable_speed(download_speed)
                    title = f"{interface+':':<8} {human_download}⬇ {human_upload}⬆"
                    string = NSAttributedString.alloc().initWithString_attributes_(title, fixed_width_font)
                    item._menuitem.setAttributedTitle_(string)

                    # Update the menubar title for the selected interface
                    if interface == self.selected_interface:
                        speeds = f"{human_download}⬇\n{human_upload}⬆"
                        string = NSAttributedString.alloc().initWithString_attributes_(speeds, multiline_font)
                        self._nsapp.nsstatusitem.setAttributedTitle_(string)
                        # Update the icon
                        bmp = self.create_bar_icon(self.speeds[interface])
                        self._icon_nsimage = bmp_bytes_to_nsimage(bmp)
                        self._icon_nsimage.setTemplate_(True)
                        try:
                            self._nsapp.setStatusBarIcon()
                        except AttributeError:
                            pass

    @staticmethod
    def human_readable_speed(bytes_per_second):
        if bytes_per_second < 1024:
            return f"{bytes_per_second:3.0f}B"
        elif bytes_per_second < 1024**2:
            return f"{bytes_per_second / 1024:3.0f}K"
        elif bytes_per_second < 1024**3:
            return f"{bytes_per_second / 1024**2:3.0f}M"
        else:
            return f"{bytes_per_second / 1024**3:3.0f}G"

    @staticmethod
    def compute_bar(speed):
        thresholds = [ (1024, 7), (512, 6), (256, 5), (128, 4),
            (64, 3), (32, 2), (16, 1)
        ]

        for threshold in thresholds:
            if speed / 1024 >= threshold[0]:
                return threshold[1]
        return 0

    @staticmethod
    def create_bar_icon(samples):
        # This function should create and return an icon (BMP image bytes)
        # representing network upload/download bandwidth usage
        width, height = 25, 16
        bgcol = (0, 0, 0, 0)
        fgcol_down = (22, 22, 22, 255)
        fgcol_up = (22, 22, 22, 128)
        img = SimpleBMP(width, height)
        img.fill_rect(0, 0, width - 1, height - 1, bgcol)
        img.draw_hline(0, width - 1, height - 1, fgcol_down)
        img.draw_hline(0, width - 1, 0, fgcol_down)

        startx = width - len(samples)
        for i, speed in enumerate(samples):
            bar = NetworkMenubarApp.compute_bar(speed[0])
            if bar > 0:
                img.draw_vline(startx + i, 1, bar, fgcol_up)
            bar = NetworkMenubarApp.compute_bar(speed[1])
            if bar > 0:
                img.draw_vline(startx + i, height - 1 - bar, height - 2, fgcol_down)

        return img.export()

def main_network():
    disable_dock_icon()
    app = NetworkMenubarApp()
    rumps.Timer(app.update_menu, 5).start()  # Update the menu every 5 seconds
    app.run()

if __name__ == '__main__':
    main_network()

