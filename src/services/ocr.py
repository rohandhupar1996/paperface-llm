import logging
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

def check_file_type(name):
    try:
        lower_name = name.lower()
        if lower_name.__contains__('.pdf'):
            file_type = 'PDF'
        else:
            file_type = 'images'
        logging.info(f"Detected file type: {file_type}")
        return file_type
    except Exception as e:
        logging.error("Error while detecting file type", exc_info=True)
        return 'Error while detecting file type'

def OCR(file, file_type):
    try:
        model = ocr_predictor(pretrained=True).cuda()
        logging.info("OCR model loaded and configured.")
        
        if file_type == 'PDF':
            doc = DocumentFile.from_pdf(file)
        else:
            doc = DocumentFile.from_images(file)
        
        logging.info(f"Document processed as: {file_type}")
        result = model(doc)
        json_output = result.export()
        logging.info("OCR prediction executed successfully.")
        return json_output
    except Exception as e:
        logging.error("Error while executing OCR prediction", exc_info=True)
        return {'Error while executing OCR prediction, Check file type passed as images and pdf can be read by the model'}

def json_to_text(json_output):
    try:
        extracted_text = ""
        for page in json_output.get('pages', []):
            for block in page.get('blocks', []):
                for line in block.get('lines', []):
                    for word in line.get('words', []):
                        extracted_text += word.get('value', '') + " "
        
        with open('output_text.txt', 'w') as file:
            file.write(extracted_text)
        logging.info("Text extracted and written to file successfully.")
    except Exception as e:
        logging.error("An error occurred while converting JSON to text", exc_info=True)

