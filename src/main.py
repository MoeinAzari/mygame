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

# text = TextBox(window.content_rect,"police-thief-cyber-"*10)
text = TextBox(window.content_rect,"you know it's a rough neighborhood when you see a pigeon "
                                   "wearing an angle monitor carries a knife. "
                                   *5)

text.event_holder = window.event_holder
text.color = cc.HOT_RED,cc.BLACK,cc.GRAY_SKY,cc.HOT_RED.lerp(cc.BLACK,0.3)
text.update()
step = 1
stuff = 1
while not window.event_holder.should_quit:

    window.get_events()
    text.get_events()
    window.check_events()
    text.check_events()
    window.render(window.surface)

    if K_SPACE in window.event_holder.keyboard_pressed_keys:
        text.create_object(Pos(text.content_rect.width,100))
        text.update()

    if K_LCTRL in window.event_holder.keyboard_held_keys:
        if K_1 in window.event_holder.keyboard_pressed_keys:
            stuff += 1
        if K_2 in window.event_holder.keyboard_pressed_keys:
            stuff -= 1

        last_center = text.margined_rect.center

        text.margin = [stuff] * 4
        text.border = [stuff] * 4
        text.padding = [stuff] * 4

        text.update()
        text.margined_rect.center = last_center



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

