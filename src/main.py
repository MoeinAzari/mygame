import pygame as pg
from pygame.locals import *

from random import randint as rand

from mygame.structures.Pos import Pos
import mygame.os.EventHolder as eventHolder
from mygame.structures.Rect import Rect
from mygame.drawables.Object import Object
from mygame.drawables.Container import Container
from mygame.drawables.ScrollView import ScrollView
from mygame.globals import functions
from mython.mylist import mylist
from mygame.structures.Color import Color, ColorConstants
from mygame.os.Window import Window

colors = ColorConstants

pg.init()

content_size = Pos(800,600)
window_size = Pos(1100,800)
window = Window(window_size, content_size)

scroll_view = ScrollView(Rect(0, 0, int(content_size.x), int(content_size.y)))
scroll_view.color = [i.lerp(Color(255,255,0),0.1) for i in
    [colors.DEAD_BLUE,colors.HOT_RED,colors.DEAD_BLUE,colors.GRAY_SKY]
    ]

scroll_view.margin = 10, 10, 10, 10
scroll_view.border = 5, 5, 5, 5
scroll_view.padding = 20, 20, 20, 20
scroll_view.update_surface()
scroll_view.event_holder = window.event_holder

def print_objects():
    print("Container {")
    for i in scroll_view.object_list:
        print("\t",i.margined_rect)
    print("}")

just_started = True
clock = pg.time.Clock()
fps = 90
adjust_pos = Pos(0,0)
adjust_step = 4


while not window.event_holder.should_quit :
    window.get_events()
    scroll_view.get_events()
    if window.event_holder.window_size_changed or just_started:
        scroll_view.margined_rect = window.content_rect.copy()
        scroll_view.sync_objects()


    if K_a in window.event_holder.keyboard_held_keys:
        scroll_view.create_object(Pos(rand(50,50),rand(50,50)))
    if K_s in window.event_holder.keyboard_pressed_keys:
        cube = rand(40,40)
        scroll_view.create_object(Pos(cube,cube))
    if K_d in window.event_holder.keyboard_held_keys or K_c in\
            window.event_holder.keyboard_pressed_keys:
        scroll_view.resize_objects(0.95)
    if K_f in window.event_holder.keyboard_held_keys or K_v in\
            window.event_holder.keyboard_pressed_keys:
        scroll_view.resize_objects(1.05)
    if K_q in window.event_holder.keyboard_pressed_keys:
        scroll_view.object_list.clear()
        scroll_view.update()

    # if K_UP in window.keyboard_held_keys: adjust_pos.y -= adjust_step
    # if K_DOWN in window.keyboard_held_keys : adjust_pos.y += adjust_step
    # if K_RIGHT in window.keyboard_held_keys : adjust_pos.x += adjust_step
    # if K_LEFT in window.keyboard_held_keys : adjust_pos.x -= adjust_step
    should_update = False
    should_recenter = False

    last_rect = scroll_view.margined_rect.copy()
    if K_LCTRL not in window.event_holder.keyboard_held_keys:
        if K_UP in window.event_holder.keyboard_held_keys:
            scroll_view.y -= adjust_step
            # should_update = True

        if K_DOWN in window.event_holder.keyboard_held_keys :
            scroll_view.y += adjust_step
            # should_update = True

        if K_RIGHT in window.event_holder.keyboard_held_keys :
            scroll_view.x += adjust_step
            # should_update = True

        if K_LEFT in window.event_holder.keyboard_held_keys :
            scroll_view.x -= adjust_step
            # should_update = True

    if K_LSHIFT in window.event_holder.keyboard_held_keys:
        if K_UP in window.event_holder.keyboard_held_keys:
            scroll_view.height += adjust_step / 2
            should_update = should_recenter = True
        if K_DOWN in window.event_holder.keyboard_held_keys:
            scroll_view.height -= adjust_step
            should_update = should_recenter = True

        if K_RIGHT in window.event_holder.keyboard_held_keys:
            scroll_view.width += adjust_step
            should_update = should_recenter = True

        if K_LEFT in window.event_holder.keyboard_held_keys:
            scroll_view.width -= adjust_step
            should_update = should_recenter = True

    if should_update:
        if should_recenter: scroll_view.margined_rect.center = last_rect.center

        scroll_view.update()

    window.check_events()
    scroll_view.check_events()

    window.render_screen()
    scroll_view.render(window.surface,adjust_pos)

    window.update()
    clock.tick(fps)

    current_fps = clock.get_fps()
    if current_fps < 60:
        print('low fps warning : ',clock.get_fps(),
            'total objects : ',len(scroll_view.object_list))

    just_started = False



