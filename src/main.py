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

textHolder = TextHolder("police-thief-cyber-"*10
                            ,window.content_rect.width)

while not window.event_holder.should_quit:


    window.get_events()
    window.check_events()
    window.render(window.surface)

    window.surface.blit(textHolder.surface,window.content_rect.pos)

    window.update()

