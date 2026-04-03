# 🤖 AI-Powered Document Analysis Web Application

A full-stack web application that uses **Claude AI** to intelligently extract and analyze documents. Upload a PDF, Word document, or image, and get structured insights including document type, key fields, summary, and tabular data.

**Built for:** GUVI x HCL Hackathon

---

## 📋 Features

✨ **Multi-Format Support**
- PDF files (text-based or scanned)
- Word documents (.docx)
- Images (JPG, PNG, BMP, GIF)

🧠 **AI-Powered Analysis**
- Document type detection
- Automatic extraction of key fields
- Intelligent summarization
- Table detection and extraction
- Structured JSON output

💻 **Modern UI**
- Drag-and-drop file upload
- Real-time loading state
- Beautiful responsive design
- Download results as JSON
- File metadata display

🔒 **Robust Backend**
- FastAPI server with CORS enabled
- Error handling and validation
- Large file support (up to 50MB)
- Token-aware text truncation

---

## 🛠️ Tech Stack

### Frontend
- **React 18** — UI library
- **react-dropzone** — File upload component
- **axios** — HTTP client
- **CSS3** — Modern styling with gradients and animations

### Backend
- **Python 3.8+** — Programming language
- **FastAPI** — Web framework
- **Anthropic Claude API** — AI model (claude-sonnet-4-20250514)
- **PyMuPDF** — PDF text extraction
- **pdfplumber** — Advanced PDF parsing
- **python-docx** — Word document parsing
- **Pillow** — Image processing

---

## 📦 Project Structure

```
document-ai/
├── backend/
│   ├── main.py                    # FastAPI server
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment variables template
│   └── utils/
│       ├── parser.py             # File parsing logic
│       └── ai_extractor.py       # Claude API integration
├── frontend/
│   ├── package.json              # React dependencies
│   ├── public/
│   │   └── index.html            # HTML entry point
│   └── src/
│       ├── App.js                # Main React component
│       ├── App.css               # Styling
│       └── index.js              # React DOM render
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 14+** (for frontend)
- **Anthropic API Key** (get it free from https://console.anthropic.com/)

### Step 1: Get Your Anthropic API Key

1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)

### Step 2: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create a Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your API key
# On Windows:
copy .env.example .env
# On macOS/Linux:
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
```

### Step 3: Setup Frontend

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install Node dependencies
npm install

# You're ready to run!
```

### Step 4: Run the Application

**Terminal 1 - Backend (FastAPI Server):**
```bash
cd backend
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Start the server on port 8000
python main.py
# or
uvicorn main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Terminal 2 - Frontend (React Dev Server):**
```bash
cd frontend

# Start the development server on port 3000
npm start
```

Expected output:
```
webpack compiled successfully
On Your Network: http://192.168.x.x:3000
Local: http://localhost:3000
```

### Step 5: Open in Browser

Visit **http://localhost:3000** and start uploading documents!

---

## 📖 How to Use

1. **Upload a Document**
   - Drag and drop a file onto the upload area
   - Or click to select a file
   - Supported formats: PDF, DOCX, JPG, PNG

2. **Wait for Analysis**
   - The document is sent to the backend
   - Backend extracts text using appropriate parser
   - Text is sent to Claude API for intelligent analysis
   - Results are displayed in the UI

3. **View Results**
   - **Document Information** — Type, filename, size
   - **Summary** — AI-generated overview
   - **Key Fields** — Important data extracted
   - **Tables** — Structured table data

4. **Download Results**
   - Click "Download as JSON" to save analysis results
   - Perfect for further processing or archiving

5. **Analyze Another**
   - Click "Analyze Another Document" to reset and upload a new file

---

## 🎯 Example Use Cases

### Invoice Analysis
Upload an invoice and extract:
- Vendor name, invoice number, date
- Item descriptions, quantities, amounts
- Total amount, payment terms
- Billing and shipping addresses

### Resume Parsing
Upload a resume and extract:
- Candidate name, contact information
- Education history with degrees and institutions
- Work experience with roles and duration
- Skills and certifications

### Contract Review
Upload contracts and extract:
- Contract type and parties involved
- Key dates and payment terms
- Obligations and responsibilities
- Termination clauses

### Expense Report Analysis
Upload receipts and extract:
- Merchant name and location
- Transaction date and amount
- Item descriptions
- Tax and total amounts

### Research Paper Processing
Upload academic papers and extract:
- Title, authors, abstract
- Key research questions and findings
- Methodology overview
- References and citations

---

## 📡 API Reference

### POST /analyze

**Endpoint:** `http://localhost:8000/analyze`

**Request:**
```javascript
const formData = new FormData();
formData.append('file', fileObject);

const response = await axios.post('http://localhost:8000/analyze', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

**Response:**
```json
{
  "document_type": "Invoice",
  "key_fields": {
    "invoice_number": "INV-2024-001",
    "date": "2024-01-15",
    "vendor": "Acme Corp",
    "total": "$1000.00"
  },
  "summary": "Invoice from Acme Corp dated January 15, 2024 for services rendered. Total amount due is $1000.00.",
  "tables": [
    {
      "header": ["Item", "Quantity", "Rate", "Amount"],
      "rows": [
        ["Consulting", "10", "$100", "$1000.00"]
      ]
    }
  ],
  "original_filename": "invoice.pdf",
  "file_size": 245000,
  "error": null
}
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Anthropic API Key (required)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### CORS Settings

The backend is configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`

To add more origins, edit [backend/main.py](backend/main.py):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://your-custom-domain.com"],
    ...
)
```

---

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set" Error

**Solution:** Make sure your `.env` file is in the `backend/` directory with the correct API key.

```bash
cd backend
cat .env  # Verify the file exists and has the key
```

### Backend won't start on port 8000

**Solution:** The port might be in use. Change the port in `backend/main.py`:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Use 8001 instead
```

Also update the frontend API URL in `frontend/src/App.js`:
```javascript
const API_URL = 'http://localhost:8001';
```

### "Cannot find module" in Frontend

**Solution:** Reinstall dependencies:
```bash
cd frontend
rm -rf node_modules package-lock.json  # or use: rm -r node_modules, del package-lock.json
npm install
```

### PDF text extraction returns empty

**Solution:** Some PDFs are scanned images. Try uploading the PDF as an image file instead:
1. Convert PDF to image using an online tool
2. Upload as JPG/PNG
3. Backend will use OCR (requires Tesseract installation)

### Large files timeout

**Solution:** Files are limited to 50MB. For larger files:
1. Split the document into multiple parts
2. Upload and analyze each part separately

---

## 📚 API Model Details

**Model:** `claude-sonnet-4-20250514`
- Latest Claude Sonnet model with improved reasoning
- 200K token context window
- Excellent for document analysis tasks
- Optimized for JSON output

**Token Usage:**
- Each document analysis uses approximately 1-5 tokens per character (varies by content)
- Pricing: Check Anthropic pricing page for current rates

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)

---

## 📝 License

This project is created for the GUVI x HCL Hackathon. Feel free to use, modify, and distribute as needed.

---

## 🤝 Contributing

Found a bug or have an idea? Feel free to:
1. Report issues on GitHub
2. Submit pull requests with improvements
3. Share feedback and suggestions

---

## 👥 Support

For issues or questions:
- Check the Troubleshooting section above
- Review the API Reference
- Check console logs for detailed error messages

---

**Built with ❤️ for the GUVI x HCL Hackathon**

Start uploading documents and let AI do the analysis! 🚀
