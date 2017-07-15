import sys, copy

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *

import transit_util, gtfs
from pprint import pprint

class StationSelector(Toplevel):

    def __init__(self, stop_dict, tkStopId=None, master=None, **kwargs):
        self.stop_dict = stop_dict
        list_len = kwargs.get('list_len', 5)

        stop_id_pair = sorted(self.stop_dict.items())
        self.box_vals = [(x, y['stop_name']) for x, y in stop_id_pair if y]
        self.box_vals.sort()

        Toplevel.__init__(self, master, **kwargs)
        #self.config(cursor='none')
        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.state = True
        #self.attributes('-fullscreen', self.state)
        self.tkStopId = tkStopId

        try:
            s_id_list = [x[0] for x in self.box_vals]
            station_inx = s_id_list.index(self.tkStopId.get()[:-1])
            if station_inx < list_len:
                self.s_ids = self.box_vals[:list_len]
            elif station_inx > len(self.box_vals) - list_len - 1:
                self.s_ids = self.box_vals[-list_len:]
            else:
                self.s_ids = self.box_vals[station_inx-list_len/2:station_inx+int(round(list_len/2.0))]
        except (AttributeError, ValueError) as e:
            print "Error: {0}".format(e.message)
            print "Defaulting to first entry"
            self.s_ids = self.box_vals[:list_len]

        self.populate()

    def populate(self):
        self.up_btn = Button(self, text=unichr(0x25B2), width=60, height=2)
        self.down_btn = Button(self, text=unichr(0x25BC), width=60, height=2)

        self.up_btn.bind("<Button-1>", lambda e: self.scroll(-1))
        self.down_btn.bind("<Button-1>", lambda e: self.scroll(1))

        self.up_btn.pack()

        for l in self.s_ids:
            options = {'text':l[1], 'font':("Helvetica", 24, "bold")}
            # put special color on current station
            if l[0].strip() == self.tkStopId.get()[:-1].strip():
                options['fg'] = '#ffdb4d'
            nl = Label(self,**options)
            nl.bind("<Button-1>", lambda e: self.select_station(e))
            nl.pack()

        self.down_btn.pack()

    def select_station(self, event):
        names = [n[1] for n in self.s_ids]
        selected_name = event.widget.cget('text')
        self.tkStopId.set(self.s_ids[names.index(selected_name)][0])
        print "Changed to station {0}".format(selected_name)
        self.destroy()

    def scroll(self, number):
        first_inx = self.box_vals.index(self.s_ids[0]) + number
        last_inx = self.box_vals.index(self.s_ids[-1]) + number

        if first_inx > 0 and last_inx < len(self.box_vals):
            for widget in self.winfo_children():
                widget.destroy()
            self.s_ids = self.box_vals[first_inx:last_inx+1]
            self.populate()
        # don't bother scrolling if beyond the range

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes('-fullscreen', self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes('-fullscreen', self.state)
        return "break"
