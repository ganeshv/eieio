from bmp import SimpleBMP
from PyObjCTools.Conversion import propertyListFromPythonCollection
from AppKit import NSAttributedString, NSImage
from Cocoa import (NSFont, NSFontAttributeName, NSBaselineOffsetAttributeName,
                   NSLeftTextAlignment, NSMutableParagraphStyle, NSParagraphStyleAttributeName)
from Foundation import NSData

# Convert the BMP byte data to an NSImage
def bmp_bytes_to_nsimage(bmp_data):
    data = NSData.dataWithBytes_length_(bmp_data, len(bmp_data))
    ns_image = NSImage.alloc().initWithData_(data)
    return ns_image

def create_bar_icon(cpu_samples):
    # This function should create and return an icon (BMP image bytes) representing the CPU usage bars
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

multiline_font = {
    NSFontAttributeName: NSFont.fontWithName_size_("Menlo", 9.0),
    NSBaselineOffsetAttributeName: -8.0
}
fixed_width_font = {
    NSFontAttributeName: NSFont.fontWithName_size_("Menlo", 14.0)
}