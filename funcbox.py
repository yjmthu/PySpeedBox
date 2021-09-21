from form import Form

class _PAPER_TYPE:
    Latest, Hot, Nature, Anime, Simple, Random, Bing, Wallpapers, Native, Advance = range(10)

class VARBOX:
    ScreenWidth = 2560
    ScreenHeight = 1600
    PAPER_TYPE = _PAPER_TYPE()

    def __init__(self, w, h) -> None:
        self.ScreenWidth = w
        self.ScreenHeight = h
        self.AppId = str()
        self.PassWord = str()
    
    def creatForm(self):
        self.form = Form(self)
        self.form.show()
    
    def initTrans():
        pass
