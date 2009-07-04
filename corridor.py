#!/usr/bin/env python

from geom import vec3
from geom import vec2
import math
import geom

class Corridor(object):
	def __init__(self, ci, p1, p2):
#		self.room_indexes = (r1, r2)
		self.end_points = (p1, p2)
		self.geometry = []
		self.ends = []
		self.corridor_index = ci
		return
	
	def make_walls_and_doors(self, width):
		line_start = self.ends[0]
		line_end   = self.ends[1]
		start_door = geom.line_end_perp2d(line_start, line_end, width) # magic number == corridor width
		end_door   = geom.line_end_perp2d(line_end, line_start, width)
		self.geometry = (  start_door[0].x, start_door[0].y, # start door
				   start_door[1].x, start_door[1].y, #				   
				    start_door[1].x, start_door[1].y, # side
				    end_door[0].x, end_door[0].y,     #

				    end_door[0].x, end_door[0].y,     # end door
				    end_door[1].x, end_door[1].y,     #
				    
				    end_door[1].x, end_door[1].y,     # side
				    start_door[0].x, start_door[0].y  ) 
		return
	
	def make_geometry(self, width):
		self.ends = [ vec2(self.end_points[0].x, self.end_points[0].y),
			      vec2(self.end_points[1].x, self.end_points[1].y) ]
		self.make_walls_and_doors(width)
		return
	
	def shorten(self, amount, end, width):
		other_end = 1-end
		old_line = self.ends[end] - self.ends[other_end]
		old_line_length = old_line.length()
		delta = old_line / old_line.length()
		self.ends[end] = self.ends[other_end] + delta * old_line_length * ( 1.0 - amount )
		self.make_walls_and_doors(width)
		return
