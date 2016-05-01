#!/usr/bin/python
import sys, os
from gtfs import Gtfs

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *

class SubwayBullet(PhotoImage):

    def __init__(self, service_name, **kwargs):
        kwargs['file'] = "img/{0}.png".format(service_name)
        PhotoImage.__init__(self, **kwargs)

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.attributes('-zoomed', True)
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.state = True
        self.tk.attributes('-fullscreen', self.state)
        self.update_arrivals('239N')

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes('-fullscreen', self.state)
        return "break"

    def update_arrivals(self, stop_id):
        gtfs = Gtfs(os.environ['MTA_API_KEY'])
        try:
            arrivals = gtfs.get_time_to_arrival('239N')
        except:
            return

        for arrival in arrivals:
            self.arrival_frame = Frame(self.frame)
            self.arrival_frame.pack(side=BOTTOM)
            bullet = SubwayBullet(arrival[0])
            icon = Label(self.arrival_frame, image=bullet)
            icon.bullet = bullet
            icon.pack(side=LEFT)
            statement = Label(self.arrival_frame, text="Will arrive In")
            statement.pack(side=LEFT)
            minutes = round(float(arrival[1]/60.0))
            time_str = "{0} min".format(int(minutes))
            time = Label(self.arrival_frame, text=time_str)
            time.pack(side=LEFT)
        

if __name__ == "__main__":

    if not os.environ.get('MTA_API_KEY'):
        with open("api_key") as f:
            os.environ['MTA_API_KEY'] = f.readline().strip()

    w = FullscreenWindow()
    w.tk.mainloop()
