# Reference:
# https://www.blog.pythonlibrary.org/2021/02/23/drawing-shapes-on-images-with-python-and-pillow/

import math
from PIL import Image, ImageDraw

def draw_test(data,test_no):

  w, h = 1000, 1000
    
  # creating new Image object
  img = Image.new("RGB", (w, h))
    
  # create rectangleimage
  img1 = ImageDraw.Draw(img)  

  size=50                    # box dimension                                       #
  item_marker=0              # for scanning each byte of a testcase bytes sequence #

  for j in range(200):	     # y - axis pass					   #
    for i in range(10):      # x - axis pass					   #

      if item_marker>len(data)-1: 
        break                # break when no more bytes left to scan from test     #

      img1.rectangle((i*size,j*size,size+i*size,size+j*size), fill = data[item_marker], outline ="blue")
      item_marker+=1

  test_no = "{0:09d}".format(test_no)
  img.save("file_" +test_no+".png")

if __name__ == "__main__":

  f = open("tests_generated", 'r')
  lines = f.readlines()
  test_no=0

  for line in lines:

    test_no+=1
    line=line.strip()
    data=line.split(" ")

    idx=0

    for item in data:

      # generate the color code
      item=item.strip()
      item="#"+item+"0000"
      data[idx]=item
      idx+=1

    draw_test(data,test_no)
  
