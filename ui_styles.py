class Font:
    def __init__(self, family):
        if family == 0:
            self.light = "Open Sans Light"
            self.medium = "Open Sans Medium"
            self.reg = "Open Sans Regular"
            self.semibold = "Open Sans SemiBold"
            self.bold = "Open Sans Bold"
            self.extrabold = "Open Sans ExtraBold"


class Colour:
    def __init__(self, scheme):
        if scheme == 0:
            self.btn = "#DCDDDE"
            self.btn_click = "#B9BBBE"
            self.txt_title = "#000000"
            self.txt_subtitle = "#060607"
            self.txt_body = "#2E3338"
            self.txt_peripheral = "#616A75"
            self.txt_inactive = "#C7CCD1"
            self.bg_low = "#FFFFFF"
            self.bg_mid = "#F2F3F5"
            self.bg_high = "#E3E5E8"

        elif scheme == 1:
            self.btn = "#4F5660"
            self.btn_click = "#2E3338"
            self.txt_title = "#FFFFFF"
            self.txt_subtitle = "#F8F8F9"
            self.txt_body = "#DCDDDE"
            self.txt_peripheral = "#8E9297"
            self.txt_inactive = "#4F545C"
            self.bg_low = "#36393F"
            self.bg_mid = "#2F3136"
            self.bg_high = "#202225"


colour = Colour(1)
# 0 = Light Mode
# 1 = Dark Mode

font = Font(0)
# 0 = Open Sans
