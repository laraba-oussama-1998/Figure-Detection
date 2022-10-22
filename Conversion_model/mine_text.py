from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import os
import sys
import re



def get_text(file_source):
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    data = list()
    i = 1
    content=""
    for page in PDFPage.get_pages(open(file_source, 'rb')):
        interpreter.process_page(page)
        #data =  retstr.getvalue().split("\n\n")
        content += retstr.getvalue().split("\n\n")[len(data)-1].split("\x0c")[1]+"\n\n" if  len(data)!= 0 else ""
        
        for sentence in retstr.getvalue().split("\n\n")[len(data):]:
            content += sentence+"\n\n"
        content +="\n\n***page"+str(i)+" finished***\n\n"
        data = retstr.getvalue().split("\n\n")
        
        i+=1
        
        #print(data)

    return content


#mining the caption of figures and table from text.txt file and images 
def extract_figtab_caption():
    source = os.path.join(os.getcwd(),"text_image")
    pdfs = os.listdir(source)
    caption_dict=dict()
    
    
    for pdf in pdfs:
        captions = list()
        caption_dict[pdf]=""
        caption = False
        content = ""
        text_file_path = os.path.join(source,pdf)
        num_page=1
        
        with open(text_file_path+r"\text.txt","r",encoding="utf-8") as file:
            for line in file.readlines():
                if caption :
                    if str(line.encode("utf-8"))[2:-1] != r"\n":
                        content += str(line.encode("utf-8"))[2:-3]
                        
                    else: 
                        caption = False
                        dic = dict()
                        dic["page"] = num_page
                        dic["caption"]= content
                        content=""
                        captions.append(dic)
                else: 
                    
                    if re.search(r"^(Figure|Fig[.]|Table) ([0-9]+|[IVX]+)(:|[.])",str(line.encode("utf-8"))[2:-3]):
                        caption = True
                        content += str(line.encode("utf-8"))[2:-3]
                    else:
                        num_page += 1 if re.match("[*]{3}page[0-9]+ finished[*]{3}",str(line.encode("utf-8"))[2:-3]) else 0
                        
        #print(type(page_dict))
        caption_dict[pdf] = captions.copy()
    #print(caption_dict)
    for pdf_name in caption_dict.keys():
        i=1
        print("********* "+pdf_name+"*********\n")
        for caption in caption_dict.get(pdf_name):
            
            print("caption : ",i,"\n")
            print(str(caption)+"\n")
            i+=1
            
    return caption_dict

""" 

if __name__ == '__main__':
    source_dir = os.path.join(os.getcwd(),"pdfs")
    destination_dir = os.path.join(os.getcwd(),"text_image")
    pdfs = os.listdir(source_dir)
    for pdf in pdfs:
        source_file = os.path.join(source_dir,pdf)
        destination_file = os.path.join(destination_dir,pdf.split(".")[0])
        with open(destination_file+r"\text.txt","w",encoding="utf-8") as text:
            text.write(Mine_text.get_text(source_file))
"""