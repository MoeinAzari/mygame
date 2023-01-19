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
        self.scroll_step = 0.01
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

        self.objects_adjust_pos.y = -self.scroll_scale * self.scroll_diff
        if self.is_scrollable:
            if K_RCTRL in self.event_holder.keyboard_held_keys :
                self.scroll_scale -= self.scroll_step
                if self.scroll_scale <= 0 :
                    self.scroll_scale = 0
                should_scroll = True
            elif K_RSHIFT in self.event_holder.keyboard_held_keys :
                self.scroll_scale += self.scroll_step
                if self.scroll_scale > 1 :
                    self.scroll_scale = 1
                should_scroll = True

            self.objects_adjust_pos.y = -self.scroll_scale * self.scroll_diff
            if should_scroll:
                self.was_changed = True




    def update( self  ):
        super(ScrollView, self).update()



    def check_events( self ):
        if self.scroll_scale < 0 or self.scroll_scale > 1:
            print(self.scroll_scale,'WARNING!')
        super().check_events()

    def render( self,surface:pg.surface.Surface,pos_adjust:Pos = None ):
        super(ScrollView, self).render(surface)

