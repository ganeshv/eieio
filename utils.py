import rumps

from AppKit import NSImage, NSAttributedString
from Cocoa import (NSFont, NSFontAttributeName, NSBaselineOffsetAttributeName)
from Foundation import NSData, NSBundle

# Subclass rumps.App to add some utility methods
class App(rumps.App):
    def set_icon(self, bmp):
        # Update the icon from a byte array containing a BMP
        self._icon_nsimage = bmp_bytes_to_nsimage(bmp)
        self._icon_nsimage.setTemplate_(True)
        try:
            self._nsapp.setStatusBarIcon()
        except AttributeError:
            pass
    
    def set_attr_title(self, title, attributes):
        # Update the menubar title with an attributed string
        string = NSAttributedString.alloc().initWithString_attributes_(title, attributes)
        self._nsapp.nsstatusitem.setAttributedTitle_(string)

class MenuItem(rumps.MenuItem):
    def set_attr_title(self, title, attributes):
        # Update the menu item title with an attributed string
        string = NSAttributedString.alloc().initWithString_attributes_(title, attributes)
        self._menuitem.setAttributedTitle_(string)

# Convert the BMP byte data to an NSImage
def bmp_bytes_to_nsimage(bmp_data):
    data = NSData.dataWithBytes_length_(bmp_data, len(bmp_data))
    ns_image = NSImage.alloc().initWithData_(data)
    return ns_image

multiline_font = {
    NSFontAttributeName: NSFont.fontWithName_size_("Menlo", 9.0),
    NSBaselineOffsetAttributeName: -8.0
}
fixed_width_font = {
    NSFontAttributeName: NSFont.fontWithName_size_("Menlo", 14.0)
}

def disable_dock_icon():
    bundle = NSBundle.mainBundle()
    info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
    info['LSUIElement'] = '1'
