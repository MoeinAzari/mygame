from .src.mygame.drawables import Container,Menu,MSprite,Object,Page
from .src.mygame.drawables import ScrollView,Sprite,TextBox,TextHolder

Container = Container.Container
Object = Object.Object
ScrollView = ScrollView.ScrollView # using these led to typing problems with ide
Sprite = Sprite.Sprite
TextHolder = TextHolder.TextHolder
TextBox = TextBox.TextBox


from .src.mygame.drawables.ScrollView import ScrollView
from .src.mygame.drawables.Container import Container
from .src.mygame.drawables.Object import Object
from .src.mygame.drawables.Sprite import Sprite
from .src.mygame.drawables.TextBox import TextBox
from .src.mygame.drawables.TextHolder import TextHolder


