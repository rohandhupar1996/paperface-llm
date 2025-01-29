from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, status ,APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List
import secrets
import logging

# Assuming the following imports are available and correct
from src.services.predibase_llm_engine import predibase
from src.services.ocr import OCR, check_file_type, json_to_text

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app and security
app = FastAPI()
router = APIRouter()
security = HTTPBasic()

# Basic authentication dependency
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")
    if not (correct_username and correct_password):
        logger.warning(f"Unauthorized access attempt with username: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    logger.info(f"Authenticated user: {credentials.username}")
    return credentials.username

# Instantiate predibase service
predibase_instance = predibase()

# Dependency provider for predibase
def get_predibase():
    return predibase_instance

@router.post("/upload/")
async def upload_files(
    files: List[UploadFile] = File(...),
    parser: predibase = Depends(get_predibase),
    username: str = Depends(get_current_username)
):
    results = []
    for uploaded_file in files:
        doc_name = uploaded_file.filename
        logger.info(f"Starting to process file: {doc_name}")
        try:
            file_type = check_file_type(doc_name)
            logger.info(f"File type detected as {file_type} for file: {doc_name}")
            content = await uploaded_file.read()
            ocr_result = OCR(content, file_type)
            ocr_text = json_to_text(ocr_result)
            logger.info(f"OCR and text extraction completed for file: {doc_name}")
            final_response = parser.experience_parser("/home/ubuntu/ONGRID_OCR_PREDIBASE/output_text.txt")
            results.append({"filename": doc_name, "file_output": final_response})
            logger.info(f"File {doc_name} processed successfully with extracted data.")
        except Exception as e:
            logger.error(f"Failed to process file {doc_name}: {str(e)}", exc_info=True)
            results.append({"filename": doc_name, "message": f"Error processing file: {str(e)}"})
    return results
