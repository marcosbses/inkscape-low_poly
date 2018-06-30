import math
import random
def distancia_puntos(pto1,pto2):
	return math.sqrt((pto1[0]-pto2[0])**2+(pto1[1]-pto2[1])**2)

def linear_func(pto1,pto2):
	diff_x=pto2[0]-pto1[0]
	diff_y=pto2[1]-pto1[1]
	if diff_x==0:
		return {'a':float('inf'),'b':'-'+str(pto1[0])+'*inf'}
	try:
		a=float(diff_y)/diff_x
	except ZeroDivisionError:
  		a=float('inf')
	b=pto1[1]-a*pto1[0]
	return {'a':a,'b':b}

def x_intersect(lf1,lf2):
	inf=-1
	if lf1['a']==float('inf'):
		return eval(lf1['b'])
	if lf2['a']==float('inf'):
		return eval(lf2['b'])
	inf=1
	if lf1['a']==-float('inf'):
		return eval(lf1['b'])
	if lf2['a']==-float('inf'):
		return eval(lf2['b'])
	if lf1['a'] == lf2['a']:
		return float('nan')
	return (lf2['b']-lf1['b'])/(lf1['a']-lf2['a'])


def lr_side(coords,seg):
	#vertical
	if seg[0][0]==seg[1][0]:
		#hacia arriba
		if seg[0][1]>seg[1][1]:
			if coords[0]>seg[0][0]:
				return 'r'
			else:
				return 'l'
		else:
			if coords[0]>seg[0][0]:
				return 'l'
			else:
				return 'r'
	if seg[0][1]==seg[1][1]:
		#horizontal
		if seg[0][0]<seg[1][0]:
			#hacia derecha
			if coords[1]>seg[0][1]:
				return 'r'
			else:
				return 'l'
		else:
			if coords[1]>seg[0][1]:
				return 'l'
			else:
				return 'r'

	lf=linear_func(seg[0],seg[1])
	y=lf['a']*coords[0]+lf['b']
	if seg[0][0]<seg[1][0] and seg[0][1]<seg[1][1]:
		#main diag
		#print('md')
		if y>coords[1]:
			return 'l'
		if y<coords[1]:
			return 'r'

	if seg[0][0]>seg[1][0] and seg[0][1]>seg[1][1]:
		#print('md2')
		if y<coords[1]:
			return 'l'
		if y>coords[1]:
			return 'r'
	if seg[0][1]<seg[1][1] and seg[1][0]<seg[0][0]:
		#print('sd')
		if y<coords[1]:
			return 'l'
		if y>coords[1]:
			return 'r'
	if seg[0][1]>seg[1][1] and seg[1][0]>seg[0][0]:
		#print('sd2')
		if y<coords[1]:
			return 'r'
		if y>coords[1]:
			return 'l'

def box(poly):
	x_min=float('inf')
	y_min=float('inf')
	x_max=0
	y_max=0
	for seg in poly:
		p1=seg[0]
		p2=seg[1]
		if p1[0]<x_min:
			x_min=p1[0]
		if p2[0]<x_min:
			x_min=p2[0]
		if p1[1]<y_min:
			y_min=p1[1]
		if p2[1]<y_min:
			y_min=p2[1]
		if p1[0]>x_max:
			x_max=p1[0]
		if p2[0]>x_max:
			x_max=p2[0]
		if p1[1]>y_max:
			y_max=p1[1]
		if p2[1]>y_max:
			y_max=p2[1]
	return ((x_min,y_min),(x_max,y_max))

def center_coords(poly):
	cs=[((seg[0][0]+seg[1][0])/2,(seg[0][1]+seg[1][1])/2) for seg in poly]
	x=0
	y=0
	for c in cs:
		x=x+c[0]
		y=y+c[1]
	return (x/len(poly),y/len(poly))

def is_inside_polygon(coords,poly):
	box_=box(poly)
	c=center_coords(poly)
	x=coords[0]
	y=coords[1]
	if x<box_[0][0]:
		return False
	if x>box_[1][0]:
		return False
	if y<box_[0][1]:
		return False
	if y>box_[1][1]:
		return False

	for seg in poly:
		
		lr=lr_side(c,seg)
		#print('lr: '+str(lr))
		if lr_side(coords,seg)!=lr:
			return False
	return True


#<
def slope(radians):
	if radians==math.pi/2:
		return float('inf')
	if radians==-math.pi/2:
		return -float('inf')
	c=math.cos(radians)
	s=math.sin(radians)
	return s/c

def angle_of_slope(slope):
	if slope==float('inf'):
		return math.pi/2
	if slope==-float('inf'):
		return -math.pi/2
	d=math.sqrt(slope**2+1)
	dy=slope/d
	return math.asin(dy)

#<
def perpend_angle(radians):
	if radians>=0 and radians<=math.pi/2:
		return -math.pi/2+radians
	if radians<=0 and radians>=-math.pi/2:
		return math.pi/2+radians

