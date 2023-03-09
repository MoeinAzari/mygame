import pygame as pg
from PIL import Image, ImageFont, ImageDraw

from typing import Optional

from ..structures.Color import Color
from ..structures.Pos import Pos
from ..structures.Rect import Rect
from .Object import Object

class TextBox(Object) :

    def __init__( self, text, text_pos,text_width, font_path, font_size, font_color, background_color,
            direction, wholesome=False ) :

        self.font = ImageFont.truetype(font_path, font_size)
        self.font_color = font_color
        self.font_background_color = background_color
        self.font_direction = direction
        self.text_width = text_width
        self.text_height = 0
        self.text = text
        self.texts: Optional[str] = None
        self.wholesome = wholesome

        self.text_surface: Optional[pg.surface.Surface] = None

        self.generate_texts()
        self.generate_surface()
        super().__init__(Rect(text_pos.x,text_pos.y,self.text_width,self.text_height))

    def update_text( self,new_text=None,new_font_color=None,new_font_bg_color=None,
            new_font_width=None ):

        if new_text is not None:
            self.text = new_text

        if new_font_color is not None:
            self.font_color = new_font_color

        if new_font_bg_color is not None:
            self.font_background_color = new_font_bg_color

        if new_font_width is not None:
            self.text_width = new_font_width


        self.generate_texts()
        self.generate_surface()




    def generate_texts( self ) :
        texts = []
        start = 0
        current = 0

        target = self.text
        if self.wholesome :
            target = self.text.split(" ")

        end = len(target) - 1

        while current != end :
            next_step = target[start :current + 1]
            current_step = target[start :current]

            if self.wholesome :
                current_step = "".join([i + " " for i in current_step])
                next_step = "".join([i + " " for i in next_step])

            if self.font.getsize(next_step)[0] > self.text_width :
                texts.append(current_step)

                start = current
            if current + 1 == end :
                hopped_step = target[start :current + 2]
                if self.wholesome :
                    hopped_step = "".join([i + " " for i in hopped_step])
                texts.append(hopped_step)

            current += 1

        self.text_height = 0
        for i in texts :
            self.text_height += self.font.getsize(i)[1]

        self.texts = texts


    def generate_surface( self ) :
        surface_list = []

        for i in self.texts :
            if i == "": continue # temporary fix

            image = Image.new("RGBA", self.font.getsize(i), (0, 0, 0, 0))

            draw = ImageDraw.Draw(image)

            draw.text((0, 0), i, self.font_color, font=self.font, direction=self.font_direction)
            surface = pg.image.fromstring(image.tobytes(), image.size, image.mode)  # NOQA

            surface_list.append(surface)

        self.text_surface = pg.surface.Surface((self.text_width, self.text_height)).convert_alpha()
        self.text_surface.fill(self.font_background_color)
        y = 0

        for i in surface_list :
            if self.font_direction == "rtl" :
                pos = (self.text_width - i.get_width(), y)
            else :
                pos = (0, y)

            self.text_surface.blit(i, pos)
            y += i.get_height()

    def update( self ):
        self.generate_texts()
        self.generate_surface()
        super(TextBox, self).update()
        self.width = self.text_width + self.horizontal_space
        self.height = self.text_height + self.vertical_space



    def render( self, surface ) :
        super(TextBox, self).render(surface)
        surface.blit(self.text_surface, self.content_rect.pos)

    def render_at( self,surface:pg.surface.Surface,at:Pos ):
        super(TextBox, self).render_at(surface,at)
        surface.blit(self.text_surface,[at.x + self.left_space,at.y + self.top_space])
