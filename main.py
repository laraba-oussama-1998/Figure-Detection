from Classification_model.classification import classification
from Conversion_model.conversion_model import conversion
from Extraction_model.exractor import extraction


def begin_process():
    
    figure_pages = conversion()
    contour_dict = extraction(figure_pages)
    #checkpoint_file_path = "tmp/checkpoint"
    checkpoint_file_path = "Classification_model/models/inception_model.h5"
    fig_dict = classification(checkpoint_file_path,contour_dict)
    

if __name__ == "__main__":
    begin_process()