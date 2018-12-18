from classifier.models import Img
import os
import glob
import time

test_imgs_path = r'C:\kdav490\web_dev\img_classifier\test_images'

for i in glob.glob(test_imgs_path + "\\*.jpg"):
    pic = Img(image=i)
    pic.image.save(os.path.basename(i), open(i, 'rb'))
    print("{} - Uploaded: {}".format(time.ctime(), os.path.basename(i)))