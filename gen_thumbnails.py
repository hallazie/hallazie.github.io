from PIL import Image as im
import os

def area(x, y):
	return x * y

def run_mywork():
	img_dict = {}
	for _,_,fs in os.walk('myworks'):
		for f in fs:
			prefix = f.split('.')[0].split('-')[0]
			img = im.open('myworks/'+f)
			if prefix not in img_dict.keys():
				img_dict[prefix] = img
			else:
				if img.size[0]*img.size[1] > img_dict[prefix].size[0]*img_dict[prefix].size[1]:
					img_dict[prefix] = img
		# for f in fs:
		# 	os.remove('myworks/'+f)
		for k in img_dict.keys():
			x, y = img_dict[k].size
			if min(x, y) == x:
				t_x, t_y = 480, int(480*y/float(x))
			else:
				t_x, t_y = int(480*x/float(y)), 480
			thumb = img_dict[k].resize((t_x, t_y))
			img_dict[k].save('myworks/%s-%sx%s.jpg' % (k, x, y))
			thumb.save('myworks/%s-%sx%s.jpg' % (k, t_x, t_y))
	for _,_,fs in os.walk('myworks'):
		for f in fs:
			if 'x' not in f or '(' in f or '（' in f:
				os.remove('myworks/' + f)

def run_yml():
	pass

if __name__ == '__main__':
	run_mywork()
	run_yml()