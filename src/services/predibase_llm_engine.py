import logging
import json
from predibase import PredibaseClient
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class predibase:
    def __init__(self):
        try:
            with open("/home/ubuntu/ONGRID_OCR_PREDIBASE/src/configs/config.json", "r") as f:
                config = json.load(f)

            predibase_model = config["predibase"]["model"]
            predibase_context_window = config["predibase"]["context_window"]
            predibase_temperature = config["predibase"]["temprature"]  # Note: Corrected spelling of "temperature"
            predibase_api_token = config["predibase"]["api_token"]

            self.pc = PredibaseClient(token=predibase_api_token)
            self.llm = self.pc.LLM(predibase_model)
            self.options = {
                "max_new_tokens": predibase_context_window,
                "temperature": predibase_temperature
            }

            logger.info(f"Predibase initialized with model: {predibase_model}, context window: {predibase_context_window}, temperature: {predibase_temperature}")

        except Exception as e:
            logger.error("Failed to initialize predibase: ", exc_info=True)
            raise e

    def experience_parser(self, text_file_path):
        logger.info(f"Processing file: {text_file_path}")
        try:
            with open(text_file_path, 'r') as file:
                content = file.read()
            logger.info("File content read successfully")

            result = self.llm.generate(f"""
                        <s>
            [INST]Your task is to act as a document question and answer assistant specialized in processing experience slip documents. You will be given the content of an experience or relieving letter. Extract the relevant details about the employee from the provided content and format these details as a JSON object. Specifically, identify the following information:
                {{
                "FullName": " ",
                "Employer": " ", 
                "EmployeeId": "", 
                "Designation": " ", 
                "Location": " ",
                "DateOfJoining": "",
                "LastDateOfWorking": "" 
                }}
                [/INST]
                        
                [INST]# Note: Employee ID may be referred to as EmpNo, E. No, E-Code, EmpId, employee code or like ECODE-xxx, ECode-xxx, CON-xxx.[/INST]
                [INST]# Note: Last date of working might also be mentioned as date of resignation or date of relieving.[/INST]
                [INST]# Note: convert all kind of dates in dd/mm/yy format in numbers only for eg 20 jun 2019 then 20/06/19.[/INST]
                [INST]# Note: in last designation just mention about designation not departments .[/INST]
                    
                [INST]# Note: DO NOT PROVIDE ANY EXPLANATION OR ANY NOTE BUT JUST THE JSON OBJECT[/INST]
                        </s>
                [INST]{content}[/INST]""")
            
            logger.info("Model generation completed successfully.")
            result_dict = json.loads(result.response)  # Convert string to dictionary
            return result_dict
        except Exception as e:
            logger.error("Failed to process experience slip document", exc_info=True)
            raise e
