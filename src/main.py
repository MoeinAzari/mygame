import sys
if __name__ == "__main__":
    sys.exit(0)

import pygame as pg
from ..drawables import *
from ..os import *
from ..structures import *

cc = ColorConstants
pg.init()

window = Window(Pos(1200,800),Pos(800,600))
window.color = cc.GRAY_SKY,cc.BLACK,cc.GRAY_SKY,cc.GRAY_SKY.lerp(cc.BLACK,0.3)

while not window.event_holder.should_quit:


    window.get_events()
    window.check_events()
    window.render(window.surface)
    window.update()

