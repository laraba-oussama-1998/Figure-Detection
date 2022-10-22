import cv2 as cv
import os
import re


#create array contours that have x,y coordination and the width and height of the box
def get_contours(dilate):
    try:
        countours = cv.findContours(dilate,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        
        countours = countours[0] if len(countours) == 2 else countours[1]
        
        countours = sorted(countours,key = lambda x : cv.boundingRect(x))
        
        real_contours = list()
        for countour in countours:
            x, y, w, h = cv.boundingRect(countour)
            
            real_contours.append([x+3,y+2,w-6,h-7])
            
    except:
        real_contours = []
        countours = []
    return real_contours,countours



#this function for delete drawed box on images
def remove_image_drawed():
    source = os.path.join(os.getcwd(),"text_image")
    images_folder = os.listdir(source)
    for image_folder in images_folder:
        folder_image_with_path = os.path.join(source,image_folder,"image_with_content")
        
        folder_image_with = os.listdir(folder_image_with_path)
    
        for image in folder_image_with:
            if re.search("drawed",image):
                os.remove(os.path.join(folder_image_with_path,image))



#this function is for drawnig the boxes in the original image
def drawing_contours(real_contours,image,source):
    source_searcher = re.search(r"\\page[0-9]+[.]jpg",source)
    source,image_name = source[:source_searcher.span()[0]],source[source_searcher.span()[0]+1:]
    print(image_name)
    for final_countour in real_contours:
        x,y,w,h = final_countour

        cv.rectangle(image, (x , y) , (x+w , y+h) , (36,255,12),1) 
        
    cv.imwrite(os.path.join(source,image_name.split(".")[0]+"_drawed."+image_name.split(".")[1]),image)




#join countours that are intersect or contours that are iside other contours
def join_contours(real_contours):
    
    len_contours = len(real_contours)
    breaker = False
    changes = False
    
    for contour in real_contours:
        i = 0
        x1, y1, w1, h1 = contour 
        
        for j in range(i,len_contours):
            
            x2, y2, w2, h2 = real_contours[j]
            if  real_contours[j] is not contour:  
                breaker = False
                
                """
                x31,y31                           x32,y32


                x33,y33                          x34,y34
                """
                
                #figure out who's the box that he is in extreme left
                x31 = min(x1,x2)
                y31 = min(y1,y2)
                
                #get the width and the height of the final box (the result box of the joining)
                w3 = max(x1+w1,x2+w2)-x31
                h3 = max(y1+h1,y2+h2)-y31
                
                if join_check([x1,y1,w1,h1],[x2,y2,w2,h2],[x31,y31,w3,h3]):
                    real_contours, breaker = contour_join(real_contours,[x31,y31,w3,h3],\
                        real_contours[j],contour)
                
                if breaker : 
                    changes = True
                
                break
    
    return changes,real_contours


#checking for the intresection of the 2 box
def join_check(box1,box2,box3):
    
    x1, y1, w1, h1 =box1
    x2, y2, w2, h2 = box2
    x3, y3, _ , _ = box3
    checked = False
    
    if x3 == x1 : 
        if y3 == y1:
            #that mean that the box 1 is in extreme left and top
            #check if the first point off the box 2 is in the area of the box 1
            if (x2 >= x1 and x2 <= x1+w1) and (y2 >= y1 and y2 <= y1+h1):
                checked = True
        
        else :
            #that mean that the box 1 is in extreme left and box 2 is extreme top
            if (x2 >= x1 and x2 <= x1+w1) and (y2+h2 >= y1 and y2 <= y1) :
                checked = True
    
    else:
        if y3 == y2:
            #that mean that the box 2 is in extreme left and top
            if (x2 <= x1 and x1 <= x2+w2) and (y2 <= y1 and y1 <= y2+h2) :
                checked = True
        
        else :
            #that mean that the box 2 is in extreme left and box 1 is extreme top
            if (x2 <= x1 and x1 <= x2+w2) and (y1+h1 >= y2 and y1  <= y2) :
                checked = True
    
    return checked


# joining 2 box
def contour_join(real_contours,final_box,contour_2,contour):
    
    real_contours.append(final_box)
    real_contours.remove(contour_2)
    real_contours.remove(contour)
    
    return real_contours,True



#cette methode pour eliminé les countours qui sont dans autre contours
def join_in (contours):
    
    contours_copy = contours.copy()
    for box1 in contours_copy:
        # search the box2 that contain the box1 on it
        for box2 in contours_copy:
            
            if box2 is not box1 and box2[0]-1<=box1[0] and box2[0]+box2[2]+1>=box1[0]+box1[2] \
                and box2[1]-1<=box1[1] and box2[1]+box2[3]+1>=box1[1]+box1[3]:
                
                contours.remove(box1)
                
                break
    
    del contours_copy
    return contours


# this function is used to merge the lebels with their owen figure
def merge_small_element(contours):
    print(contours)
    changes = False
    small_contour_to_join, contours = choose_small_contours_to_merge(contours)
    
    nearest = list()
    seconde_nearest = list()
    for small_contour in small_contour_to_join:
        
        nearest, seconde_nearest = searching_the_two_nearest_contours(contours,small_contour)
        
        if nearest :
            changes = True
            # adding the small contour to the nearest contour (contour joining)
            contours = add_to_contours(contours,small_contour,nearest)
            
            # adding the small contour to the seconde nearest contour (contour joining)
            if seconde_nearest and seconde_nearest != nearest:
                contours = add_to_contours(contours,small_contour,seconde_nearest)
                contours.remove(seconde_nearest)
            
            print("nearest ",nearest)
            
            contours.remove(nearest)
            contours.remove(small_contour)
    
    return changes,contours



#choosing the contours to be merged and eliminating the extra small ones
def choose_small_contours_to_merge(contours):
    small_contour_to_join = list()
    
    for contour in contours:
        # add the small contours that is going to be merged
        if (contour[2]<60 and contour[3]<150) or (contour[3]<60 and contour[2]<150) :
            small_contour_to_join.append(contour)
            
        # eliminating extra small contours
        if contour[2]<5 or contour[3]<5:
            contours.remove(contour)
    
    return small_contour_to_join, contours


#search for the nearest and the seconde nearest contours for the small one
def searching_the_two_nearest_contours(contours, small_contour):
    nearest = list()
    seconde_nearest = list()
    min_distance_seconde_nearest = 56
    min_distance_nearest = 25 
    for contour in contours:
        
        if contour != small_contour and contour[2]>60 and contour[3]>60:
            #check if the small contours is whitin top left and top right x coordination
            if small_contour[0]>=contour[0] and small_contour[0]<=contour[0]+contour[2]:
                
                #check if the small one is above the other to calculate the distance
                if small_contour[1] < contour[1]:
                    distance = abs(contour[1]-(small_contour[1]+small_contour[3]))
                    min_distance_nearest, min_distance_seconde_nearest, nearest, seconde_nearest =\
                    updating_the_distance(distance,min_distance_nearest,min_distance_seconde_nearest,\
                        nearest,seconde_nearest,contour)
                    
                else:
                    distance =abs(small_contour[1] - (contour[1]+contour[3]))
                    min_distance_nearest, min_distance_seconde_nearest, nearest, seconde_nearest =\
                    updating_the_distance(distance,min_distance_nearest,min_distance_seconde_nearest,\
                        nearest,seconde_nearest,contour)

            #check if the small contours is whitin top left and top right x coordination
            if small_contour[1]>=contour[1] and small_contour[1]<=contour[1]+contour[3]:
                
                #check if the small one is left to the other to calculate the distance
                if small_contour[0] < contour[0]:
                    distance = abs(contour[0]-(small_contour[0]+small_contour[2]))
                    min_distance_nearest, min_distance_seconde_nearest, nearest, seconde_nearest =\
                    updating_the_distance(distance,min_distance_nearest,min_distance_seconde_nearest,\
                        nearest,seconde_nearest,contour)
                    
                else:
                    distance = abs(small_contour[0] - (contour[0]+contour[2]))
                    min_distance_nearest, min_distance_seconde_nearest, nearest, seconde_nearest =\
                    updating_the_distance(distance, min_distance_nearest,min_distance_seconde_nearest,\
                        nearest,seconde_nearest,contour)
        
    return nearest, seconde_nearest


# checking the distance and update the nearest contour if exist
def updating_the_distance(distance,dis,min_seconde,nearest,second_nearst,contour):
    
    if  distance < dis and distance > 0 :
        dis = distance
        second_nearst = nearest.copy()
        nearest = contour.copy()
    elif distance < min_seconde and distance > 0:
        min_seconde = distance
        second_nearst = contour.copy()
        
    return dis,min_seconde,nearest,second_nearst



# join elements wihtout removing theme (useful for mergin)
def add_to_contours(contours, contour1, contour2):
    
    x,y = min(contour1[0],contour2[0]),min(contour1[1],contour2[1])
    w,h = max(contour1[0]+contour1[2],contour2[0]+contour2[2])-x,\
        max(contour1[1]+contour1[3],contour2[1]+contour2[3])-y
        
    contours.append([x,y,w,h])
    print([x,y,w,h])
    return contours

