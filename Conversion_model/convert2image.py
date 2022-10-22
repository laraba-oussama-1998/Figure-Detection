import json
import os
import re
from PIL import Image
from pdf2image import convert_from_path



def convert(file_source,destination):
    path = os.path.join(destination,"Image_with_content")
    os.mkdir(path)
    os.chdir(path)
    root = os.getcwd()
    
    images = convert_from_path(file_source)
    i=1
    for page in images:
        page.save('page'+str(i)+'.jpg', 'JPEG')
        i=i+1
        
    """image = Image.open('page1.jpg')
    return image.size"""
        
    #os.path.abspath(os.path.join(os.getcwd(), '..'))
    #os.chdir(os.getcwd()+"\images")
