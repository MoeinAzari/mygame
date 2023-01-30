import pygame as pg

from ..structures.Color import Color,ColorConstants
cc = ColorConstants

from typing import Optional

class TextHolder:
    __font_name = None
    __font_size = 40

    def __init__(self,text:str,max_width:int,font:pg.font.Font=None):
        if font is None:
            self.font = pg.font.Font(TextHolder.__font_name,TextHolder.__font_size)
        else:
            self.font = font

        self.__texts:list[str] = []
        self.text = text
        self.max_width = max_width
        self.surface:Optional[pg.surface.Surface] = None

        self.update()

    def update_surface( self ):
        height = 0
        width = max([self.font.size(i)[0] for i in self.__texts ])

        if len(self.__texts) != 0:
            height = self.font.size(self.__texts[0])[1] * len(self.__texts)

        self.surface = pg.surface.Surface([width,height]).convert_alpha()
        self.surface.fill(cc.BLUE.with_alpha(100))


        current_height = 0
        for i in self.__texts:
            mfont = self.font.render(i,True,cc.BLACK)
            self.surface.blit(mfont,[0,current_height])
            current_height += mfont.get_height()


    def generate_texts( self ):

        self.__texts.clear()
        start = 0
        current = 0
        end = len(self.text) - 1


        while current != end:
            if self.font.size(self.text[start:current+1])[0] > self.max_width:
                self.__texts.append(self.text[start:current])
                start = current
            if current + 1 == end:
                self.__texts.append(self.text[start:current + 1])

            current += 1

    def update( self,new_text=None ):
        if new_text is not None: self.text = new_text
        self.generate_texts()
        self.update_surface()


