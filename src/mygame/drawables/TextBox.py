import pygame as pg

from ..structures.Pos import Pos
from ..structures.Rect import Rect
from ..structures.Color import Color
from .ScrollView import ScrollView
from .TextHolder import TextHolder

class TextBox(ScrollView):

    def __init__(self,rect:Rect,text:str):

        self.text_holder = TextHolder(rect.copy(),text)

        super(TextBox, self).__init__(rect)
        self.object_list.append(self.text_holder)

        self.update()



    def update( self  ):
        self.text_holder.max_width = self.text_holder.width = self.content_rect.width
        self.text_holder.update()
        super(TextBox, self).update()



    def render( self,surface:pg.surface.Surface,pos_adjust:Pos = None ):
        super(TextBox, self).render(surface, pos_adjust)
        print(self.object_list)

    def render_at( self,surface:pg.surface.Surface,at:Pos ):
        super(TextBox, self).render_at(surface, at)
        print(self.object_list)



