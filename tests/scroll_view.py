import pygame as pg
from pygame.locals import *
from structures import *
from drawables import *
from my_os import *

print(Window)

pg.init()
window = Window(Pos(1200,800),Pos(800,600))

scroll_view = ScrollView(Rect(0,0,window.content_rect.width,window.content_rect.height))
scroll_view.event_holder = window.event_holder
scroll_view.margined_rect.center = window.margined_rect.center

scroll_view.padding = 1,1,1,1
scroll_view.content_color = ColorConstants.DEAD_YELLOW

step_list = [1,2,5]
step_index = 0
step = 2

def recenter_scroll_view_by_window():
    scroll_view.margined_rect.center = window.margined_rect.center

def recenter_scroll_view(pos):
    scroll_view.margined_rect.center = pos

recenter_scroll_view_by_window()

def get_events():
    global step_index,step

    if scroll_view.event_holder.window_size_changed:
        recenter_scroll_view_by_window()

    held_keys = scroll_view.event_holder.keyboard_held_keys
    pressed_keys = scroll_view.event_holder.keyboard_pressed_keys

    weight = lambda: -1 if K_LSHIFT in held_keys else 1

    report = lambda: print(scroll_view.margined_rect) if K_RETURN in pressed_keys else None

    create_object = lambda: scroll_view.create_object(Pos(100,100)) \
                        if K_a in pressed_keys else None

    toggle = lambda : 1 if K_1 in pressed_keys else 0

    if toggle():
        step_index += 1
        if step_index > step_list.__len__() - 1:
            step_index = 0

        step = step_list[step_index]



    report()
    create_object()




    if K_UP in held_keys:
        if K_DOWN in held_keys:
            last_center = scroll_view.margined_rect.center
            scroll_view.height += step * weight()
            recenter_scroll_view(last_center)


        else:
            scroll_view.y -= step

    elif K_DOWN in held_keys:
        scroll_view.y += step

    if K_RIGHT in held_keys:
        if K_LEFT in held_keys :
            last_center = scroll_view.margined_rect.center
            scroll_view.width += step * weight()
            recenter_scroll_view(last_center)

        else :
            scroll_view.x += step

    elif K_LEFT in held_keys:
        scroll_view.x -= step

    if scroll_view.width > window.width:
        scroll_view.width = window.width

    if scroll_view.height > window.height :
        scroll_view.height = window.height

    if scroll_view.x < 0:
        scroll_view.x = 0

    if scroll_view.y < 0:
        scroll_view.y = 0

    if scroll_view.x > window.width - scroll_view.width:
        scroll_view.x = window.width - scroll_view.width

    if scroll_view.y > window.height - scroll_view.height:
        scroll_view.y = window.height - scroll_view.height


while not window.event_holder.should_quit:
    window.get_events()
    scroll_view.get_events()
    get_events()

    window.check_events()
    scroll_view.check_events()

    window.render(window.surface)
    scroll_view.render(window.surface)

    window.update()

