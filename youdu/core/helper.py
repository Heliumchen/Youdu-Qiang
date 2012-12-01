import StringIO
from PIL import Image
from Image import EXTENT
from django.core.files.uploadedfile import InMemoryUploadedFile

small_poster_size = 360, 500

def get_thumbnail(file, filename):
	img_format = filename.split('.')[1]
	thumb_io = StringIO.StringIO()
	img = Image.open(file)
	img.thumbnail(small_poster_size, Image.ANTIALIAS)
	img.save(thumb_io,format='JPEG')
	thumb_file = InMemoryUploadedFile(thumb_io, None, filename, 'image/jpeg',
                                  thumb_io.len, None)
	return thumb_file

def get_profile_qrcode(profile):
	url = u'http://www.qrcn.net/api?chs=120x120&chl=MECARD:'
	chl = ''
	for item in profile.items():
		if item[1] != '':
			print item
			chl += '%s:%s;' % (item[0],item[1])
	return url+chl
	 