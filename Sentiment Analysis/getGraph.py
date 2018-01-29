import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from kivy.app import App

import numpy as np
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas,\
                                                NavigationToolbar2Kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from matplotlib.transforms import Bbox
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle

import matplotlib.pyplot as plt


def getGraph(pos, neg):
	N = 1
	positive = pos
	negative = neg
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
	return canvas


# class MatplotlibTest(App):
#     title = 'Matplotlib Test'

#     def build(self):
#         fl = BoxLayout(orientation="vertical")
#         fl.add_widget(canvas)
#         return fl

# if __name__ == '__main__':
#     MatplotlibTest().run()
