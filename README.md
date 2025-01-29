# OCR LLM Experience Letter Parser

A FastAPI-based service that automates the extraction and parsing of information from experience letters and relieving letters using OCR and Large Language Models.

## Features

- **Document Processing**: Supports both PDF and image formats
- **OCR Integration**: Uses doctr for accurate text extraction
- **LLM Processing**: Leverages Predibase's Mistral-7B model for intelligent information extraction
- **Structured Output**: Returns parsed information in consistent JSON format
- **Secure API**: Includes basic authentication for API endpoints
- **Comprehensive Logging**: Built-in logging system for debugging and monitoring

## Architecture

The service follows a modular architecture:
- FastAPI for RESTful API endpoints
- Document OCR processing using doctr
- LLM-based text parsing using Predibase
- JSON response formatting

## Technical Requirements

- Python 3.8+
- CUDA-compatible GPU (for OCR processing)
- Required Python packages:
  - fastapi
  - uvicorn
  - python-multipart
  - doctr
  - predibase
  - python-jose[cryptography]

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rohandhupar1996/paperface-llm.git
cd OCR_PREDIBASE
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the application:
- Update `src/configs/config.json` with your Predibase API token and model preferences
- Modify logging configuration if needed

## Usage

1. Start the server:
```bash
python main.py
```

The server will start on `http://0.0.0.0:9001`

2. API Endpoints:

- Health Check:
```
GET /health
```

- Document Upload and Processing:
```
POST /upload/
```

3. Authentication:
- Default credentials:
  - Username: admin
  - Password: secret

## API Documentation

### POST /upload/

Upload one or more experience/relieving letters for processing.

**Request:**
- Method: POST
- Authentication: Basic Auth
- Content-Type: multipart/form-data
- Body: List of files (PDF/Images)

**Response:**
```json
[
    {
        "filename": "example.pdf",
        "file_output": {
            "FullName": "John Doe",
            "Employer": "Example Corp",
            "EmployeeId": "EMP123",
            "Designation": "Software Engineer",
            "Location": "New York",
            "DateOfJoining": "01/01/20",
            "LastDateOfWorking": "31/12/22"
        }
    }
]
```

## Error Handling

The service includes comprehensive error handling for:
- File type validation
- OCR processing errors
- LLM processing failures
- Authentication failures

## Logging

Logs are written to `app.log` and include:
- Request processing details
- OCR operation status
- LLM processing results
- Error traces for debugging

## Security Considerations

- Basic authentication required for API endpoints
- Configuration stored in separate config file
- Sensitive information should be managed through environment variables
- File type validation before processing

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
