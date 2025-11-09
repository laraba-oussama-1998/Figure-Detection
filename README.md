# Figure‑Detection

## Overview  
This project implements a system for detecting and segmenting figures (e.g., images, charts, diagrams) in documents or scanned material. The goal is to extract figure elements from larger pages, enabling downstream processing such as classification, OCR, or indexing.

## Tech Stack  
- Python  
- Deep learning frameworks (TensorFlow / PyTorch) – depending on your implementation  
- OpenCV / PIL for image processing  
- Data handling: pandas, numpy  
- (If applicable) OCR / text‑recognition libraries  
- (If applicable) PDF/image parsing tools  

## Features  
- Load document pages (images or PDFs) and extract figure regions.  
- Apply a trained detection model to locate figure bounding boxes.  
- Segment and save figure crops for further analysis or classification.  
- Provide inference pipeline for new documents.  
- (Optional) Generate reports of extracted figures.  

## Usage  

### 1. Clone the repository  
```bash
git clone https://github.com/laraba-oussama-1998/Figure-Detection.git
cd Figure-Detection
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare data / models  
- Ensure you have model weights under models/ or as indicated in your code. 
- (If required) Download pre‑trained model or checkpoint and place it in the appropriate folder.  
- Place input documents (images or PDFs) under data/input/ (or your chosen folder).

### 4. Run inference
```bash
python detect_figures.py --input data/input/sample_page.jpg --output data/output/
```

## 5. View Results
- Output folder should contain cropped images of detected figures.
- Optionally: A log or CSV summarizing figure bounding boxes (e.g., `output/log.csv`).

---

## Results
- Demonstrated ability to detect figure regions across a variety of document styles.
- Cropped figure images available in output for downstream tasks.
- Performance metrics (if any) can be added here, e.g., detection precision, recall, IoU averages.

---

## Future Improvements
- Extend detection to different figure types (tables, graphs, diagrams) with finer classification.
- Deploy as a web service or integrate into document-processing pipelines.
