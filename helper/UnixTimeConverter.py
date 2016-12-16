#!/usr/bin/env python

from Tkinter import Tk, Frame, Entry, Label, END, LEFT, StringVar, W, E
from datetime import date as Date, time as Time, datetime as Datetime
from calendar import timegm

ENTRYFONT = 'Courier 14'
LABELFONT = 'Arial 14'

class DateFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, padx=7, pady=7)
        self.year = StringVar()
        self.month = StringVar()
        self.day = StringVar()
        self.year.set(str(Datetime.now().year))
        self.month.set(str(Datetime.now().month))
        self.day.set(str(Datetime.now().day))
        for obj in [self.year, self.month, self.day]:
            obj.trace('w', lambda a, b, c: master.updateFromDateTime())
        for obj in [Entry(self, width=4, textvariable=self.year, font=ENTRYFONT), \
                    Label(self, text='-', font=ENTRYFONT), \
                    Entry(self, width=2, textvariable=self.month, font=ENTRYFONT), \
                    Label(self, text='-', font=ENTRYFONT), \
                    Entry(self, width=2, textvariable=self.day, font=ENTRYFONT)]:
            obj.pack(side=LEFT)
    def getDate(self):
        if self.year.get().isdigit() and self.month.get().isdigit() and \
           self.day.get().isdigit():
            return Date(int(self.year.get()), int(self.month.get()), \
                        int(self.day.get()))
        else:
            return False
    def setDate(self, date):
        self.year.set(str(date.year))
        self.month.set(str(date.month))
        self.day.set(str(date.day))

class TimeFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, padx=7, pady=7)
        self.hour = StringVar()
        self.minute = StringVar()
        self.second = StringVar()
        self.hour.set(str(Datetime.now().hour))
        self.minute.set(str(Datetime.now().minute))
        self.second.set(str(Datetime.now().second))
        for obj in [self.hour, self.minute, self.second]:
            obj.trace('w', lambda a, b, c: master.updateFromDateTime())
        for obj in [Entry(self, width=2, textvariable=self.hour, font=ENTRYFONT), \
                    Label(self, text=':', font=ENTRYFONT), \
                    Entry(self, width=2, textvariable=self.minute, font=ENTRYFONT), \
                    Label(self, text=':', font=ENTRYFONT), \
                    Entry(self, width=2, textvariable=self.second, font=ENTRYFONT)]:
            obj.pack(side=LEFT)
    def getTime(self):
        if self.hour.get().isdigit() and self.minute.get().isdigit and \
           self.second.get().isdigit():
            return Time(int(self.hour.get()), int(self.minute.get()), \
                        int(self.second.get()))
        else:
            return False
    def setTime(self, time):
        self.hour.set(str(time.hour))
        self.minute.set(str(time.minute))
        self.second.set(str(time.second))

class UnixFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, padx=7, pady=7)
        self.unix = StringVar()
        self.unix.set(str(timegm(Datetime.now().timetuple())))
        self.unix.trace('w', lambda a, b, c: master.updateFromUnix())
        Entry(self, width=10, textvariable=self.unix, font=ENTRYFONT).pack()
    def getUnix(self):
        if self.unix.get().isdigit():
            return int(self.unix.get())
        else:
            return False
    def setUnix(self, unix):
        self.unix.set(str(unix))

class UnixTimeConverter(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('UnixTimeConverter')
        self.date = DateFrame(self)
        self.time = TimeFrame(self)
        self.unix = UnixFrame(self)
        for i, obj in enumerate([self.date, self.time, self.unix]):
            obj.grid(row=i, column=1, sticky=W)
        for i, label in enumerate(['Date:', 'Time:', 'Timestamp:']):
            Label(self, text=label, padx=7, pady=7, font=LABELFONT).grid(row=i, column=0, sticky=E)
        self.mainloop()
    def updateFromDateTime(self):
        date = self.date.getDate()
        time = self.time.getTime()
        if date and time:
            self.unix.setUnix(timegm(Datetime.combine(date, time).timetuple()))
    def updateFromUnix(self):
        unix = self.unix.getUnix()
        if unix:
            datetime = Datetime.utcfromtimestamp(unix)
            self.date.setDate(datetime.date())
            self.time.setTime(datetime.time())

def main():
    UnixTimeConverter()

if __name__ == '__main__':
    main()
