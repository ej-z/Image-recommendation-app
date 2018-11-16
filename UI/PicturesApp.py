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
    pic_info.append({'cluster': 'cluster1', 'data':[{'id':'10041290516', 'info':'kool'},{'id':'10041384303', 'info':'kool2'},{'id':'9960455216', 'info':'kool3'},{'id':'9960426144', 'info':'kool2'},{'id':'9960411914', 'info':'kool'},{'id':'8557266548', 'info':'kool2'},{'id':'10427997426', 'info':'kool3'},{'id':'10686677944', 'info':'kool2'}]})
    PicturesApp(pic_info).run()
    print("hello i am running")
