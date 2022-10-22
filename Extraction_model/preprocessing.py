import cv2 as cv


def pre_processing(image):
    
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    while not cv.imwrite("gray_result.png",gray):
        pass
    
    thresh = cv.threshold(gray,240,255,cv.THRESH_BINARY_INV)[1]
    while not cv.imwrite("threshold.png",thresh):
        pass
    
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(14,5))
    dilate = cv.dilate(thresh,kernel,iterations=1)
    while not cv.imwrite("dilate1.png",dilate):
        pass
    
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(8,5))
    erode = cv.erode(dilate,kernel,iterations=1)
    
    while not cv.imwrite("erode.png",erode):
        pass
    
    
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(11,6))
    dilate = cv.dilate(erode,kernel,iterations=1)
    
    while not cv.imwrite("dilated2.png",dilate):
        pass
    
    
    return dilate