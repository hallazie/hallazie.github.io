# coding:utf-8

from PIL import Image as im
import os

def area(x, y):
	return x * y

def run_mywork():
	img_dict = {}
	for _,_,fs in os.walk('bak'):
		for f in fs:
			print(f)
			prefix = f.split('.')[0].split('-')[0]
			img = im.open('bak/'+f)
			if prefix not in img_dict.keys():
				img_dict[prefix] = img
			else:
				if img.size[0]*img.size[1] > img_dict[prefix].size[0]*img_dict[prefix].size[1]:
					img_dict[prefix] = img
		# for f in fs:
		# 	os.remove('bak/'+f)
		for k in img_dict.keys():
			x, y = img_dict[k].size
			t_x, t_y = 640, int(640*y/float(x))
			thumb = img_dict[k].resize((t_x, t_y))
			img_dict[k].save('myworks/%s-%sx%s.jpg' % (k, x, y))
			thumb.save('myworks/%s-%sx%s.jpg' % (k, t_x, t_y))
	for _,_,fs in os.walk('bak'):
		for f in fs:
			if 'x' not in f or '(' in f or '（' in f:
				os.remove('bak/' + f)

def run_yml():
	res = []
	f_dict = {}
	res.append('picture_path: myworks')
	res.append('pictures:')
	for _,_,fs in os.walk('myworks'):
		for f in fs:
			pref = f.split('-')[0]
			if pref not in f_dict.keys():
				f_dict[pref] = [0,0]
				f_dict[pref][0] = f
			else:
				f_dict[pref][1] = f
	for k in f_dict.keys():
		if '640x' in f_dict[k][0]:
			thumb = f_dict[k][0]
			orign = f_dict[k][1]
		else:
			thumb = f_dict[k][1]
			orign = f_dict[k][0]
		res.append('- filename: %s' % k)
		res.append('  original: %s' % orign)
		res.append('  sizes:')
		res.append('  - %s' % orign)
		res.append('  - %s' % thumb)
		res.append('  thumbnail: %s' % thumb)
	with open('_data/galleries/myworks.yml', 'w') as yf:
		for line in res:
			yf.write(line+'\n')

if __name__ == '__main__':
	run_mywork()
	run_yml()
