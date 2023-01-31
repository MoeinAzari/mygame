import pygame as pg

from .Object import Object
from ..structures.Rect import Rect
from ..structures.Pos import Pos
from ..structures.Color import Color,ColorConstants
cc = ColorConstants

from typing import Optional

class TextHolder (Object):
    __font_name = None
    __font_size = 40

    def __init__(self,rect:Rect,text:str,font:pg.font.Font=None):
        super(TextHolder, self).__init__(rect)
        self.margin = self.border = self.padding = [0] * 4
        if font is None:
            self.font = pg.font.Font(TextHolder.__font_name,TextHolder.__font_size)
        else:
            self.font = font

        self.__texts:list[str] = []
        self.text = text
        self.max_width = self.width
        self.text_surface:Optional[pg.surface.Surface] = None

        self.update()

    def update_surface( self ):
        height = 0
        width = max([self.font.size(i)[0] for i in self.__texts ])

        if len(self.__texts) != 0:
            height = self.font.size(self.__texts[0])[1] * len(self.__texts)

        self.text_surface = pg.surface.Surface([width,height]).convert_alpha()
        self.text_surface.fill(cc.BLUE.with_alpha(255))


        current_height = 0
        for i in self.__texts:
            mfont = self.font.render(i,True,cc.BLACK)
            self.text_surface.blit(mfont,[0,current_height])
            current_height += mfont.get_height()





    def render( self,surface:pg.surface.Surface):
        super(TextHolder, self).render(surface)
        surface.blit(self.text_surface,self.content_rect.pos)

    def render_at( self,surface:pg.surface.Surface,at:Pos ):
        super(TextHolder, self).render_at(surface,at)
        surface.blit(self.text_surface, at.join(Pos(self.left_space,self.top_space)))



    def generate_texts( self ):

        self.__texts.clear()
        start = 0
        current = 0
        end = len(self.text) - 1


        while current != end:
            if self.font.size(
                    self.text[start:current+1])[0] > self.max_width - self.horizontal_space:
                self.__texts.append(self.text[start:current])
                start = current
            if current + 1 == end:
                self.__texts.append(self.text[start:current + 1])

            current += 1

    def update( self,new_text=None):

        if new_text is not None: self.text = new_text
        self.max_width = self.width

        self.generate_texts()
        self.update_surface()
        self.margined_rect.height = self.text_surface.get_height()


