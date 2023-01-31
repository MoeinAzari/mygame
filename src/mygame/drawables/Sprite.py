import pygame as pg

import os
import pathlib
from ..structures.Rect import Rect
from ..structures.Pos import Pos
from ..structures.Color import Color,ColorConstants
from ..structures.Surface import Surface

from .Object import Object

class Sprite(Object):
    already_loaded_list:list[tuple[str,pg.surface.Surface]] = []

    def __init__(self,path:str,rect:Rect):
        super(Sprite, self).__init__(rect)
        self.offset:Pos = Pos(0,0)
        self.path = path

        found_index = -1
        c = 0
        for i in Sprite.already_loaded_list:
            if i[0] == self.path:
                found_index = c
            c+=1

        if found_index != -1:
            self.raw = Sprite.already_loaded_list[found_index][1]
        else:
            self.raw = pg.image.load(self.path)
            Sprite.already_loaded_list.append((self.path,self.raw))



        self.transformed = self.raw.copy()
        self.transform_picture()


    def update( self ):
        self.transform_picture()

    def transform_picture( self ):

        by_width = Pos(pos=self.raw.get_size()).transform(
                            mult_xy=self.content_rect.width / self.raw.get_width())

        self.offset.reset(new_y=(self.content_rect.height - by_width.y) / 2)

        successor = by_width

        by_height = Pos(pos=self.raw.get_size()).transform(
            mult_xy=self.content_rect.height / self.raw.get_height())

        if by_width.y > self.content_rect.height:
            self.offset.reset(new_x=(self.content_rect.width - by_height.x) / 2)
            successor = by_height

        self.transformed = pg.transform.scale(self.raw,successor)


    @Object.margined_rect.setter
    def margined_rect( self, new_margined_rect: Rect ) :
        super(Sprite, self.__class__).margined_rect.fset(self, new_margined_rect)  # type: ignore

    @Object.margin.setter
    def margin( self, new_margin: tuple[float, float, float, float] ) :
        super(Sprite, self.__class__).margin.fset(self, new_margin)  # type: ignore


    @Object.border.setter
    def border( self, new_border: tuple[float, float, float, float] ) :
        super(Sprite, self.__class__).border.fset(self, new_border)  # type: ignore


    @Object.padding.setter
    def padding( self, new_padding: tuple[float, float, float, float] ) :

        super(Sprite, self.__class__).padding.fset(self, new_padding)  # type: ignore


    def render( self, surface: pg.surface.Surface) :

        super().render(surface)
        surface.blit(self.transformed,self.content_rect.pos.join(self.offset))

    def render_at( self,surface:pg.surface.Surface,at:Pos ):
        super(Sprite, self).render_at(surface, at)
        surface.blit(self.transformed,at.join(Pos(self.left_space,self.top_space))
                        .join(self.offset))






