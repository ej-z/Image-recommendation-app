from pymongo import MongoClient
import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class PicturesApp(App):
    def build(self):

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db['LIU_commonterms']

        main_layout = BoxLayout(orientation='vertical')

        for info in self.pic_info:
            cluster_layout = BoxLayout(orientation='vertical')
            cluster_layout.add_widget(Label(text=info['cluster'], size_hint=(1, .1)))
            tile_layout = GridLayout(cols=3)
            for d in info['data']:
                t = table.find_one({'image': d['id']})
                inner_layout = BoxLayout(orientation='vertical')
                inner_layout.add_widget(Label(text=t['image'], size_hint=(1, .15)))
                inner_layout.add_widget(Image(source=t['imagepath']))
                inner_layout.add_widget(Label(text=d['info'], size_hint=(1, .15)))
                tile_layout.add_widget(inner_layout)
            cluster_layout.add_widget(tile_layout)
            main_layout.add_widget(cluster_layout)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(main_layout)
        return root

    def __init__(self, p_i):
        App.__init__(self)
        self.pic_info = p_i

if __name__ == '__main__':
    pic_info = []
    pic_info.append({'cluster': 'cluster1', 'data':[{'id':'9067739127', 'info':'kool'},{'id':'9067738157', 'info':'kool2'},{'id':'9067739127', 'info':'kool3'},{'id':'9067738157', 'info':'kool2'},{'id':'9067739127', 'info':'kool'},{'id':'9067738157', 'info':'kool2'},{'id':'9067739127', 'info':'kool3'},{'id':'9067738157', 'info':'kool2'}]})
    PicturesApp(pic_info).run()