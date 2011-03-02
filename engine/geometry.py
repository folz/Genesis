'''
Created on Jun 22, 2010

@author: catapult
'''

import math, pygame

class Vector:

	def __init__( self, x=0.0, y=0.0 ):
		self.x, self.y = x, y

	def __repr__( self ):
		return "Vector(%s, %s)" % ( self.x, self.y )

	def copy( self ):
		return Vector( self.x, self.y )

	def dot( self, other ):
		return self.x * other.x + self.y * other.y

	def __add__( self, other ):
		return Vector( self.x + other.x, self.y + other.y )

	def __neg__( self ):
		return Vector( -self.x, -self.y )

	def __sub__( self, other ):
		return - other + self

	def __mul__( self, scalar ):
		return Vector( self.x * scalar, self.y * scalar )

	__rmul__ = __mul__
	
	def __div__( self, scalar ):
		return 1.0 / scalar * self

	def angle( self ):
		return math.degrees( math.atan2( self.y, self.x ) )

	def rotate( self, ang ):
		ang = self.angle() + ang
		mag = self.magnitude()
		x = math.cos( math.radians( ang ) ) * mag
		y = math.sin( math.radians( ang ) ) * mag
		return Vector( x, y )

	def magnitude( self ):
		return math.sqrt( self.x * self.x + self.y * self.y )

	def normalize( self ):
		if self.magnitude() != 0.0:
			inverse_magnitude = 1.0 / self.magnitude()
			return Vector( self.x * inverse_magnitude, self.y * inverse_magnitude )
		else: return Vector( 0, 0 )

	def perpendicular( self ):
		return Vector( -self.y, self.x )

class Projection:

	def __init__( self, min, max ):
		self.min, self.max = min, max

	def intersection( self, other ):
		if self.max > other.min and other.max > self.min:
			return self.max - other.min
		return 0

class Polygon:

	def __init__( self, points, pos=( 0, 0 ) ):
		if type( pos ) in [type( () ), type( [] )]:
			self.pos = Vector( pos[0], pos[1] )
		elif isinstance( pos, Vector ):
			self.pos = pos
		else:
			self.points = []
		self.points = []
		self.realPoints = []
		for p in points:
			self.points.append( Vector( *p ) )
			self.realPoints.append( ( p ) )

		self.edges = []
		self.isAbove = False
		for i in range( len( self.points ) ):
			point = self.points[i]
			next_point = self.points[( i + 1 ) % len( self.points )]
			self.edges.append( next_point - point )

	def __getitem__( self, i ):
		return self.points[i]

	def __iter__( self ):
		return iter( self.points )

	def get_points( self ):
		new_points = []
		for point in self.points:
			p = point.copy()
			p.x += self.pos.x
			p.y += self.pos.y
			new_points.append( ( p.x, p.y ) )
		return new_points

	def project_to_axis( self, axis ):
		projected_points = []
		for point in self.points:
			p = point.copy()
			p.x += self.pos.x
			p.y += self.pos.y
			projected_points.append( p.dot( axis ) )
		return Projection( min( projected_points ), max( projected_points ) )

	def intersects( self, other ):
		edges = []
		edges.extend( self.edges )
		edges.extend( other.edges )

		projections = []
		for edge in edges:
			axis = edge.normalize().perpendicular()

			self_projection = self.project_to_axis( axis )
			other_projection = other.project_to_axis( axis )
			intersection1 = self_projection.intersection( other_projection )
			intersection2 = -other_projection.intersection( self_projection )
			if not intersection1:
				return False

			proj_vector1 = Vector( axis.x * intersection1, axis.y * intersection1 )
			proj_vector2 = Vector( axis.x * intersection2, axis.y * intersection2 )
			projections.append( proj_vector1 )
			projections.append( proj_vector2 )

		mtd = -self.find_mtd( projections )

		return mtd

	def collide( self, other ):
		mtd = self.intersects( other )
		if mtd:
			if mtd.x > 0:
				mtd.x += 1
				self.isLeft = False
			elif mtd.x < 0:
				mtd.x -= 1
				self.isLeft = True
			else:
				self.isLeft = None
			if mtd.y < 0:
				mtd.y -= 1
				self.isAbove = True
			elif mtd.y > 0:
				mtd.y += 1
				self.isAbove = False
			else:
				self.isAbove = None
			if math.fabs( mtd.x ) < 25: self.update_pos( mtd )
			return mtd
		return False

	def move( self, amount ):
		self.pos += amount
		temp = []
		for p in self.realPoints:
			p = ( p[0] + amount.x, p[1] + amount.y )
			temp.append( p )
		self.realPoints = temp

	def update_pos( self, mtd ):
		self.pos += mtd
		temp = []
		for p in self.realPoints:
			p = ( p[0] + mtd.x, p[1] + mtd.y )
			temp.append( p )
		self.realPoints = temp

	def find_mtd( self, push_vectors ):
		mtd = push_vectors[0]
		mind2 = push_vectors[0].dot( push_vectors[0] )
		for vector in push_vectors[1:]:
			d2 = vector.dot( vector )
			if d2 < mind2:
				mind2 = d2
				mtd = vector
		return mtd

class Line( Polygon ):
	def __init__( self, points, pos=( 0, 0 ) ):
		Polygon.__init__( self, points, pos )

class Rect( Polygon ):

	def __init__( self, x, y, w, h ):
		points = [( 0, 0 ), ( w, 0 ), ( w, h ), ( 0, h )]
		Polygon.__init__( self, points, ( x, y ) )
		self.realPoints = [( x, y ), ( x + w, y ), ( x + w, y + h ), ( x, y + h )]
		self.x = x
		self.y = y
		self.width = w
		self.height = h

	def __repr__( self ):
		return "Rect (%d, %d), (%d, %d)" % ( self.realPoints[0][0], self.realPoints[0][1], self.realPoints[1][0], self.realPoints[2][1] )

class GameBox( Rect ):

	def __init__( self, x, y, w, h, vel ):
		Rect.__init__( self, x, y, w, h )
		self.vel = vel
		self.x = x
		self.y = y

	def update( self ):
		self.move( self.vel )

class Slope( Line ):
	'''
	A Slope is a Line that you can collide with
	'''

	def __init__( self, points ):
		Line.__init__( self, points, ( 0, 0 ) )

	def __repr__( self ):
		return "Slope (%d, %d); (%d, %d)" % ( self.realPoints[0][0], self.realPoints[0][1], self.realPoints[1][0], self.realPoints[1][1] )

	def debug( self ):
		pygame.draw.line( self.world, ( 255, 255, 255 ), self.realPoints[0], self.realPoints[1] )

	def set_world_callback( self, world ):
		self.world = world

class Terrain( Polygon ):
	'''
	A Terrain is a Polygon that you can collide with
	'''

	def __init__( self, points, world ):
		Polygon.__init__( self, points, ( 0, 0 ) )
		self.world = world
		self.location = Vector( points[0][0], points[0][1] )
		self.width = abs( points[0][0] - points[1][0] )
		self.height = abs( points[0][1] - points[2][1] )

	def debug( self ):
		if not self.is_on_screen(): return
		pygame.draw.polygon( self.world, ( 255, 255, 255 ), self.realPoints )

	def set_world_callback( self, world ):
		self.world = world

	def is_on_screen( self ):
		return self.location.x + self.width >= self.world.viewport.get_x_coord() and self.location.x <= self.world.viewport.get_x_coord() + self.world.get_width() and self.location.y + self.height >= self.world.viewport.get_y_coord() and self.location.y <= self.world.viewport.get_y_coord() + self.world.get_height()
