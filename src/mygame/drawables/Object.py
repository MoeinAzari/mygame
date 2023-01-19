import time
from typing import Optional

import pygame as pg

from ..structures.Pos import Pos
from ..structures.Rect import Rect
from ..structures.Color import Color,ColorConstants
from ..structures.Surface import Surface

colors = ColorConstants

# It could have been DrawableObject but that's not finger friendly
class Object(object) :

    """
    "Object" contains the information about how something should be rendered
    on the screen.
    The content to be rendered is provided by subclasses that use this class
     it has padding, border and margin properties.
    But its functionality is completely different from HTML drawable objects.
    Since the rect parameter which is fed to this Object while initialization determines
     an absolute rendering point and  DOES NOT CHANGE IN RELATION TO OTHER OBJECTS.
    So the rectangular size of the content to be rendered is:
        content_width = rect.width - padding_horizontal + border_horizontal + margin_horizontal
        content_height = rect.height - padding_vertical + border_vertical + margin_vertical
    """
    def __init__( self, rect: Rect ) :

        self.__rect: Rect = rect
        self.surface: Optional[pg.surface.Surface] = None
        self.has_surface:bool = False
        self.__alpha = 200
        self.was_changed:bool = False

        self.should_render_debug:bool = False

        self.margined_color: Optional[Color,None] = None
        self.bordered_color: Optional[Color,None] = None
        self.padded_color: Optional[Color,None] = None
        self.content_color: Optional[Color,None] = None

        self.padding_left = 0
        self.padding_right = 0
        self.padding_top = 0
        self.padding_bottom = 0

        self.margin_left = 0
        self.margin_right = 0
        self.margin_top = 0
        self.margin_bottom = 0

        self.border_left_width = 0
        self.border_right_width = 0
        self.border_top_width = 0
        self.border_bottom_width = 0

        self.content_min_width = 0
        self.content_min_height = 0
        self.content_max_width = -1
        self.content_max_height = -1

        self.color = colors.BLUE,colors.BLACK,colors.GREEN,colors.WHITE


        super(Object, self).__init__()

    def __str__(self):
        return f'Object{{\n\trect:{self.margined_rect}\n\tmargin:{self.margin}'\
               f'\n\tborder:{self.border}'\
               f'\n\tpadding:{self.padding}\n}}'

    @property
    def color( self ):
        return self.margined_color,self.bordered_color,self.padded_color,self.content_color

    @color.setter
    def color( self,colors_:tuple[Color,Color,Color,Color] ):
        self.margined_color = colors_[0]
        self.bordered_color = colors_[1]
        self.padded_color = colors_[2]
        self.content_color = colors_[3]


    def check_events( self ):
        if self.was_changed:
            self.update()


    
    @property
    def alpha( self ):
        return self.__alpha
    
    @alpha.setter
    def alpha( self,new_alpha:int ):
        if 0<=new_alpha<=255 and self.has_surface:
            self.__alpha = new_alpha
            self.was_changed = True


    @property
    def x( self ):
        return self.__rect.x

    @x.setter
    def x( self,new_x ):
        self.__rect.x = new_x
        self.was_changed = True

    @property
    def y( self ) :
        return self.__rect.y

    @y.setter
    def y( self, new_y ) :
        self.__rect.y = new_y
        self.was_changed = True


    @property
    def width( self ) :
        return self.__rect.width

    @width.setter
    def width( self, new_width ) :
        if new_width - self.content_min_width >= self.horizontal_space:
            if new_width <= self.content_max_width or self.content_max_width == -1:
                self.was_changed = True
                self.margined_rect.width = new_width

    @property
    def height( self ) :
        return self.__rect.height

    @height.setter
    def height( self, new_height ) :
        if new_height - self.content_min_height >= self.vertical_space :
            if new_height <= self.content_max_height or self.content_max_height == -1 :
                self.was_changed = True
                self.margined_rect.height = new_height

    @property
    def margined_rect( self ) -> Rect:
        return self.__rect

    @margined_rect.setter
    def margined_rect( self,p_rect:Rect ):
        self.x = p_rect.x
        self.y = p_rect.y
        self.width = p_rect.width
        self.height = p_rect.height


    @property
    def bordered_rect( self ):
        rect = self.margined_rect.copy()

        rect.x += self.margin_left
        rect.width -= self.margin_right * 2

        rect.y += self.margin_top
        rect.height -= self.margin_bottom * 2

        return rect

    @property
    def padded_rect( self ):
        rect = self.bordered_rect.copy()

        rect.x += self.border_left_width
        rect.width -= self.border_right_width * 2

        rect.y += self.border_top_width
        rect.height -= self.border_bottom_width * 2

        return rect


    @property
    def content_rect( self ) :
        rect = self.padded_rect.copy()

        rect.x += self.padding_left
        rect.width -= self.padding_right * 2

        rect.y += self.padding_top
        rect.height -= self.padding_bottom * 2

        return rect



    @property
    def padding( self ) -> tuple[float,float,float,float]:
        return self.padding_left, self.padding_top, self.padding_right, self.padding_bottom


    @padding.setter
    def padding( self, new_padding: tuple[float, float, float, float] ) :
        self.padding_left, self.padding_top = new_padding[:2]
        self.padding_right, self.padding_bottom = new_padding[2 :]


    @property
    def margin( self ) -> tuple[float,float,float,float] :
        return self.margin_left, self.margin_top, self.margin_right, self.margin_bottom


    @margin.setter
    def margin( self, new_margin: tuple[float, float, float, float] ) :
        self.margin_left, self.margin_top = new_margin[:2]
        self.margin_right, self.margin_bottom = new_margin[2 :]

    @property
    def border( self ) -> tuple[int, int, int, int] :
        return self.border_left_width, self.border_top_width,\
            self.border_right_width, self.border_bottom_width

    @border.setter
    def border( self, new_border: tuple[int, int, int, int] ) :
        self.border_left_width, self.border_top_width = new_border[:2]
        self.border_right_width, self.border_bottom_width = new_border[2 :]

    @property
    def left_space(self):
        return self.margin_left + self.border_left_width + self.padding_left

    @property
    def right_space( self ) :
        return self.margin_right + self.border_right_width + self.padding_right

    @property
    def top_space( self ) :
        return self.margin_top + self.border_top_width + self.padding_top

    @property
    def bottom_space( self ) :
        return self.margin_bottom + self.border_bottom_width + self.padding_bottom

    @property
    def horizontal_space( self ):
        return self.left_space + self.right_space

    @property
    def vertical_space( self ) :
        return self.top_space + self.bottom_space


    def update( self ):
        self.was_changed = False

        self.surface = pg.surface.Surface(self.margined_rect.size).convert_alpha()
        self.surface.set_alpha(self.alpha)

        diff = Rect(-self.x,-self.y,0,0)


        pg.draw.rect(self.surface, self.margined_color,
            self.margined_rect.copy().join(diff))

        pg.draw.rect(self.surface, self.bordered_color,
            self.bordered_rect.copy().join(diff))

        pg.draw.rect(self.surface, self.padded_color,
            self.padded_rect.copy().join(diff))

        pg.draw.rect(self.surface, self.content_color,
            self.content_rect.copy().join(diff))

    def render_debug( self,surface:pg.surface.Surface ):
        if self.should_render_debug :
            ...

    def render( self,surface:pg.surface.Surface) :

        if self.has_surface and self.surface is not None:
            surface.blit(self.surface,self.margined_rect.pos)
        else:
            pg.draw.rect(surface,self.margined_color,self.margined_rect)
            pg.draw.rect(surface,self.bordered_color,self.bordered_rect)
            pg.draw.rect(surface,self.padded_color,self.padded_rect)
            pg.draw.rect(surface,self.content_color,self.content_rect)




    def render_at( self,surface:pg.surface.Surface,at:Pos ):
        if self.has_surface and self.surface is not None:
            surface.blit(self.surface,at)
        else:
            margined_pos = at.copy()
            bordered_pos = at.transform(self.margin_left,self.margin_top)
            padded_pos = bordered_pos.transform(self.border_left_width,self.border_top_width)
            content_pos = padded_pos.transform(self.padding_left,self.padding_top)

            pg.draw.rect(surface,self.margined_color
                ,self.margined_rect.copy().reset_pos(pos=margined_pos))

            pg.draw.rect(surface,self.bordered_color
                ,self.bordered_rect.copy().reset_pos(pos=bordered_pos))

            pg.draw.rect(surface,self.padded_color
                ,self.padded_rect.copy().reset_pos(pos=padded_pos))

            pg.draw.rect(surface,self.content_color
                ,self.content_rect.copy().reset_pos(pos=content_pos))



    def all_attrs( self ) -> str :
        text = "Object {\n"
        L = vars(self)
        for i in L :
            text += "\t" + str(i) + " = " + str(L[i]) + "\n"
        text += "}"
        return text
