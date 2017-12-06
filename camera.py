class Camera():
    def __init__(self,display,x,y):
        self.cam_w = display.get_width()
        self.cam_h = display.get_height()
        self.x = x
        self.y = y
    def set_pos(self, x, y):
        self.x = x
        self.y = y
