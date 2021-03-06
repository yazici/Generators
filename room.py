import geom
from geom import vec2
from corridor import Corridor

def compare_points(p0, p1):
	result = p0.theta - p1.theta
	if (result < 0):
		return -1
	if (result > 0):
		return 1
	else:
		return 0
	
class Room(object):
	def __init__(self, centre, branches, connections):
		self.centre = centre
		self.branches = branches     # indexes of endpoints of connections this room makes with oter room (indexes end_points)
		self.connections = connections # this one is same, but indexes connections
		self.points = []             # points in polygon describing walls
		self.centre_point = None     # centre of room
		self.doors = []
		self.radius = 0
		self.floorplan = []
		
	def build_geometry(self, points):
		""" Builds the geometry for a room consisting of centre point, ad a number of corridor end points where each branch of a corridoor ends """
		length = 0
		radius = 0.0
		self.centre_point = vec2( points[self.centre].x, points[self.centre].y ) 
		for b in self.branches:
			end_point = vec2( points[b].x, points[b].y ) 
			self.points = self.points + [ end_point ]
			length = geom.line_exp_len_2d(self.centre_point, end_point)
			radius  = radius + length
		self.radius = radius / ( len(self.branches) * 2.0 )
		#print "Radius %s " % self.radius
		return

	def convert_to_polar(self, point):
		""" Convert this point to a polar coordinate (r, theta) centred on the room itself """
		# need to look this up
		point - self.centre_point
		return geom.xy_to_polar(point - self.centre_point)


	def convert_from_polar(self, point):
		""" Convert this polar pointer from polar form centred on the room to """
		return geom.polar_to_xy(point) + self.centre_point
	
	def build_floorplan(self, corridors, room_centre_points):
		""" Construct a floorplan for the room. Consists of a series of points describing a polygon around the room in polar form """
		for ci in self.connections:
			corridor = corridors[ci]
			end = corridor.connection.closest(self.centre_point, room_centre_points) # which end of the corridor is closest to this room?
			for point in corridor.door_geometry(end):
				self.floorplan += [ self.convert_to_polar(point) ]
		# sort them in radial orde
		self.floorplan.sort(compare_points)
		new_floorplan = []
		new_floorplan.append(self.floorplan[0])
		for i in range(0, len(self.floorplan) - 1):
			new_floorplan.append(vec2(self.floorplan[i].r,
					     self.floorplan[i].theta +
						  (self.floorplan[i+1].theta - self.floorplan[i].theta)  / 2))
			new_floorplan.append(self.floorplan[i+1])
		self.floorplan = new_floorplan
