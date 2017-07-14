#!/usr/bin/python
import sys, os, traceback, datetime, urllib2, json
from gtfs import Gtfs
from transit_util import get_stop_dict, get_stop_name_dict

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *

from subway_bullet import *
from station_selector import *

class FullscreenWindow:

    def __init__(self, stop_id, server_url):
        self.stop_id = stop_id
        self.server_url = server_url
        self.server_station_list = "{0}/stop_list".format(self.server_url)

        self.tk = Tk()
        self.tk.wm_title("NYC Train Arrival")

        self.tk.configure(bg='#111111')
        self.tk.tk_setPalette(background='#111111', 
            foreground='#ffffff')

        self.tk.attributes('-zoomed', True)
        self.tk.config(cursor='none')

        self.frame = Frame(self.tk)
        self.frame.pack()
        self.list_frame = Frame(self.tk)
        self.list_frame.pack()
        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.state = True
        self.tk.attributes('-fullscreen', self.state)

        self.stops = get_stop_dict()

        # only populate with GTFS data stations
        #gtfs = Gtfs(os.environ['MTA_API_KEY'])
        response = urllib2.urlopen(self.server_station_list)
        self.stop_keys = json.loads(response.read())
        self.stop_dict = transit_util.get_stop_names_from_keys(self.stop_keys)
        
        self.add_header()
        self.update_arrivals()

    def refresh(self):
        self.clear_old_arrivals()
        self.clear_header()
        self.add_header()
        self.print_arrivals()

    def northbound_southbound_toggle(self):
        if self.stop_id[-1] == 'N':
            self.stop_id = self.stop_id[:-1] + 'S'
        elif self.stop_id[-1] == 'S':
            self.stop_id = self.stop_id[:-1] + 'N'
        print "Switched direction {0}".format(self.stop_id)
        self.refresh()

    def get_direction(self):
        direction = ""
        if self.stop_id[-1] == 'N':
            direction = "Northbound"
        if self.stop_id[-1] == 'S':
            direction = "Southbound"
        return direction

    def update_arrivals(self):
        try:
            self.print_arrivals()
        finally:
            # run even if printing arrivals fails
            self.tk.after(30000, self.update_arrivals)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes('-fullscreen', self.state)
        return "break"

    def add_header(self):
        stop = self.stops[self.stop_id[:-1]]

        direction = self.get_direction()
        
        self.header = Label(self.frame,
            text=stop,
            font=("Helvetica", 30, "bold"))

        self.subheader = Label(self.frame,
            text=direction,
            font=("Helvetica", 24, "bold"))

        self.header.bind("<Button-1>", lambda e: self.launch_station_selector())
        self.subheader.bind("<Button-1>", lambda e: self.northbound_southbound_toggle())
        self.header.pack(side=TOP)
        self.subheader.pack(side=TOP)

    def launch_station_selector(self):
        station_name = StringVar()
        station_name.set(self.header.cget('text'))
        self.station_selector = StationSelector(
            self.stop_keys, station_name)
        self.station_selector.wait_window()
        self.set_new_stop(station_name.get())

    def set_new_stop(self, station_name):
        direction = self.get_direction()[0]
        self.stop_id = self.stop_dict[station_name] + direction
        print "New stop_id {0}".format(self.stop_id)
        self.refresh()

    def clear_header(self):
        try:
            for widget in self.frame.winfo_children():
                widget.destroy()
        except:
            pass

    def clear_old_arrivals(self):
        try:
            for widget in self.list_frame.winfo_children():
                widget.destroy()
        except:
            # handle exception caused by lack of arrivals
            pass

    def format_icon(self, arrival):

        UNICODE_DICT = {'1':unichr(0x2460),
                        '2':unichr(0x2461),
                        '3':unichr(0x2462),
                        '4':unichr(0x2463),
                        '5':unichr(0x2464),
                        '5X':unichr(0x2464),
                        '6':unichr(0x2465),
                        'GS':unichr(0x24C8),
                        '6X':unichr(0x2465)+unichr(0x2666)}

        try:
            bullet = SubwayBullet(arrival['route'])
            bullet = bullet.subsample(2)
            icon = Label(self.arrival_frame, image=bullet)
            icon.bullet = bullet
            
        except TclError:
            print "Failed to use icons, falling back to text formatting"
            if arrival.get('route')[0] in ['1','2','3']:
                fg = '#EE352E'
            elif arrival.get('route')[0] in ['4','5','6']:
                fg = '#00933C'
            elif arrival.get('route')[0] in ['L']:
                fg = '#A7A9AC'
            else:
                fg = '#808183'
            icon = Label(self.arrival_frame, 
                text=u"  {0}  ".format(UNICODE_DICT.get(arrival['route'], arrival['route'])),
                font=("Helvetica", 24), fg=fg)

        return icon

    def print_arrivals(self):
        try:
            self.server_route = "{0}/stop/{1}".format(self.server_url, self.stop_id)
            response = urllib2.urlopen(self.server_route)
            print "Received response from {0}".format(self.server_route)
            arrivals = json.loads(response.read())
            arrivals.sort(key=lambda x: x['time'])
        except:
            return

        self.clear_old_arrivals()

        for arrival in arrivals:
            minutes = round(float(arrival['time']/60.0))
            # if the minutes is < -2, don't bother displaying
            if minutes < -2:
                continue

            self.arrival_frame = Frame(self.list_frame)
            self.arrival_frame.pack(side=TOP, fill=X)

            
            if minutes < 0 and minutes >= -2:
                minutes = 0

            if minutes == 0:
                statement = Label(self.arrival_frame, text="  Now Arriving ",
                    font=("Helvetica", 24, 'bold italic'), fg='#ffdb4d')

            else:
                statement = Label(self.arrival_frame, text="  Will Arrive In ",
                    font=("Helvetica", 24))

            if minutes >= 0:
                icon = self.format_icon(arrival)

                icon.pack(side=LEFT)
                statement.pack(side=LEFT)
                
                time_str = "{0} min".format(int(minutes))
                time = Label(self.arrival_frame, text=time_str,
                    font=("Helvetica", 24))
                time.pack(side=RIGHT)

        print "Updated {0}".format(str(datetime.datetime.now()))
        

if __name__ == "__main__":

    station = sys.argv[1]

    try:
        server_url = sys.argv[2]
    except IndexError:
        server_url = 'http://127.0.0.1:5000'

    w = FullscreenWindow(station, server_url)
    w.tk.mainloop()
