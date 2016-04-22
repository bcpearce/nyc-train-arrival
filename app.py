from kivy.app import App 
from kivy.uix.button import Button 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.utils import escape_markup
from gtfs import Gtfs

import os

class SubwayBullet(Image):

    def __init__(self, service, **kwargs):
        img_path = "img/{0}.png".format(service)
        kwargs['source'] = img_path
        super(SubwayBullet, self).__init__(**kwargs)

class Arrival(GridLayout):

    COLS = 3
    FONT = {'font_size':'20sp'}

    def __init__(self, arrival_tup, **kwargs):
        super(Arrival, self).__init__(**kwargs)
        self.cols = self.COLS
        minutes = round(float(arrival_tup[1]/60.0))
        time_str = "{0} min".format(int(minutes))
        self.add_widget(SubwayBullet(arrival_tup[0]))
        if minutes > 0:
            self.add_widget(Label(text='Will Arrive In', font_size='20sp'))
            self.add_widget(Label(text=time_str, font_size='20sp'))
        else: 
            self.add_widget(Label(
                text='[b][i][color=FFA500]' + escape_markup("Is Now Arriving") + '[/b][/i][/color]', 
                font_size='22sp', markup=True))
            self.add_widget(Label(text="0 min", font_size='20sp'))

class ArrivalList(GridLayout):

    def __init__(self, arrivals, **kwargs):
        super(ArrivalList, self).__init__(**kwargs)
        self.rows = len(arrivals)
        for arrival in arrivals:
            self.add_widget(Arrival(arrival))

class ArrivalsApp(App):

    def build(self):
        if not os.environ.get('MTA_API_KEY'):
            with open("api_key") as f:
                os.environ['MTA_API_KEY'] = f.readline().strip()

        gtfs = Gtfs(os.environ['MTA_API_KEY'])
        times = gtfs.get_time_to_arrival('234N')
        times.sort(key=lambda x: x[1])
        return ArrivalList(times)

ArrivalsApp().run()