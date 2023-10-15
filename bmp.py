class SimpleBMP:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[(255, 255, 255, 255) for y in range(height)] for x in range(width)]

    def set_pixel(self, x, y, color):
        """Set the color of a specific pixel."""
        self.pixels[x][y] = color

    def draw_hline(self, x1, x2, y, color):
        """Draw a horizontal line."""
        for x in range(x1, x2 + 1):
            self.set_pixel(x, y, color)

    def draw_vline(self, x, y1, y2, color):
        """Draw a vertical line."""
        for y in range(y1, y2 + 1):
            self.set_pixel(x, y, color)

    def draw_rect(self, x1, y1, x2, y2, color):
        """Draw a rectangle outline."""
        self.draw_hline(x1, x2, y1, color)
        self.draw_hline(x1, x2, y2, color)
        self.draw_vline(x1, y1, y2, color)
        self.draw_vline(x2, y1, y2, color)

    def fill_rect(self, x1, y1, x2, y2, color):
        """Draw a filled rectangle."""
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.set_pixel(x, y, color)

    def export(self):
        """Export the BMP data as bytes."""
        data_size = self.width * self.height * 4
        header_size = 138
        total_size = data_size + header_size

        bmp_bytes = bytearray(total_size)

        # BMP Header
        bmp_bytes[0:2] = b'BM'                         # Signature
        bmp_bytes[2:6] = (total_size).to_bytes(4, 'little')  # File size
        bmp_bytes[10:14] = b'\x8A\x00\x00\x00'          # Offset to data (image pixel data)

        # BITMAPV5HEADER
        bmp_bytes[14:18] = b'\x7C\x00\x00\x00'          # Header size (124 bytes for BITMAPV5HEADER)
        bmp_bytes[18:22] = self.width.to_bytes(4, 'little')  # Image width
        bmp_bytes[22:26] = self.height.to_bytes(4, 'little') # Image height
        bmp_bytes[26:28] = b'\x01\x00'                  # Planes (always 1)
        bmp_bytes[28:30] = b'\x20\x00'                  # Bits per pixel (32 for RGBA)
        bmp_bytes[30:34] = b'\x03\x00\x00\x00'          # Compression (BI_BITFIELDS, no compression with mask values provided)
        bmp_bytes[34:38] = (data_size).to_bytes(4, 'little')  # Image data size
        bmp_bytes[38:42] = b'\x13\x0B\x00\x00'          # Horizontal resolution (pixels per meter, but can be arbitrary)
        bmp_bytes[42:46] = b'\x13\x0B\x00\x00'          # Vertical resolution (pixels per meter, but can be arbitrary)
        bmp_bytes[54:58] = b'\x00\x00\xFF\x00'          # Blue channel bitmask
        bmp_bytes[58:62] = b'\x00\xFF\x00\x00'          # Green channel bitmask
        bmp_bytes[62:66] = b'\xFF\x00\x00\x00'          # Red channel bitmask
        bmp_bytes[66:70] = b'\x00\x00\x00\xFF'          # Alpha channel bitmask
        bmp_bytes[70:74] = b'\x42\x47\x52\x73'          # Color space (LCS_sRGB)

        # Explicitly zero out the remainder of the header
        bmp_bytes[74:138] = b'\x00' * (138 - 74)

        # Pixel data (bottom-to-top)
        offset = header_size
        for y in range(self.height):
            for x in range(self.width):
                r, g, b, a = self.pixels[x][y]
                bmp_bytes[offset:offset + 4] = bytes([b, g, r, a])
                offset += 4

        return bmp_bytes

    def save(self, filename):
        """Save the BMP data to a file."""
        with open(filename, 'wb') as f:
            f.write(self.export())

if __name__ == "__main__":
    # Example usage:
    bmp = SimpleBMP(128, 128)
    bmp.draw_rect(10, 10, 120, 120, (255, 0, 0, 255))
    bmp.fill_rect(20, 20, 100, 100, (0, 255, 0, 128))
    bmp.save("output.bmp")
