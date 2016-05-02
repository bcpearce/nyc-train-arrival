#!/usr/bin/python
import sys, os, traceback, datetime
from gtfs import Gtfs
from transit_util import get_stop_dict

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *

class SubwayBullet(PhotoImage):

    def __init__(self, service_name, **kwargs):
        kwargs['file'] = "img/{0}.png".format(service_name)
        PhotoImage.__init__(self, **kwargs)

class FullscreenWindow:

    def __init__(self, stop_id):
        self.stop_id = stop_id
        self.tk = Tk()

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
        
        self.add_header()
        self.update_arrivals()

    def northbound_southbound_toggle(self):
        if self.stop_id[-1] == 'N':
            self.stop_id = self.stop_id[:-1] + 'S'
        elif self.stop_id[-1] == 'S':
            self.stop_id = self.stop_id[:-1] + 'N'
        print "Switched direction {0}".format(self.stop_id)
        self.clear_old_arrivals()
        self.clear_header()
        self.add_header()
        self.print_arrivals()

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
        stops = get_stop_dict()
        stop = stops[self.stop_id[:-1]]

        direction = ""
        if self.stop_id[-1] == 'N':
            direction = "Northbound"
        if self.stop_id[-1] == 'S':
            direction = "Southbound"

        self.header = Label(self.frame,
            text=stop,
            font=("Helvetica", 40, "bold"))
        self.subheader = Label(self.frame,
            text=direction,
            font=("Helvetica", 20, "bold"))
        self.subheader.bind("<Button-1>", lambda e: self.northbound_southbound_toggle())
        self.header.pack(side=TOP)
        self.subheader.pack(side=TOP)

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

    def print_arrivals(self):
        gtfs = Gtfs(os.environ['MTA_API_KEY'])
        try:
            arrivals = gtfs.get_time_to_arrival(self.stop_id)
            arrivals.sort(key=lambda x: x[1])
        except:
            return

        self.clear_old_arrivals()

        for arrival in arrivals:
            minutes = round(float(arrival[1]/60.0))
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
                try:
                    bullet = SubwayBullet(arrival[0])
                    icon = Label(self.arrival_frame, image=bullet)
                    icon.bullet = bullet
                    
                except TclError:
                    print "Failed to use icons, falling back to text formatting"
                    if int(arrival[0][0]) in [1,2,3]:
                        bg = '#EE352E'
                    elif int(arrival[0][0]) in [4,5,6]:
                        bg = '#00933C'
                    else:
                        bg = '808183'
                    icon = Label(self.arrival_frame, 
                        text="  {0}  ".format(arrival[0]),
                        font=("Helvetica", 24), fg='white', bg=bg)

                icon.pack(side=LEFT)
                statement.pack(side=LEFT)
                
                time_str = "{0} min".format(int(minutes))
                time = Label(self.arrival_frame, text=time_str,
                    font=("Helvetica", 24))
                time.pack(side=RIGHT)

        print "Updated {0}".format(str(datetime.datetime.now()))
        

if __name__ == "__main__":

    if not os.environ.get('MTA_API_KEY'):
        with open("api_key") as f:
            os.environ['MTA_API_KEY'] = f.readline().strip()

    station = sys.argv[1]

    w = FullscreenWindow(station)
    w.tk.mainloop()
