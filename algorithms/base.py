class BrailleEncoder(object):
    WIDTH = 2
    HEIGHT = None
    CHARSET = ''
    DOT_OFFSETS = ()

    @classmethod
    def encode(cls, values, size, negative=False):
        data = []
        max_y = (size[1] // cls.HEIGHT) * cls.HEIGHT
        max_x = (size[0] // cls.WIDTH) * cls.WIDTH

        for y in range(0, max_y, cls.HEIGHT):
            line = ''
            for x in range(0, max_x, cls.WIDTH):
                chr_bin = ''.join(
                    str(values[(y + y_offset) * size[0] + x + x_offset] // 255)
                    for y_offset, x_offset in cls.DOT_OFFSETS
                )

                index = int(chr_bin, 2)
                if negative:
                    index = len(cls.CHARSET) - 1 - index
                line += cls.CHARSET[index]
            data.append(line)

        return '\n'.join(data)
