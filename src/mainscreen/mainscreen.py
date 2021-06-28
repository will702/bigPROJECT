from kivymd.uix.screen import MDScreen
import sys
import os
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
folder = os.path.dirname(os.path.realpath(__file__))
from kivy.lang import Builder
from screen1 import Screen1
Builder.load_file(folder + '/screen1.kv')
Builder.load_file(folder+'/mainscreen.kv')


class MainScreen(MDScreen):
    pass
