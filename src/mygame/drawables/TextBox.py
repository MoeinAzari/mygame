import pygame as pg

from ..structures.Pos import Pos
from ..structures.Rect import Rect
from ..structures.Color import Color
from .ScrollView import ScrollView
from .TextHolder import TextHolder

class TextBox(ScrollView):

    def __init__(self,rect:Rect,text:str):
        super(TextBox, self).__init__(rect)

        self.text_holder = TextHolder(text,self.content_rect.width)


        self.object_list.append((Pos(0,0),self.text_holder.text_surface))

        self.update()



    def render( self,surface:pg.surface.Surface,pos_adjust:Pos = None ):
        super(TextBox, self).render(surface,pos_adjust)







