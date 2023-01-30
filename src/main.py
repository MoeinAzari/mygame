import sys
if __name__ == "__main__":
    sys.exit(0)

import pygame as pg
from pygame.locals import *

from ..drawables import *
from ..os import *
from ..structures import *

cc = ColorConstants
pg.init()

window = Window(Pos(1200,800),Pos(800,600))
window.color = cc.GRAY_SKY,cc.BLACK,cc.GRAY_SKY,cc.GRAY_SKY.lerp(cc.BLACK,0.3)

text = TextHolder(window.content_rect,"police-thief-cyber-"*10)
# text.margin = [10] * 4
# text.border = [5] * 4
# text.padding = [10] * 4
text.color = cc.HOT_RED,cc.BLACK,cc.GRAY_SKY,cc.WHITE.lerp(cc.BLACK,0.3)
text.update()
step = 1
while not window.event_holder.should_quit:

    window.get_events()
    window.check_events()
    window.render(window.surface)
    if window.event_holder.window_size_changed:
        text.margined_rect = window.content_rect
    else:
        last_center = text.margined_rect.center
        if K_LSHIFT in window.event_holder.keyboard_held_keys:
            if K_UP in window.event_holder.keyboard_held_keys:
                text.height += step
            if K_DOWN in window.event_holder.keyboard_held_keys:
                text.height -= step

            if K_RIGHT in window.event_holder.keyboard_held_keys:
                text.width += step
            if K_LEFT in window.event_holder.keyboard_held_keys:
                text.width -= step
            text.update()
            text.margined_rect.center = last_center

        else:
            if K_UP in window.event_holder.keyboard_held_keys:
                text.y -= step
            if K_DOWN in window.event_holder.keyboard_held_keys:
                text.y += step

            if K_RIGHT in window.event_holder.keyboard_held_keys:
                text.x += step
            if K_LEFT in window.event_holder.keyboard_held_keys:
                text.x -= step

    text.render(window.surface)
    window.update()

