#!/usr/bin/env python

import math
from cgkit.cgtypes import vec3

def r8mat_inverse_2d( mat ):
    """ R8MAT_INVERSE_2D inverts a 2 by 2 R8MAT using Cramer's rule.  """
    det = mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1]
    if ( det == 0.0 ):
        return None
    b = [ [ 0, 0 ], [ 0, 0 ] ]
    b[0][0] = mat[1][1] / det
    b[1][0] = mat[1][0] / det
    b[0][1] = mat[0][1] / det
    b[1][1] = mat[0][0] / det
    return b
 
def line_exp_perp_2d(p1, p2, p3):
    """  LINE_EXP_PERP_2D computes a line perpendicular to a line and through a point. """
    bot = math.pow( p2.x - p1.x, 2 ) + math.pow( p2.y - p1.y, 2 )
    if ( bot == 0.0 ):
        return None
    t = ( ( p1.x - p3.x ) * ( p1.x - p2.x ) 
          + ( p1.y - p3.y ) * ( p1.y - p2.y ) ) / bot
    return vec3( p1.x + t * ( p2.x - p1.x ), p2.y + t * ( p2.y - p1.y ), 1 )

def line_exp2imp_2d(point1, point2):
    """  LINE_EXP2IMP_2D converts an explicit line to implicit form in 2D. """
    assert( point1 != point2)
    return (point2.y - point1.y,
            point1.x - point2.x,
            point2.x * point1.y - point1.x * point2.y)

def lines_imp_int_2d( a1, b1, c1, a2, b2, c2 ):
    """ LINES_IMP_INT_2D determines where two implicit lines intersect in 2D. """
    if (a1 == 0.0) and (b1 == 0.0):
        return None
    elif (a2 == 0.0) and (b2 == 0.0):
        return None
    a = [ [0,0], [0,0] ]
    a[0][0] = a1
    a[1][0] = b1
    a[0][1] = a2
    a[1][1] = b2
    b = r8mat_inverse_2d(a)
    if (b != None):
        return vec3(-b[0][0] * c1 - b[1][0] * c2, -b[0][1] * c1 - b[1][1] *c2)
    else:
        return None # // or coincident
    return

def line_end_perp2d(p1, p2, w):
	""" Returns a line perpendicular to the line from p1 to p2 at the end point p1, of w length """
	dx = ( p1.x - p2.x ) 
	dy = ( p1.y - p2.y )
	l = math.sqrt( dx * dx + dy * dy)
	dx = dx / l
	dy = dy / l
	pp1 = vec3(p1.x - dy * w, p1.y + dx * w)
	pp2 = vec3(p1.x + dy * w, p1.y - dx * w)
	return (pp1, pp2)
	
def lines_exp_int_2d(p1, p2, p3, p4 ):
    """ LINES_EXP_INT_2D determines where two explicit lines intersect in 2D. """
    ival = 0
    assert(point1 != point2)
    assert(point3 != point4)
    (a1,b1,c1) = line_exp2imp_2d( point1, point2 )
    (a2,b2,c2)  = line_exp2imp_2d( point3, point4 )
    return lines_imp_int_2d( a1, b1, c1, a2, b2, c2 )

def triangle_orthocentre_2d(point1, point2, point3):
    """  TRIANGLE_ORTHOCENTER_2D computes the orthocenter of a triangle in 2D.  """

    p23 = line_exp_perp_2d( point2, point3, point1 )
    p31 = line_exp_perp_2d( point3, point1, point2 )
    p = lines_exp_int_2d( point1, p23, point2, p31 )
    return p

def atan4( y, x):
    """   ATAN4 computes the inverse tangent of the ratio Y / X. """
    if x == 0.0:
        if  ( 0.0 < y ):
            return math.pi / 2.0
        elif ( y < 0.0):    
            return 3.0 * math.pi / 2.0
        elif ( y == 0.0 ):
            return 0.0
    elif ( y == 0.0 ):
        if ( 0.0 < x ):
            return 0.0
        elif ( x < 0.0 ):
            return math.pi
    
    if (( 0.0 < x ) and ( 0.0 < y )):
        return math.atan2( y, y )
    elif (( x < 0.0 ) and ( 0.0 < y )):
        return math.pi - math.atan2( y, - x )
    elif (( x < 0.0 ) and ( y < 0.0 )):
        return ( 2.0 * math.pi - math.atan2( -y, x ))
        
    return 0.0

def angle_turn_2d( p1, p2, p3 ):
    """   ANGLE_TURN_2D computes a turning angle in 2D. """
    p = [  ( p3[0] - p2[0] ) * ( p1[0] - p2[0] ) 
         + ( p3[1] - p2[1] ) * ( p1[1] - p2[1] ),
           ( p3[0] - p2[0] ) * ( p1[1] - p2[1] ) 
         - ( p3[1] - p2[1] ) * ( p1[0] - p2[0] ) ]
    
    turn = 0.0
    if ( ( p[0] <> 0.0 ) or ( p[1] <> 0.0) ):
        turn = math.pi - atan4( p[1], [0] )
        
    return turn

def catmull_rom( p0, p1, p2, p3, t ):
	""" Retuns a point on the catmull rom spline defined by control points p0,p3, endpoints p1,p2 at interval t  """
	return  0.5 * ( (2.0 * p1) + (-p0 + p2) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t * t + (-p0 + 3.0 * p1- 3.0 * p2 + p3) * t * t * t ) 