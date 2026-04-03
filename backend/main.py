"""
FastAPI backend for AI-powered document analysis.
Handles file uploads, text extraction, and AI-powered document analysis.
"""

import os
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from utils.parser import parse_document, validate_file_type
from utils.ai_extractor import process_document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Document Analysis API",
    description="Extract and analyze documents using Mistral AI via Hugging Face",
    version="1.0.0"
)

# Configure CORS for React frontend on localhost:3000, 3001, 3002
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class AnalysisResult(BaseModel):
    """Response model for document analysis"""
    document_type: str
    key_fields: Dict[str, Any]
    summary: str
    tables: list
    original_filename: Optional[str] = None
    file_size: Optional[int] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Document Analysis API",
        "status": "running",
        "endpoints": {
            "analyze": "/analyze (POST)",
            "health": "/"
        }
    }


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_document(file: UploadFile = File(...)) -> AnalysisResult:
    """
    Analyze a document by extracting text and using Claude AI for structured parsing.
    
    Accepts:
    - PDF files
    - DOCX files
    - Image files (JPG, PNG, BMP, GIF)
    
    Returns:
    - Structured document analysis with document type, key fields, summary, and tables
    """
    
    # Validate file type
    if not validate_file_type(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Supported types: PDF, DOCX, JPG, PNG"
        )
    
    # Get file size
    file_content = await file.read()
    file_size = len(file_content)
    
    # Check file size (limit to 50MB)
    max_size = 50 * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: 50MB, got {file_size / 1024 / 1024:.2f}MB"
        )
    
    # Create temporary file to save upload
    temp_file = None
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            tmp.write(file_content)
            temp_file = tmp.name
        
        logger.info(f"Processing file: {file.filename} ({file_size} bytes)")
        
        # Extract file extension
        file_ext = os.path.splitext(file.filename)[1]
        
        # Parse document to extract text
        try:
            extracted_text, document_type_hint = parse_document(temp_file, file_ext)
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            return AnalysisResult(
                document_type="Unknown",
                key_fields={},
                summary="Failed to extract text from document",
                tables=[],
                original_filename=file.filename,
                file_size=file_size,
                error=f"Text extraction failed: {str(e)}"
            )
        
        # Check if text was extracted
        if not extracted_text or len(extracted_text.strip()) == 0:
            logger.warning(f"No text extracted from {file.filename}")
            return AnalysisResult(
                document_type="Unknown",
                key_fields={},
                summary="No text could be extracted from this document",
                tables=[],
                original_filename=file.filename,
                file_size=file_size,
                error="No extractable text found"
            )
        
        # Process with Claude AI
        try:
            analysis_result = process_document(extracted_text, document_type_hint)
            
            # Add file metadata
            analysis_result["original_filename"] = file.filename
            analysis_result["file_size"] = file_size
            
            logger.info(f"Successfully analyzed {file.filename}")
            return AnalysisResult(**analysis_result)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return AnalysisResult(
                document_type="Unknown",
                key_fields={},
                summary="Failed to analyze document with AI",
                tables=[],
                original_filename=file.filename,
                file_size=file_size,
                error=f"AI analysis failed: {str(e)}"
            )
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except Exception as e:
                logger.warning(f"Failed to delete temp file: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Run with: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
