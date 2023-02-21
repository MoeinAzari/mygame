from .TextBox import TextBox
from .ScrollView import ScrollView

from ..structures.Pos import Pos
from ..structures.Rect import Rect
from ..structures.Color import Color


class TextView(ScrollView):
    def __init__(self,rect:Rect,text_box:TextBox):
        super(TextView, self).__init__(rect)

        self.text_box_list = [text_box]


    def add_text_box( self , text_box:TextBox):
        self.text_box_list.append(text_box)
