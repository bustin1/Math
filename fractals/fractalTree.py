import cmath
import random
import math
import kivy
#kivy.require('1.11.1')
from kivy.app import App
from kivy.graphics import Line
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import numpy as np

#from kivy.uix.button import Button
from kivy.graphics import InstructionGroup

Window.size = (800, 600)
origin_x = Window.width//2
origin_y = 0

'''
object to store the functionality
of creating/rotating lines
'''
class myLine(GridLayout):
    def __init__(self, **kargs):
        super(myLine, self).__init__(**kargs)

        #to remove the lines
        self.group = InstructionGroup()

        #set 2 col with 100 height
        self.cols=2
        self.row_force_default=True
        self.row_default_height=70 

        #angle slider
        self.angleSlider = Slider(min=0, max=360, value=30)
        self.add_widget(self.angleSlider)

        #label for angle slider
        self.L1 = Label(text="Angle: " + str(self.angleSlider.value))
        self.add_widget(self.L1)


        #scale slider
        self.scaleSlider = Slider(min=1, max=5, value=3)
        self.add_widget(self.scaleSlider)

        #label for the slider
        self.L2 = Label(text="Scale: " + str(self.scaleSlider.value))
        self.add_widget(self.L2)


        #ratio slider
        self.ratioSlider = Slider(min=.01, max=.8, value=.67)
        self.add_widget(self.ratioSlider)

        #label for the slider
        self.L3 = Label(text="Ratio: " + str(self.ratioSlider.value))
        self.add_widget(self.L3)


        #attach a call back
        self.angleSlider.bind(value=self.on_value1) 
        self.scaleSlider.bind(value=self.on_value2) 
        self.ratioSlider.bind(value=self.on_value3) 

        with self.canvas:
            angle = math.pi/2
            self.drawLine(origin_x, origin_y, math.pi/2, 30)

    def on_value1(self, instance, angle):
        self.L1.text = "Angle: " + str(round(angle, 2))

    def on_value2(self, instance, scale):
        self.L2.text = "Length: " + str(round(scale, 2))

    def on_value3(self, instance, ratio):
        self.L3.text = "Ratio: " + str(round(ratio, 2))

    def on_touch_up(self, touch):
        with self.canvas:
            angle = math.pi/2
            self.canvas.remove_group("test")
            self.drawLine(origin_x, origin_y, angle, 30)

#    def on_touch_move(self, touch):
#        self.on_touch_up(touch)

    def drawLine(self, start_x, start_y, angle, length):

        if length <= 1:
            return

        end_x = length * self.scaleSlider.value * math.cos(angle) + start_x
        end_y = length * self.scaleSlider.value * math.sin(angle) + start_y
        self.group.add(Line(points=[start_x,start_y,end_x,end_y], group="test"))

        length *= self.ratioSlider.value
        self.drawLine(end_x, end_y, angle-self.angleSlider.value*math.pi/180, length)
        self.drawLine(end_x, end_y, angle+self.angleSlider.value*math.pi/180, length)





class MyApp(App):

    def build(self):
        return myLine()




if __name__ == "__main__":
    MyApp().run()

'''
to draw an image, make sure to use a website to covert svg to
a list of coordinates in the form x,y if you have png or jpeg, 
convert to svg then coordinates. Use this website to convert:
https://shinao.github.io/PathToPoints/
'''









