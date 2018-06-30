import re

def triangle_path_data_to_sided_triangle(path_data):
	l=re.split(' ',path_data)
	if l[0]=='M':
		s_c0=l[1]
		c0=(float(s_c0[0:s_c0.index(',')]),float(s_c0[s_c0.index(',')+1:]))
		s_c0=l[2]
		c1=(float(s_c0[0:s_c0.index(',')]),float(s_c0[s_c0.index(',')+1:]))
		s_c0=l[3]
		c2=(float(s_c0[0:s_c0.index(',')]),float(s_c0[s_c0.index(',')+1:]))
		return ((c0,c1),(c1,c2),(c2,c0))


	s_c0=l[1]

	c0=(float(s_c0[0:s_c0.index(',')]),float(s_c0[s_c0.index(',')+1:]))
	s_c0=l[2]
	c1=(float(s_c0[0:s_c0.index(',')]),float(s_c0[s_c0.index(',')+1:]))
	s_c0=l[3]
	c2=(float(s_c0[0:s_c0.index(',')]),float(s_c0[s_c0.index(',')+1:]))

	c1=(c0[0]+c1[0],c0[1]+c1[1])
	c2=(c1[0]+c2[0],c1[1]+c2[1])
	return ((c0,c1),(c1,c2),(c2,c0))
