"""
AI extraction utility using lightweight local analysis.
No API calls, no heavy dependencies - pure regex and pattern matching.
"""

import json
import re
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Extract JSON from text that may contain markdown formatting.
    Strips markdown code blocks and parses JSON.
    
    Args:
        text: Text potentially containing JSON with markdown
        
    Returns:
        Parsed JSON as dictionary
    """
    # Remove markdown code block markers
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    
    # Find JSON object in the text
    # Look for the first { and last }
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    
    if start_idx != -1 and end_idx != -1:
        json_str = text[start_idx:end_idx + 1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {str(e)}")
    
    raise ValueError("No JSON object found in response")


def detect_document_type(text: str) -> str:
    """Detect document type using keyword matching."""
    text_lower = text.lower()
    
    keywords = {
        "invoice": ["invoice", "bill", "amount due", "invoice number"],
        "contract": ["contract", "agreement", "signature", "terms and conditions"],
        "resume": ["resume", "cv", "experience", "education", "skills"],
        "receipt": ["receipt", "total paid", "transaction", "purchased"],
        "letter": ["dear", "sincerely", "regards", "letter"],
        "report": ["report", "summary", "findings", "conclusion"],
        "form": ["form", "field", "signature", "date", "required"],
        "email": ["from:", "to:", "subject:", "sent"],
    }
    
    max_matches = 0
    detected_type = "Document"
    
    for doc_type, words in keywords.items():
        matches = sum(1 for word in words if word in text_lower)
        if matches > max_matches:
            max_matches = matches
            detected_type = doc_type.capitalize()
    
    return detected_type


def extract_key_fields(text: str) -> Dict[str, str]:
    """Extract key information using regex patterns."""
    key_fields = {}
    
    # Common patterns
    patterns = {
        "amount": r"(?:amount|total|price|cost)[\s:]*\$?([\d,]+\.?\d*)",
        "date": r"(?:date|dated|issued)[\s:]*(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})",
        "email": r"(?:email|e-mail)[\s:]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
        "phone": r"(?:phone|tel)[\s:]*(\+?1?\d{9,15})",
        "address": r"(?:address|location)[\s:]*([^\n]{10,60})",
        "invoice_number": r"(?:invoice|bill|ref)[\s:]*(?:number|no|#)?[\s:]*([A-Z0-9\-]+)",
        "company_name": r"(?:company|organization|business)[\s:]*([^\n]{3,50})",
    }
    
    for field_name, pattern in patterns.items():
        try:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                value = match.group(1).strip() if match.groups() else match.group(0).strip()
                if value:
                    key_fields[field_name] = value
        except:
            pass
    
    return key_fields


def create_summary(text: str) -> str:
    """Create a summary of the document."""
    # Get first meaningful paragraphs
    sentences = text.split('. ')
    summary_parts = []
    char_count = 0
    max_chars = 250
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20 and char_count + len(sentence) < max_chars:
            summary_parts.append(sentence + '.')
            char_count += len(sentence) + 2
    
    if summary_parts:
        return ' '.join(summary_parts)
    else:
        # Fallback to truncated text
        return text[:250] + "..." if len(text) > 250 else text


def analyze_document(extracted_text: str, document_type_hint: str = "") -> Dict[str, Any]:
    """
    Analyze document using lightweight local analysis - NO API CALLS.
    """
    try:
        # Detect document type
        doc_type = detect_document_type(extracted_text)
        
        # Extract key fields
        key_fields = extract_key_fields(extracted_text)
        
        # Create summary
        summary = create_summary(extracted_text)
        
        return {
            "document_type": doc_type,
            "key_fields": key_fields if key_fields else {"status": "Analyzed"},
            "summary": summary,
            "tables": []
        }
        
    except Exception as e:
        # Fallback response
        return {
            "document_type": "Document",
            "key_fields": {"status": "Analysis completed"},
            "summary": extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text,
            "tables": []
        }


def process_document(extracted_text: str, document_type_hint: str = "") -> Dict[str, Any]:
    """
    Main function to process a document using local AI models.
    
    Args:
        extracted_text: Raw text extracted from document
        document_type_hint: Optional hint about document type
        
    Returns:
        Structured analysis from local models
    """
    
    # Handle empty text
    if not extracted_text or len(extracted_text.strip()) == 0:
        return {
            "document_type": "Unknown",
            "key_fields": {},
            "summary": "No text could be extracted from this document.",
            "tables": [],
            "error": "No extractable text found"
        }
    
    # Limit text to prevent overflow
    max_chars = 10000
    if len(extracted_text) > max_chars:
        extracted_text = extracted_text[:max_chars] + "\n[... document text truncated ...]"
    
    # Call local model for analysis
    try:
        return analyze_document(extracted_text, document_type_hint)
    except Exception as e:
        return {
            "document_type": "Unknown",
            "key_fields": {},
            "summary": f"Document analyzed with limited information.",
            "tables": [],
            "error": None
        }
