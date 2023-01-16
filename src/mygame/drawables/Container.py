import pygame as pg
from typing import Optional

from .Object import Object
from .Sprite import Sprite
from ..os.EventHolder import EventHolder,EventConstants
from ..structures.Rect import Rect
from ..structures.Pos import Pos
from ..structures.Color import Color,ColorConstants

class Container(Object):
    def __init__(self,rect:Rect):
        super(Container, self).__init__(rect)
        self.object_list :list[Sprite] = []
        self.surface:Optional[None,pg.surface.Surface] = None
        self.event_holder:EventHolder = None
        self.update_surface()


    def update( self ):


        self.sync_objects()
        self.update_surface()



    def update_surface( self ):


        self.surface = pg.surface.Surface(self.margined_rect.size)
        content_surface = pg.surface.Surface(self.content_rect.size).convert_alpha()
        content_surface.fill(ColorConstants.GLASS)

        super(Container, self).render(self.surface,
            self.margined_rect.pos.transform(mult_xy=-1))

        for i in self.object_list :
            i.render(content_surface, self.content_rect.pos.transform(mult_xy=-1))

        self.surface.blit(content_surface,
            self.content_rect.pos.join(self.margined_rect.pos.transform(mult_xy=-1)))

        # self.surface.blit(self.surface, self.margined_rect.pos)


    def check_events( self ):
        if self.content_rect.collidepoint(self.event_holder.mouse_pos):
            if EventConstants.MOUSE_LEFT in self.event_holder.mouse_pressed_keys:
                print('real mouse pos',self.event_holder.mouse_pos,
                            'relative mouse pos',self.event_holder.mouse_pos.join(
                        self.content_rect.pos.transform(mult_xy=-1)
                    ))


    def render( self,surface:pg.surface.Surface,pos_adjust:Pos = None ):
        surface.blit(self.surface,self.margined_rect.pos)

    def resize_objects( self,scale:float ):


        for i in self.object_list:

            i.width = i.width * scale
            i.height = i.height * scale

            if type(i) == Sprite:
                i.update()

        self.update()

    def create_object( self,object_size:Pos ):


        new_sprite = Sprite(Rect(self.content_rect.x,self.content_rect.y
                                    ,object_size.x,object_size.y))
        zero = 0,0,0,0
        new_sprite.margin = 5,5,5,5
        new_sprite.border = 5,5,5,5
        new_sprite.padding = 5,5,5,5

        new_sprite.content_max_width = 150
        new_sprite.content_max_height = 150

        # new_sprite.margin = new_sprite.border = new_sprite.padding = zero

        new_sprite.color = ColorConstants.BLUE,ColorConstants.BLACK\
                                ,ColorConstants.RED,ColorConstants.HOT_RED
        new_sprite.color = [Color.randomColor(True) for _ in range(4)]
        new_sprite.alpha_support = True

        new_sprite.update()

        self.object_list.append(new_sprite)

        self.update()

    def sync_objects( self ):

        pos = self.content_rect.pos.copy()

        last_line_max_height = 0

        last_i = None
        for i in self.object_list:

            if last_i is not None:
                if pos.x + last_i.width + i.width < self.content_rect.x + self.content_rect.width:
                    pos.x += last_i.width
                    if i.height > last_line_max_height :
                        last_line_max_height = i.height
                else:
                    pos.x = self.content_rect.x
                    pos.y += last_line_max_height
                    last_line_max_height = i.height
            else:
                last_line_max_height = i.height

            i.margined_rect.reset_pos(pos=pos)

            last_i = i


