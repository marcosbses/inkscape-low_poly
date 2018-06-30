#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
from simplestyle import *

from base64 import decodestring
import StringIO
from PIL import Image
import geometria
from svg_data_to_geometrical_conversion import triangle_path_data_to_sided_triangle
from geometrical_to_svg_data_conversion import sided_triangle_to_triangle_path_data

class HelloWorldEffect(inkex.Effect):
	"""
	Example Inkscape effect extension.
	Creates a new layer with a "Hello World!" text centered in the middle of the document.
	"""
	def __init__(self):
		"""
		Constructor.
		Defines the "--what" option of a script.
		"""
		# Call the base class constructor.
		inkex.Effect.__init__(self)

		# Define string option "--what" with "-w" shortcut and default value "World".
		self.OptionParser.add_option('-w', '--what', action = 'store',type = 'string', dest = 'what', default = 'World',help = 'What would you like to greet?')

	def get_crgb_list(self,image,width,height,anchor):
		w,h=image.size
		w2=w/10
		h2=h/10
		rw=float(width)/w
		rh=float(height)/h
		rgb_image=image.convert('RGB')
		crgbs=[]
		for x in range(w2):
			for y in range(h2):
				crgbs.append(((int(anchor[0])+int((x*10)*rw),int(anchor[1])+int((y*10)*rh)),rgb_image.getpixel((x*10,y*10))))
		return crgbs

	#extrinsic_width is extrinsic width of image
	def get_list_of_crgb_inside_triangle(self,rgb_image,triangle,extrinsic_width,extrinsic_height,anchor):
		cs=geometria.get_XxX_coords_inside_poly(5,triangle)
		crgbs=[]
		w,h=rgb_image.size
		for c in cs:
			c2=geometria.extrinsic_to_intrinsic_coords(c,w,h,extrinsic_width,extrinsic_height,anchor)
			crgbs.append((c,rgb_image.getpixel(c2)))
		return crgbs

	def average_rgb_from_crgbs(self,crgbs):
		rgb=(0,0,0)
		for crgb in crgbs:
			rgb=(rgb[0]+crgb[1][0],rgb[1]+crgb[1][1],rgb[2]+crgb[1][2])
		len_=len(crgbs)
		if len_==0:
			return (255,0,0)
		return (rgb[0]/len_,rgb[1]/len_,rgb[2]/len_)

	def average_rgb_in_triangle(self,rgb_image,triangle,extrinsic_width,extrinsic_height,anchor):
		crgbs=self.get_list_of_crgb_inside_triangle(rgb_image,triangle,extrinsic_width,extrinsic_height,anchor)
		return self.average_rgb_from_crgbs(crgbs)

	def get_list_of_coords_from_selected_circles(self):
		#first_node=self.selected[self.options.ids[0]]
		lista=[]
		for id_ in self.options.ids:
			element=self.selected[id_]
			if element.tag=='{http://www.w3.org/2000/svg}circle' or element.tag=='{http://www.w3.org/2000/svg}ellipse':
				x=float(element.get('cx'))
				y=float(element.get('cy'))
				lista.append((x,y))
		return lista

	def make_triangle(self,pointy_triangle,rgb,svg):
		rgb_hex="#%02x%02x%02x" % (rgb[0],rgb[1],rgb[2])

		sided_triangle=((pointy_triangle[0],pointy_triangle[1]),(pointy_triangle[1],pointy_triangle[2]),(pointy_triangle[2],pointy_triangle[0]))
		path_data=sided_triangle_to_triangle_path_data(sided_triangle)
		path_element = inkex.etree.SubElement(svg, 'path')
		path_element.set('d',path_data)
		style = {'opacity':1,'fill':rgb_hex,'fill-opacity':1,'fill-rule':'evenodd','stroke':'#64667a','stroke-width':0,'stroke-linecap':'round','stroke-linejoin':'miter','stroke-miterlimit':4,'stroke-dasharray':'none','stroke-opacity':1}
		path_element.set('style', formatStyle(style))

	


	def effect(self):
		"""
		Effect behaviour.
		Overrides base class' method and inserts "Hello World" text into SVG document.
		"""
		
		svg = self.document.getroot()
		

		coords_list=self.get_list_of_coords_from_selected_circles()

		image_element=svg.find('.//{http://www.w3.org/2000/svg}image')
		image_string=image_element.get('{http://www.w3.org/1999/xlink}href')
		#find comma position
		i=0
		while i<40:
			if image_string[i]==',':
				break
			i=i+1
		image_string=image_string[i+1:len(image_string)]
		decoded_image_data=decodestring(image_string)
		image = Image.open(StringIO.StringIO(decoded_image_data))
		rgb_image=image.convert('RGB')

		extrinsic_image_width=float(image_element.get('width'))
		extrinsic_image_height=float(image_element.get('height'))
		anchor_x=float(image_element.get('x'))
		anchor_y=float(image_element.get('y'))
		rgb_image=image.convert('RGB')
		anchor=(anchor_x,anchor_y)

		triangulation=geometria.bowyer_watson(coords_list)
		for pointy_triangle in triangulation:
			sided_triangle=((pointy_triangle[0],pointy_triangle[1]),(pointy_triangle[1],pointy_triangle[2]),(pointy_triangle[2],pointy_triangle[0]))
			try:
				rgb=self.average_rgb_in_triangle(rgb_image,sided_triangle,extrinsic_image_width,extrinsic_image_height,anchor)
				self.make_triangle(pointy_triangle,rgb,svg)
			except IndexError:
				pass
		


# Create effect instance and apply it.
effect = HelloWorldEffect()
effect.affect()