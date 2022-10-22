from __future__ import print_function
import cv2 as cv
import pytesseract as pytesseract
from Extraction_model.preprocessing import pre_processing
from Extraction_model.contours import get_contours,drawing_contours,join_contours,\
    remove_image_drawed,merge_small_element,join_in
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\LENOVO THINKPAD X260\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

#lunch the process
def lunch_extract(source):
    image  = cv.imread(source,cv.IMREAD_COLOR)
    real_contours,cont = get_contours(pre_processing(image))
    
    
    while join_contours(real_contours)[0]:
        pass
    
    
    while merge_small_element(real_contours)[0]:
        pass
    
    
    real_contours = join_in(real_contours)
    #cv.drawContours(image, cont, -1, (0,0,255), 3)
    drawing_contours(real_contours,image,source)
    return real_contours


if __name__ == "__main__":
    remove_image_drawed()   
    #lunch_extract(r"C:\Users\LENOVO THINKPAD X260\pretraitement_pdf\text_image\aaai10_1\Image_with_content\page7.jpg")
    