import time

import pygame as pg
from pygame.locals import *

from typing import Optional

from .Object import Object
from .Sprite import Sprite
from .Container import Container
from ..os.EventHolder import EventHolder,EventConstants
from ..structures.Rect import Rect
from ..structures.Pos import Pos
from ..structures.Color import Color,ColorConstants

class ScrollView(Container):
    def __init__(self,rect:Rect):
        self.scroll_scale = 0
        self.scroll_step = 0.004
        self.wheel_timer_interval_initial = 0.3
        self.wheel_timer_interval = self.wheel_timer_interval_initial
        self.wheel_timer_interval_step = self.wheel_timer_interval * 0.1

        self.scrolling_triggered = False
        self.wheel_timer_last_time = time.time()
        super(ScrollView, self).__init__(rect)

    @property
    def is_scrollable( self ):
        return self.all_lines_height > self.content_rect.height

    @property
    def scroll_diff( self ) -> Optional[float]:
        if self.is_scrollable:
            return self.all_lines_height - self.content_rect.height

        self.scroll_scale = 0
        return 0


    def get_events( self ):
        super().get_events()

        should_scroll = False
        if self.content_rect.collidepoint(self.event_holder.mouse_pos):
            if self.event_holder.mouse_wheel_triggered or self.scrolling_triggered:
                if self.event_holder.mouse_wheel_triggered:
                    self.scrolling_triggered = True
                    self.wheel_timer_last_time = time.time()
                    if self.scrolling_triggered:
                        self.wheel_timer_interval += self.wheel_timer_interval_step
                else:
                    if self.wheel_timer_last_time + self.wheel_timer_interval < time.time():
                        self.scrolling_triggered = False
                        self.wheel_timer_interval = self.wheel_timer_interval_initial

                if self.event_holder.mouse_wheel_rel < 0 :
                    self.scroll_scale -= self.scroll_step
                    if self.scroll_scale <= 0 :
                        self.scroll_scale = 0
                        self.event_holder.mouse_wheel_triggered = False
                    should_scroll = True
                elif self.event_holder.mouse_wheel_rel > 0 :
                    self.scroll_scale += self.scroll_step
                    if self.scroll_scale > 1 :
                        self.scroll_scale = 1
                        self.event_holder.mouse_wheel_triggered = False

                    should_scroll = True

                self.objects_adjust_pos.y = -self.scroll_scale * self.scroll_diff
                if should_scroll:
                    self.was_changed = True




    def update( self  ):
        super(ScrollView, self).sync_objects()
        self.objects_adjust_pos.y = -self.scroll_scale * self.scroll_diff
        super(ScrollView, self).update_surface()



    def check_events( self ):
        if self.scroll_scale < 0 or self.scroll_scale > 1:
            print(self.scroll_scale,'WARNING!')
        super().check_events()

    def render( self,surface:pg.surface.Surface,pos_adjust:Pos = None ):
        super(ScrollView, self).render(surface)

