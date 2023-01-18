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


    def get_events( self,pos_adjust:Pos=None ):
        if pos_adjust is None: pos_adjust = Pos(0,0)

        scroll_pos = Pos(0, self.scroll_scale * self.scroll_diff)

        super().get_events(scroll_pos.transform(mult_xy=-1))

        should_scroll = False
        if self.is_scrollable:

            if K_LCTRL in self.event_holder.keyboard_held_keys:
                if K_UP in self.event_holder.keyboard_held_keys:
                    self.scroll_scale -= self.scroll_step
                    if self.scroll_scale <= 0:
                        self.scroll_scale = 0
                    should_scroll = True
                elif K_DOWN in self.event_holder.keyboard_held_keys:
                    self.scroll_scale += self.scroll_step
                    if self.scroll_scale > 1:
                        self.scroll_scale = 1
                    should_scroll = True

            if should_scroll:
                self.update(scroll_pos.transform(mult_xy=-1))

    def update( self , pos_adjust:Pos = None ):
        super(ScrollView, self).update(pos_adjust)

    def update_surface( self , pos_adjust:Pos = None):
        super(ScrollView, self).update_surface(Pos(0, -self.scroll_scale * self.scroll_diff))

    def check_events( self ):
        if self.scroll_scale < 0 or self.scroll_scale > 1:
            print(self.scroll_scale,'WARNING!')
        super().check_events()

    def render( self,surface:pg.surface.Surface,pos_adjust:Pos = None ):
        super(ScrollView, self).render(surface, pos_adjust)

