from multiprocessing.spawn import import_main_path
import json
import os
import re
from Conversion_model import mine_text
from Conversion_model import convert2image
from Extraction_model.extract_elements import lunch_extract




def conversion():
    extract_text_images()

    #trouver les page qui ont des figures
    caption_dict = mine_text.extract_figtab_caption()
    
    figures_pages = dict()
    
    for pdf_name in caption_dict.keys():
        figures_pages[pdf_name] = []
        if caption_dict[pdf_name] != []:
            for figures in caption_dict[pdf_name]:
                
                if figures["page"] not in figures_pages[pdf_name]:
                    figures_pages[pdf_name].append(figures["page"])
        else:pass
    

    return figures_pages



#extract images with content and text from pdf file
def extract_text_images():
    pdfs = os.listdir(os.getcwd()+"\pdfs")
    source = os.getcwd()+"\pdfs\\"
    for pdf in pdfs:
        root = os.getcwd()
        destination = os.path.join(os.getcwd(),"text_image\\"+pdf.split(".")[0])
        source = os.path.join(os.getcwd(),"pdfs\\"+pdf)
        try:
            if not os.path.isdir(destination):
                os.mkdir(destination)
                os.chdir(destination)
                
                with open("text.txt","w", encoding="utf-8") as file:
                    file.write(mine_text.get_text(source))
                convert2image.convert(source,destination)
                os.chdir(root)
        
        except: pass

