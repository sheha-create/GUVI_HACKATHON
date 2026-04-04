import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

function App() {
  // State management
  const [uploadedFile, setUploadedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // API endpoint - use environment variable or fall back to the hosted backend
  const API_URL = process.env.REACT_APP_API_URL || 'https://doc-analyzer-ai.onrender.com';

  // Handle file drop
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setUploadedFile(file);
      setError(null);
      // Auto-analyze on drop
      analyzeFile(file);
    }
  }, []);

  // Configure dropzone
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    multiple: false
  });

  // Analyze file with backend API
  const analyzeFile = async (file) => {
    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.error) {
        setError(`Analysis completed with warning: ${response.data.error}`);
      }

      setAnalysisResult(response.data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to analyze document';
      setError(errorMsg);
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Download results as JSON
  const downloadJSON = () => {
    if (!analysisResult) return;

    const dataToDownload = {
      ...analysisResult,
      timestamp: new Date().toISOString(),
    };

    const jsonStr = JSON.stringify(dataToDownload, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `analysis_${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Reset for new analysis
  const resetAnalysis = () => {
    setUploadedFile(null);
    setAnalysisResult(null);
    setError(null);
  };

  // Format file size
  const formatFileSize = (bytes) => {
    if (!bytes) return 'Unknown';
    const kb = bytes / 1024;
    if (kb < 1024) return `${kb.toFixed(2)} KB`;
    const mb = kb / 1024;
    return `${mb.toFixed(2)} MB`;
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>📄 AI Document Analysis</h1>
        <p>Upload a document and let AI extract structured insights</p>
      </header>

      <main className="app-main">
        {!analysisResult ? (
          // Upload Section
          <div className="upload-section">
            <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
              <input {...getInputProps()} />
              <div className="dropzone-content">
                <span className="dropzone-icon">📥</span>
                {isDragActive ? (
                  <p>Drop your document here...</p>
                ) : (
                  <>
                    <p className="dropzone-text">Drag and drop a document here, or click to select</p>
                    <p className="dropzone-subtext">Supported: PDF, DOCX, JPG, PNG</p>
                  </>
                )}
              </div>
            </div>

            {uploadedFile && (
              <div className="file-info">
                <p>📎 Selected file: <strong>{uploadedFile.name}</strong></p>
                <p>📊 Size: {formatFileSize(uploadedFile.size)}</p>
              </div>
            )}

            {loading && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Analyzing document with AI...</p>
              </div>
            )}

            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                <p>{error}</p>
              </div>
            )}
          </div>
        ) : (
          // Results Section
          <div className="results-section">
            <div className="results-header">
              <h2>✅ Analysis Complete</h2>
              <button className="btn-reset" onClick={resetAnalysis}>
                Analyze Another Document
              </button>
            </div>

            {/* File Info */}
            <div className="result-card file-info-card">
              <h3>📄 Document Information</h3>
              <div className="info-grid">
                <div>
                  <span className="info-label">Filename:</span>
                  <span className="info-value">{analysisResult.original_filename}</span>
                </div>
                <div>
                  <span className="info-label">Type:</span>
                  <span className="info-value">{analysisResult.document_type}</span>
                </div>
                <div>
                  <span className="info-label">Size:</span>
                  <span className="info-value">{formatFileSize(analysisResult.file_size)}</span>
                </div>
              </div>
            </div>

            {/* Summary */}
            <div className="result-card">
              <div className="card-header">
                <h3>📝 Summary</h3>
              </div>
              <p className="summary-text">{analysisResult.summary}</p>
            </div>

            {/* Key Fields */}
            {analysisResult.key_fields && Object.keys(analysisResult.key_fields).length > 0 && (
              <div className="result-card">
                <div className="card-header">
                  <h3>🔑 Key Fields</h3>
                </div>
                <div className="fields-grid">
                  {Object.entries(analysisResult.key_fields).map(([key, value]) => (
                    <div key={key} className="field-item">
                      <span className="field-label">{key}:</span>
                      <span className="field-value">
                        {value !== null ? String(value) : 'N/A'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Tables */}
            {analysisResult.tables && analysisResult.tables.length > 0 && (
              <div className="result-card">
                <div className="card-header">
                  <h3>📊 Tables</h3>
                </div>
                {analysisResult.tables.map((table, idx) => (
                  <div key={idx} className="table-container">
                    <table className="data-table">
                      <thead>
                        <tr>
                          {table.header && table.header.map((col, colIdx) => (
                            <th key={colIdx}>{col}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {table.rows && table.rows.map((row, rowIdx) => (
                          <tr key={rowIdx}>
                            {row.map((cell, cellIdx) => (
                              <td key={cellIdx}>{cell}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ))}
              </div>
            )}

            {/* Error in Analysis */}
            {analysisResult.error && (
              <div className="result-card warning-card">
                <h3>⚠️ Notice</h3>
                <p>{analysisResult.error}</p>
              </div>
            )}

            {/* Download Button */}
            <div className="actions-footer">
              <button className="btn-download" onClick={downloadJSON}>
                ⬇️ Download as JSON
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
