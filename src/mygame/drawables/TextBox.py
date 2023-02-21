import pygame as pg
from PIL import Image,ImageFont,ImageDraw

from ..structures.Color import Color
from ..structures.Pos import Pos
from ..structures.Rect import Rect


class TextBox:
    def __init__(self,text,text_width,font_path,font_size,font_color,background_color,direction):
        self.font = ImageFont.truetype(font_path,font_size)

        self.width = text_width
        self.height = 0
        self.text = text
        self.texts = self.generate_texts()

        surface_list = []

        for i in self.texts:

            image = Image.new("RGBA",self.font.getsize(i),(0,0,0,0))

            draw = ImageDraw.Draw(image)

            draw.text((0,0),i,font_color,font=self.font,direction=direction)

            surface = pg.image.fromstring(image.tobytes(),image.size,
                image.mode) # NOQA

            surface_list.append(surface)


        self.surface = pg.surface.Surface((self.width,self.height)).convert_alpha()
        self.surface.fill(background_color)
        y = 0

        for i in surface_list:
            if direction == "rtl" :
                pos = (self.width-i.get_width(),y)
            else:
                pos = (0,y)

            self.surface.blit(i,pos)
            y += i.get_height()



    def generate_texts( self ):

        texts = []
        start = 0
        current = 0
        end = len(self.text) - 1


        while current != end:
            if self.font.getsize(
                    self.text[start:current+1])[0] > self.width:
                texts.append(self.text[start:current])
                start = current
            if current + 1 == end:
                texts.append(self.text[start:current + 2])

            current += 1

        self.height = 0
        for i in texts:
            self.height += self.font.getsize(i)[1]


        return texts



    def render( self,surface,at ):
        surface.blit(self.surface,at)