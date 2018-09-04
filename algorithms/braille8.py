class Encoder(object):
    CHARSET = (
        "⠀⠁⠂⠃⠄⠅⠆⠇⡀⡁⡂⡃⡄⡅⡆⡇"
        "⠈⠉⠊⠋⠌⠍⠎⠏⡈⡉⡊⡋⡌⡍⡎⡏"
        "⠐⠑⠒⠓⠔⠕⠖⠗⡐⡑⡒⡓⡔⡕⡖⡗"
        "⠘⠙⠚⠛⠜⠝⠞⠟⡘⡙⡚⡛⡜⡝⡞⡟"
        "⠠⠡⠢⠣⠤⠥⠦⠧⡠⡡⡢⡣⡤⡥⡦⡧"
        "⠨⠩⠪⠫⠬⠭⠮⠯⡨⡩⡪⡫⡬⡭⡮⡯"
        "⠰⠱⠲⠳⠴⠵⠶⠷⡰⡱⡲⡳⡴⡵⡶⡷"
        "⠸⠹⠺⠻⠼⠽⠾⠿⡸⡹⡺⡻⡼⡽⡾⡿"
        "⢀⢁⢂⢃⢄⢅⢆⢇⣀⣁⣂⣃⣄⣅⣆⣇"
        "⢈⢉⢊⢋⢌⢍⢎⢏⣈⣉⣊⣋⣌⣍⣎⣏"
        "⢐⢑⢒⢓⢔⢕⢖⢗⣐⣑⣒⣓⣔⣕⣖⣗"
        "⢘⢙⢚⢛⢜⢝⢞⢟⣘⣙⣚⣛⣜⣝⣞⣟"
        "⢠⢡⢢⢣⢤⢥⢦⢧⣠⣡⣢⣣⣤⣥⣦⣧"
        "⢨⢩⢪⢫⢬⢭⢮⢯⣨⣩⣪⣫⣬⣭⣮⣯"
        "⢰⢱⢲⢳⢴⢵⢶⢷⣰⣱⣲⣳⣴⣵⣶⣷"
        "⢸⢹⢺⢻⢼⢽⢾⢿⣸⣹⣺⣻⣼⣽⣾⣿"
    )

    @classmethod
    def encode(cls, values, size, negative=False):
        data = []

        for y in range(0, (size[1] // 4) * 4, 4):
            line = ''
            for x in range(0, (size[0] // 2) * 2, 2):
                chr_bin = ''.join(map(str, (
                    values[(y + 3) * size[0] + x + 1] // 255,
                    values[(y + 2) * size[0] + x + 1] // 255,
                    values[(y + 1) * size[0] + x + 1] // 255,
                    values[(y + 0) * size[0] + x + 1] // 255,
                    values[(y + 3) * size[0] + x + 0] // 255,
                    values[(y + 2) * size[0] + x + 0] // 255,
                    values[(y + 1) * size[0] + x + 0] // 255,
                    values[(y + 0) * size[0] + x + 0] // 255,
                )))

                index = int(chr_bin, 2)
                if negative:
                    index = 255 - index
                line += cls.CHARSET[index]
            data.append(line)

        for i, l in enumerate(data):
            print(l)




