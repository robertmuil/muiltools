import numpy as np
from pylab import figure, show

class PointBrowser:
	"""
	Click on a point to select and highlight it -- the data that
	generated the point will be shown in the lower axes.  Use the left and 
	and right keys to browse through the next and pervious points

	TODO: update to use screen coordinates?
	"""
	def __init__(self, ax=None,  select_callback=None,
			dbg_func=None):
		"""
		provide the ax to listen to.
		"""
		self.curr_line = 0
		self.ax=ax
		self.ax.get_figure().canvas.mpl_connect('pick_event',
				self.onpick)
		self.ax.get_figure().canvas.mpl_connect('key_press_event',
				self.onpress)
		self.select_callback=select_callback
		if dbg_func is not None:
			self.d=dbg_func
		else:
			self.d=lambda *x: None

	def onpress(self, event):
		self.d(3, 'onpress: event=({}), key=({})'.format(repr(event),
				repr(event.key)))
		if event.key not in ('left', 'right', 'up', 'down'):
			return
		if event.key in ('right', 'up'): inc = 1
		else:  inc = -1

		self.curr_line += inc

		self.curr_line = np.clip(self.curr_line, 0, len(self.ax.get_lines()))
		self.update(event)

	def onpick(self, event):
		self.d(3, 'onpick: event: {}, ind=({})'.format(repr(event),
			repr(event.ind)))

		N = len(event.ind) #can get multiple indices if clicking on multiple points
		if not N:
			return True

		# the click locations
		x = event.mouseevent.xdata
		y = event.mouseevent.ydata

		lines = self.ax.get_lines()
		self.curr_line=lines.index(event.artist)

		# tie-breaker: select closest point.
		distances = np.hypot(
				x-event.artist.get_xdata()[event.ind],
				y-event.artist.get_ydata()[event.ind])
		indmin = distances.argmin()
		self.curr_point = event.ind[indmin]

		self.update(event,x,y)

	def update(self, event, x=None, y=None):
		self.d(1, 'current linenum: {:d}'.format(self.curr_line))
		self.d(1, ' -> current pointnum: {:d}'.format(self.curr_point))
		if self.select_callback is not None:
			self.select_callback(self.curr_line, self.curr_point, event)

X = np.random.rand(100, 200)
xs = np.mean(X, axis=1)
ys = np.std(X, axis=1)

fig = figure()
ax = fig.add_subplot(211)
ax.set_title('click on point to plot time series')
line, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance
line2, = ax.plot(xs*0.99, ys, 'x', picker=5)  # 5 points tolerance
ax2 = fig.add_subplot(212)

def update_selected(linenum, pointnum, event):

	ax2.cla()
	ax2.plot(X[pointnum])

	ax2.text(0.05, 0.9, 'mu=%1.3f\nsigma=%1.3f'%(xs[pointnum], ys[pointnum]),
			 transform=ax2.transAxes, va='top')
	ax2.set_ylim(-0.5, 1.5)

	selected_text.set_text('selected: line=%d, point=%d'%(linenum, pointnum))
	fig.canvas.draw()

selected_text = ax.text(0.05, 0.95, 'selected: none',
							transform=ax.transAxes, va='top')
def dbg(l,m):
	print 'D{:d}|{}'.format(l,m)

browser = PointBrowser(
		ax,
		update_selected,
	#	dbg_func=dbg
		)

show()
