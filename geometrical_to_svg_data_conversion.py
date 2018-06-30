

def sided_triangle_to_triangle_path_data(sided_triangle):
	cs=[]
	for side in sided_triangle:
		if not side[0] in cs:
			cs.append(side[0])
		if not side[1] in cs:
			cs.append(side[1])
	c0=cs[0]
	t1=(cs[1][0]-c0[0],cs[1][1]-c0[1])
	t2=(cs[2][0]-cs[1][0],cs[2][1]-cs[1][1])
	return 'm '+str(c0)[1:len(str(c0))-1]+' '+str(t1)[1:len(str(t1))-1]+' '+str(t2)[1:len(str(t2))-1]+' z'