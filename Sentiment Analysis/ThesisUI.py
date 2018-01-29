import os
import csv
import kivy
import json
import facebook
from kivy.config import Config

Config.set('graphics','resizable',True)
Config.set('graphics','position','custom')
Config.set('graphics','left',250)
Config.set('graphics','top',100)

from classifier import classifyNB
from kivy.app import App
from pprint import pprint
from kivy.clock import Clock
from kivy.factory import Factory
from os.path import join, exists
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from kivy.app import App

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from kivy.graphics import Color, Line, Rectangle
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas,\
                                                NavigationToolbar2Kivy

Window.size = (1000,700)

token = 'EAAB7Egkv9eUBADkz4uYTwqY1KQU4HFPtU75TW8lNk3ixCwkUNWfeIDVnjaSBeMfldynH8CIvtRg318RYxDRCYjTHuoSsm9IAJjkCnZC4bIZBmo9TaqHtZCqA1ZAcVPiCyyF5qoBPohQJ7qcNFB2ZCydczbwgFe6OMPsztHeWvBQZDZD'

graph = facebook.GraphAPI(access_token=token, version = 2.10)
# feeds = graph.request("/150922171656203/feed")
# feedList = feeds['data']

# genocide = []
# for i in range(len(feedList)):
#     if not('message' in feedList[i]):
#         genocide.append(i)

# feedList = [i for j, i in enumerate(feedList) if j not in genocide]
# test = []

# for i in range(0, len(feedList)):
#     if ('message' in feedList[i]):
#         test.append(feedList[i]['message'])

class data_cleaning:

    def function(self):
        pass

class chart(Popup):
    N = 1
    positive = 11
    negative = 11
    ind = np.arange(N)    # the x locations for the groups
    width = 0.02     # the width of the bars: can also be len(x) sequence

    fig, plt = plt.subplots()
    rects1 = plt.bar(ind, positive, width, color='#4bf3a2')

    rects2 = plt.bar(ind + width, negative, width, color='#f25454')

    # add some text for labels, title and axes ticks
    plt.set_xticklabels(ind)
    plt.set_yticks((np.arange(0, 1.1, 0.10)))
    plt.legend((rects1[0], rects2[0]), ('Postive', 'Negative'))

    canvas = fig.canvas

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    pass

class ScreenOne(Screen):
	pass

class CommentList(BoxLayout):
	def __init__(self, **kwargs):
		# print(kwargs)
		del kwargs['index']
		super(CommentList, self).__init__(**kwargs)
	comment_index = NumericProperty()
	message = StringProperty()
	created_time = StringProperty()

class PostList(BoxLayout):

    def __init__(self, **kwargs):
        # print(kwargs)
        del kwargs['index']
        super(PostList, self).__init__(**kwargs)
    post_index = NumericProperty()
    message = StringProperty()
    updated_time = StringProperty()
    id = StringProperty()

class ScreenTwo(Screen):
    #test2 = test
    data = ListProperty()
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def args_converter(self,row_index, post):
    	return {
    		'post_index': row_index,
    		'message': post['message'],
    		'id': post['id'],
    		'updated_time': post['updated_time']
    	}

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            # print(filename[0])
            testobject = classifyNB(filename[0],0.67)
            print(testobject)


        self.dismiss_popup()


class PostView(Screen):

    data2 = ListProperty()
    post_index = NumericProperty()
    message = StringProperty()
    id = StringProperty()

    def args_converter(self,row_index, comment):
        return {
            'comment_index': row_index,
            'message': comment['message'],
            'created_time': comment['created_time']
        }

    def selectChart(self):
        chart().open()

class ThesisApp(App):

    def build(self):
        self.screentwo = ScreenTwo(name='screentwo')
        self.load_post()
        self.clean()

        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.screentwo)
        return root

    def load_comments(self, post_id):
        comments = graph.request("/" + post_id + "/comments")
        commentList = comments['data']
        genocide = []

        for i in range(len(commentList)):
            if not('message' in commentList[i]):
                genocide.append(i)
                

            commentList = [i for j, i in enumerate(commentList) if j not in genocide]
            return commentList

    def goto_comments(self, post_index):
        post = self.screentwo.data[post_index]
        name = 'post{}'.format(post_index)
        self.postview = PostView(name=name, post_index=post_index, message=post['message'], id=post['id'])
        self.postview.data2 = self.load_comments(post['id'])

        # view = PostView(name=name)

        self.root.add_widget(self.postview)
        self.transition.direction = 'left'
        self.root.current = self.postview.name

    def goto_post(self):
        self.transition.direction = 'right'
        self.root.current = 'screentwo'

    def load_post(self):
        feeds = graph.request("/457692471281185/feed")
        feedList = feeds['data']
        genocide = []
        for i in range(len(feedList)):
            if not('message' in feedList[i]):
                genocide.append(i)

        feedList = [i for j, i in enumerate(feedList) if j not in genocide]
        self.screentwo.data = feedList

    def refresh_post(self):
        self.load_post()
        print("reload successful")

    def refresh_comment(self):
        self.load_comments(self.postview.id)
        print("reload successful")

    def clean(self):
        print(self.screentwo.data)


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
ThesisApp().run()