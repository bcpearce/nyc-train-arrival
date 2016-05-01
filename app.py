from kivy.app import App 
from kivy.uix.button import Button 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown 
from kivy.clock import Clock

from kivy.utils import escape_markup

from functools import partial

from gtfs import Gtfs
from transit_util import get_stop_list, get_stop_dict

import os, sys

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
        elif minutes <= 0: 
            self.add_widget(Label(
                text='[b][i][color=FFA500]' + escape_markup("Is Now Arriving") + '[/b][/i][/color]', 
                font_size='22sp', markup=True))
            self.add_widget(Label(text="0 min", font_size='20sp'))

class ArrivalList(GridLayout):

    LIST_LIM = 8

    def __init__(self, arrivals, **kwargs):
        super(ArrivalList, self).__init__(**kwargs)
        self.rows = len(arrivals) + 1
        if self.rows > self.LIST_LIM:
            self.rows = self.LIST_LIM + 1
        
        self.update(arrivals)

    def add_header(self, arrival_stop_name):
        stops = get_stop_dict()
        stop = stops[arrival_stop_name[:-1]]

        direction = ""
        if arrival_stop_name[-1] == 'N':
            direction = "Northbound"
        if arrival_stop_name[-1] == 'S':
            direction = "Southbound"

        self.add_widget(Label(
            text=stop + " - " + direction,
            font_size = '40sp'))

    def update(self, arrivals):
        self.clear_widgets()
        self.add_header(arrivals[0][2])
        for arrival in arrivals[:self.rows-1]:
            self.add_widget(Arrival(arrival))

class ArrivalsApp(App):

    def build(self):
        self.station = sys.argv[1]
        if not os.environ.get('MTA_API_KEY'):
            with open("api_key") as f:
                os.environ['MTA_API_KEY'] = f.readline().strip()

        self.gtfs = Gtfs(os.environ['MTA_API_KEY'])
        self.times = self.gtfs.get_time_to_arrival(self.station)
        self.times.sort(key=lambda x: x[1])
        self.arrivals = ArrivalList(self.times)
        Clock.schedule_interval(self.update_arrivals, 10)
        
        return self.arrivals

    def update_arrivals(self, dt):
        try:
            self.times = self.gtfs.get_time_to_arrival(self.station)
            self.times.sort(key=lambda x: x[1])
            self.arrivals.update(self.times)      
        except:
            pass

ArrivalsApp().run()