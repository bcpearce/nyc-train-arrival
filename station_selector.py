import sys, copy

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *

import transit_util, gtfs

class StationSelector(Toplevel):

    def __init__(self, stop_keys, tkStationName=None, master=None, **kwargs):
        self.stop_keys = stop_keys
        self.stop_dict = transit_util.get_stop_names_from_keys(self.stop_keys)
        self.box_vals = sorted(self.stop_dict.keys())

        list_len = kwargs.get('list_len', 5)

        Toplevel.__init__(self, master, **kwargs)

        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.state = True
        self.attributes('-fullscreen', self.state)
        self.tkStationName = tkStationName

        try:
            station_inx = self.box_vals.index(self.tkStationName.get())
            if station_inx < list_len:
                self.labels = self.box_vals[:list_len]
            elif station_inx > len(self.box_vals) - list_len - 1:
                self.labels = self.box_vals[-list_len:]
            else:
                self.labels = self.box_vals[station_inx-list_len/2:station_inx+int(round(list_len/2.0))]
        except (AttributeError, ValueError):
            self.labels = self.box_vals[:list_len]

        self.populate()

    def populate(self):
        self.up_btn = Button(self, text=unichr(0x25B2), width=60)
        self.down_btn = Button(self, text=unichr(0x25BC), width=60)

        self.up_btn.bind("<Button-1>", lambda e: self.scroll(-1))
        self.down_btn.bind("<Button-1>", lambda e: self.scroll(1))

        self.up_btn.pack()
        for l in self.labels:
            options = {'text':l, 'font':("Helvetica", 24, "bold")}
            # put special color on current station
            if l.strip() == self.tkStationName.get().strip():
                options['fg'] = '#ffdb4d'
            nl = Label(self,**options)
            nl.bind("<Button-1>", lambda e: self.select_station(e))
            nl.pack()

        self.down_btn.pack()

    def select_station(self, event):
        selected_name = event.widget.cget('text')
        self.tkStationName.set(selected_name)
        print "Changed to station {0}".format(selected_name)
        self.destroy()

    def scroll(self, number):
        first_inx = self.box_vals.index(self.labels[0]) + number
        last_inx = self.box_vals.index(self.labels[-1]) + number

        if first_inx > 0 and last_inx < len(self.box_vals):
            for widget in self.winfo_children():
                widget.destroy()
            self.labels = self.box_vals[first_inx:last_inx+1]
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