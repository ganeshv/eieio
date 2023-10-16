from AppKit import NSImage
from Cocoa import (NSFont, NSFontAttributeName, NSBaselineOffsetAttributeName)
from Foundation import NSData, NSBundle

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
