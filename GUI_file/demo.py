# coding=utf-8
# import sys
import time
import tkinter as tk
import matplotlib
import numpy as np
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
class figureInTK:
    
    def __init__(self,master,x=[],y=[]):
        self.x = x
        self.y = y
        self.master = master
        self.f = Figure(figsize=(5,4),dpi=100)
        a = self.f.add_subplot(111)
        a.plot(self.x,self.y)
        self.put()

    def put(self):
        figure = FigureCanvasTkAgg(figure=self.f,master=self.master)
        figure.draw()
        figure.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=tk.YES)
        self.figure = figure

    def plot(self,x,y):
        self.f.clear()
        a = self.f.add_subplot(111)
        a.plot(x,y)
        
    def showToolBar(self):
        toolbar = NavigationToolbar2Tk(self.figure,self.master)
        toolbar.update()


import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import sys

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.createWidgets()

    def createWidgets(self):
        fig=plt.figure(figsize=(8,8))
        ax=fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        canvas=FigureCanvasTkAgg(fig,master=root)
        canvas.get_tk_widget().grid(row=0,column=1)
        canvas.draw()

        self.plotbutton=tk.Button(master=root, text="plot", command=lambda: self.plot(canvas,ax))
        self.plotbutton.grid(row=0,column=0)

    def plot(self,canvas,ax):
        for line in sys.stdout:
            theta=line[1]
            r=line[2]
            ax.plot(theta,r,linestyle="None",maker='o')
            canvas.draw()
            ax.clear()

root=tk.Tk()
app=Application(master=root)
app.mainloop()