def perpendicular_linear_function(coords0,coords1):
	lf=linear_func(coords0,coords1)
	slope_=lf['a']
	angle=angle_of_slope(slope_)
	perpend_ang=perpend_angle(angle)
	perpend_slope=slope(perpend_ang)
	mid_y=(coords0[1]+coords1[1])/2
	mid_x=(coords0[0]+coords1[0])/2
	b=mid_y-perpend_slope*mid_x
	if perpend_slope==-float('inf'):
		perpend_slope=float('inf')
	if perpend_slope==float('inf'):
		b=str(-mid_x)+'*inf'

	return {'a':perpend_slope,'b':b}

def circumcircle(pointy_triangle):
	plf1=perpendicular_linear_function(pointy_triangle[0],pointy_triangle[1])
	plf2=perpendicular_linear_function(pointy_triangle[1],pointy_triangle[2])
	x=x_intersect(plf1,plf2)
	if plf1['a']==float('inf') or plf1['a']==-float('inf'):
		y=plf2['a']*x+plf2['b']
	else:
		y=plf1['a']*x+plf1['b']
	c=(x,y)
	r=distancia_puntos(c,pointy_triangle[0])
	return (c,r)

def get_XxX_coords_inside_box(x_amount,box_):
	w=box_[1][0]-box_[0][0]
	h=box_[1][1]-box_[0][1]
	dx=w/(x_amount+1)
	dy=h/(x_amount+1)
	l=[]
	for i in range(1,x_amount+1):
		for j in range(1,x_amount+1):
			c=(box_[0][0]+dx*i,box_[0][1]+dy*j)
			l.append(c)
	return l

def get_XxX_coords_inside_poly(x_amount,poly):
	box_=box(poly)
	cs=get_XxX_coords_inside_box(x_amount,box_)
	csip=[]
	for c in cs:
		if is_inside_polygon(c,poly):
			csip.append(c)
	return csip


def extrinsic_to_intrinsic_coords(coords,intrinsic_width,intrinsic_height,extrinsic_width,extrinsic_height,anchor):
	rw=intrinsic_width/extrinsic_width
	rh=intrinsic_height/extrinsic_height
	return ((coords[0]-anchor[0])*rw,(coords[1]-anchor[1])*rh)

def intrinsic_to_extrinsic_coords(coords,intrinsic_width,intrinsic_height,extrinsic_width,extrinsic_height,anchor):
	rw=extrinsic_width/intrinsic_width
	rh=extrinsic_height/intrinsic_height
	return (anchor[0]+coords[0]*rw,anchor[1]+coords[1]*rh)

def super_triangle(coords_list):
	floor_c=coords_list[0]
	right_roof_c=coords_list[0]
	left_roof_c=coords_list[0]
	for c in coords_list:
		if c[1]>floor_c[1]:
			floor_c=c
		if c[1]-c[0]<-right_roof_c[0]+right_roof_c[1]:
			right_roof_c=c
		if c[0]+c[1]<left_roof_c[0]+left_roof_c[1]:
			left_roof_c=c

	b=right_roof_c[1]-right_roof_c[0]
	lf1={'a':1,'b':b}
	b=left_roof_c[1]+left_roof_c[0]
	lf2={'a':-1,'b':b}
	x_inter=x_intersect(lf1,lf2)
	margin=30
	c0=(x_inter,(lf1['a']*x_inter+lf1['b'])-margin)
	c1=((+b-floor_c[1])-margin,floor_c[1]+margin)
	b=right_roof_c[1]-right_roof_c[0]
	c2=((-b+floor_c[1])+margin,floor_c[1]+margin)
	return ((c0,c1),(c1,c2),(c2,c0))

def is_edge_in_pointy_triangle(edge,pointy_triangle):
	if edge[0] in pointy_triangle and edge[1] in pointy_triangle:
		return True

def is_edge_shared_in_list_of_pointy_triangle(edge,list):
	i=0
	for pointy_triangle in list:
		if is_edge_in_pointy_triangle(edge,pointy_triangle):
			i=i+1
	if i>1:
		return True
	return False 

def bowyer_watson(coords_list):
	if coords_list==[]:
		return []
	triangulation=[]
	super_triangle_=super_triangle(coords_list)
	
	super_triangle_=(super_triangle_[0][0],super_triangle_[1][0],super_triangle_[2][0])
	triangulation.append(super_triangle_)

	
	for c in coords_list:
		bad_triangles=[]
		for pointy_triangle in triangulation:
			circum=circumcircle(pointy_triangle)
			center=circum[0]
			r=circum[1]
			if distancia_puntos(c,center)<r:
				bad_triangles.append(pointy_triangle)
		poly=[]
		for pointy_triangle in bad_triangles:
			for edge in ((pointy_triangle[0],pointy_triangle[1]),(pointy_triangle[1],pointy_triangle[2]),(pointy_triangle[2],pointy_triangle[0])):
				if not is_edge_shared_in_list_of_pointy_triangle(edge,bad_triangles):
					poly.append(edge)
		for pointy_triangle in bad_triangles:
			triangulation.remove(pointy_triangle)
		for edge in poly:
			new_pointy_triangle=(edge[0],c,edge[1])
			triangulation.append(new_pointy_triangle)
			
	real_triangulation=[]
	for triangle in triangulation:
		share_super=False
		for point in triangle:
			if point in super_triangle_:
				share_super=True
		if not share_super:
			real_triangulation.append(triangle)

	return real_triangulation
