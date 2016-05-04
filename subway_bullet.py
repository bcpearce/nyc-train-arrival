import sys

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *

class SubwayBullet(PhotoImage):

    def __init__(self, service_name, **kwargs):
        kwargs['file'] = "img/{0}.png".format(service_name)
        PhotoImage.__init__(self, **kwargs)