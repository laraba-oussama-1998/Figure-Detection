import os 
from PIL import Image,ImageDraw
from Classification_model.model import build_and_load_model,load_image
from tensorflow.keras.models import load_model


def classification(chekpoint_file_path, contours):
    #model = build_and_load_model(chekpoint_file_path)
    model = load_model(chekpoint_file_path)
    fig_dict = contour_classification(contours,model)
    drawing(fig_dict)
    return fig_dict



def contour_classification(contours,model):
    fig_dict = dict()

    #prediction des regions génére par le module de segmentation par le module de classification
    for pages in contours.items():
        name = pages[0]
        file_path = os.path.join(os.getcwd(),"text_image",pages[0],"Image_with_content")
        fig_dict_fig = dict()
        fig_dict[name] = fig_dict_fig
        
        for page in pages[1].items():
            
            fig_dict_fig[page[0]] = list()
            image_page = Image.open(os.path.join(file_path,str(page[0])+".jpg"))
            image_page = image_page.resize((612,792))
            
            for box in page[1]:
                
                
                box[0] = int((box[0])*612/1700)
                box[1] = int((box[1])*792/2200)
                box[2] = int((box[2])*612/1700)
                box[3] = int((box[3])*792/2200)
                
                
                sub_image = image_page.crop((box[0],box[1],box[0]+box[2],box[1]+box[3]))
                
                image = load_image(sub_image)
                # the first condition to avoid noisy data like page numbers and very small pieces
                if box[2] > 15 and box[3] > 15 and box[2]*box[3] > 1000:
                    if 1-model.predict(image)[0][0]>= 0.9 :
                        print(os.path.join(file_path,str(page[0])+".jpg"))
                        print(box[2])
                        print(box[3])
                        fig_dict_fig[page[0]].append(box)
        del fig_dict_fig
    return fig_dict


#draw the boxes that has been classifies as figures
def drawing(dict):
    
    for doc in dict:
        print(doc)
        pages = os.listdir("text_image/"+doc+"/Image_with_content")
        for page in pages:
            if page.split(".")[0] in dict[doc].keys():
                image = Image.open("text_image/"+doc+"/Image_with_content/"+page)
                image = image.resize((612,792))
                img = ImageDraw.Draw(image)  
                
                for con in dict[doc][page.split(".")[0]]:
                    
                    
                    img.rectangle([(con[0], con[1]), (con[0]+con[2] , con[1]+con[3] )], outline ="red")
                image.save("text_image/"+doc+"/Image_with_content/drawed"+page)
        pass