from pymongo import MongoClient
import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from multiprocessing import Process

class PicturesApp(App):
    def build(self):

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db['LIU_commonterms']
        tile_layout = GridLayout(cols=3)
        for d in self.pic_info:
            print(d['id'])
            t = table.find_one({'image': d['id']})
            if t is not None:
                inner_layout = BoxLayout(orientation='vertical')
                inner_layout.add_widget(Image(source=t['imagepath']))
                inner_layout.add_widget(Label(text=d['info'], size_hint=(1, .15)))
                tile_layout.add_widget(inner_layout)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(tile_layout)
        return root

    def __init__(self, p_i):
        App.__init__(self)
        self.pic_info = p_i

def show_pics(pic_info):
    ty = PicturesApp(pic_info)
    ty.run()

def display_images(pic_info):
    proc1 = Process(target=show_pics, args=(pic_info,))
    proc1.start()
    inp = input("To stop Press any key: ")
    proc1.join()

if __name__ == '__main__':
    pic_info = ([{'id':'9067739127', 'info':'kool'},{'id':'9067738157', 'info':'kool2'},{'id':'9067739127', 'info':'kool3'},{'id':'9067738157', 'info':'kool2'},{'id':'9067739127', 'info':'kool'},{'id':'9067738157', 'info':'kool2'},{'id':'9067739127', 'info':'kool3'},{'id':'9067738157', 'info':'kool2'}])
    PicturesApp(pic_info).run()
