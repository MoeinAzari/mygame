import time

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
        self.object_list :list[Optional[Sprite,(Pos,pg.surface.Surface)]] = []
        self.content_surface: Optional[pg.surface.Surface] = None

        self.event_holder:Optional[EventHolder] = None
        self.all_lines_height:Optional[float] = 0
        self.objects_adjust_pos = Pos(0,0)
        self.update()

    def update( self ):

        self.sync_objects()
        self.update_surface()


    def update_surface( self ):
        super(Container, self).update()

        self.content_surface = pg.surface.Surface(self.content_rect.size).convert_alpha()
        if self.has_surface :
            self.content_surface.set_alpha(self.alpha)

        self.content_surface.fill(ColorConstants.GLASS)

        for i in self.object_list :


            if i.type == Sprite:
                at = i.margined_rect.pos.join(
                    self.content_rect.pos.transform(mult_xy=-1).join(self.objects_adjust_pos))
                i.render_at(self.content_surface, at)
            elif i.type == tuple[Pos,pg.surface.Surface]:
                print('yaya')
                at = i[0].join(
                    self.content_rect.pos.transform(mult_xy=-1).join(self.objects_adjust_pos))
                self.content_surface.blit(i[1],at.join(self.left_space,self.top_space))
            else:
                print(i.type)


    def get_events( self ):
        mouse_pos = self.event_holder.mouse_pos
        if self.content_rect.collidepoint(mouse_pos):

            if EventConstants.MOUSE_LEFT in self.event_holder.mouse_pressed_keys:

                c = 0
                for i in self.object_list:
                    if i.margined_rect.copy().join_pos(pos=self.objects_adjust_pos
                            ).collidepoint(mouse_pos):
                        self.object_list.remove(i)
                        self.was_changed = True
                        break

                    c+=1


    def check_events( self ):
        # if self.was_changed:
        #     self.sync_objects()

        super(Container, self).check_events()

    def render_debug( self,surface:pg.surface.Surface ):
        super(Container, self).render_debug(surface)
        if self.should_render_debug:
            for i in self.object_list:
                pg.draw.rect(surface,ColorConstants.WHITE,i.margined_rect.copy(

                ).join_pos(pos=self.objects_adjust_pos)
                    ,width=5)

    def render( self,surface:pg.surface.Surface ):
        super(Container, self).render(surface)
        surface.blit(self.content_surface,self.content_rect)





    def resize_objects( self,scale:float ):
        self.was_changed = True

        for i in self.object_list:

            i.width = i.width * scale
            i.height = i.height * scale

            if type(i) == Sprite:
                i.update()

        self.update()

    def create_object( self,object_size:Pos ):

        self.was_changed = True

        new_sprite = Sprite(Rect(0,0
                                    ,object_size.x,object_size.y))

        new_sprite.margin = 5,5,5,5
        new_sprite.border = 5,5,5,5
        new_sprite.padding = 5,5,5,5

        new_sprite.content_max_width = 150
        new_sprite.content_max_height = 150



        new_sprite.color = ColorConstants.BLUE,ColorConstants.BLACK\
                                ,ColorConstants.RED,ColorConstants.HOT_RED
        new_sprite.color = [Color.randomColor(True) for _ in range(4)]
        new_sprite.has_surface = True

        new_sprite.update()

        self.object_list.append(new_sprite)

        self.update()

    def sync_objects( self ):

        pos = self.content_rect.pos.copy()

        self.all_lines_height = 0
        last_line_max_height = 0
        lines_count = 0

        last_i = None
        for i in self.object_list:

            if last_i is not None:
                if pos.x + last_i.width + i.width < self.content_rect.x + self.content_rect.width:
                    pos.x += last_i.width
                    if i.height > last_line_max_height :
                        last_line_max_height = i.height
                        if lines_count == 1:
                            self.all_lines_height = last_line_max_height
                else:
                    lines_count += 1
                    pos.x = self.content_rect.x
                    pos.y += last_line_max_height
                    last_line_max_height = i.height
                    self.all_lines_height += last_line_max_height
            else:
                last_line_max_height = i.height
                self.all_lines_height += last_line_max_height
                lines_count += 1

            i.margined_rect.reset_pos(pos=pos)
            last_i = i



