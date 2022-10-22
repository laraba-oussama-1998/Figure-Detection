from Extraction_model.extract_elements import lunch_extract
from Extraction_model.contours import remove_image_drawed
import os
import re
import json


    
def extraction(figures_pages):
    return extract_image_element(figures_pages)

#boxing elements in image
def extract_image_element(figure_pages):
    remove_image_drawed()
    source = os.path.join(os.getcwd(),"text_image")
    pdf_list = os.listdir(source)
    contour = dict()
    for pdf in pdf_list:
        pages = dict()
        image_with_content_path = os.path.join(source,pdf,"image_with_content")
        images = os.listdir(image_with_content_path)
        
        image_with_content = dict()
        for image in images:
            image_with_content[re.findall("[0-9]+",image.split(".")[0])[0]] = image
        for page in figure_pages[pdf]:
            pages[image_with_content[str(page)].split(".")[0]] =\
                lunch_extract(os.path.join(image_with_content_path,image_with_content[str(page)]))
        contour[pdf]=dict(pages)
    del pages
    del images
    with open("contour.json","w") as contour_file:
        json.dump(contour,contour_file,indent=2)
    

    return contour
    
    







"""
this for emphasize the functionality of our application

#detect hidden table that have the format apa which means there is no vertical lines
    def detect_hidden_table():
        with open("contour.json","r") as contour_file:
            contour_dict = json.loads(contour_file.read())
            print("*************\n\n")
            print(contour_dict)
            for doc_key in contour_dict.keys():
                doc = contour_dict.get(doc_key)
                print(doc_key+"\n")
                for page_key in doc.keys():
                    print("*********"+page_key+"*********\n")
                    page = doc.get(page_key)
                    elements = page.get("image_without_content").copy()
                    similaire = list()
                    passed = list()
                    elem = elements.copy()
                    for element in elements:
                        if element not in passed:
                            print(element)
                            passed.append(element)
                            similaire.append(element.copy())
                            
                            for element2 in elem:
                                if element is not element2 and element2 not in passed:
                                    if element[0] == element2[0] and element[2] == element2[2] and element[3] == element2[3]:
                                        
                                        for sim in similaire:
                                            if sim[0] == element2[0] and sim[2] == element2[2]:
                                                y = min(sim[1],element2[1])
                                                h = sim[1]+sim[3]-y if sim[1]+sim[3] > element2[1]+element2[3] else element2[1]+element2[3]-y
                                                sim[1],sim[3] = y,h
                                        
                                        passed.append(element2)
                                
                                
                    
                    print("length ",len(elements))
                    page.update({"image_without_content": similaire.copy()})
                    del elements
        return contour_dict


    #this function is for getting the most similaire figures and table between image with text and without it
    def search_similaire_box():
        with open ("contour.json","r") as contour_file:
            contour_dict = json.load(contour_file)
        for doc_name in contour_dict.keys():
            print(doc_name,"\n")
            for page in contour_dict.get(doc_name).keys():
                print(page,"\n")
                print("image_with_content : ",contour_dict.get(doc_name).get(page).get("image_with_content"),"\n")
                print("image_without_content : ",contour_dict.get(doc_name).get(page).get("image_without_content"),"\n\n")
        pass


"""