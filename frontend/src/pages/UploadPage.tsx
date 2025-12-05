import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import { 
  CloudArrowUpIcon, 
  DocumentIcon,
  CheckCircleIcon,
  XCircleIcon 
} from '@heroicons/react/24/outline';
import { uploadFile, preprocessData } from '../services/api';

export default function UploadPage() {
  const [uploading, setUploading] = useState(false);
  const [preprocessing, setPreprocessing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<any>(null);
  const [preprocessed, setPreprocessed] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setError(null);
    setUploading(true);

    try {
      const result = await uploadFile(file);
      setUploadedFile(result);
      localStorage.setItem('uploadedFile', JSON.stringify(result));
      
      // Auto-preprocess
      setPreprocessing(true);
      const preprocessResult = await preprocessData(result.filename);
      setPreprocessed(true);
      localStorage.setItem('preprocessedData', JSON.stringify(preprocessResult));
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
    } finally {
      setUploading(false);
      setPreprocessing(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    maxFiles: 1,
    disabled: uploading || preprocessing,
  });

  const handleContinue = () => {
    if (uploadedFile) {
      navigate('/analysis');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-dark-surface rounded-lg shadow-xl border border-dark-border p-8">
        <h2 className="text-3xl font-bold text-white mb-2">Upload Your Data</h2>
        <p className="text-gray-300 mb-8">
          Upload a CSV file to start your AutoML journey. We'll automatically process and analyze it.
        </p>

        {/* Upload Area */}
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all duration-200 ${
            isDragActive
              ? 'border-primary-500 bg-primary-900/20 shadow-lg shadow-primary-500/20'
              : 'border-dark-border hover:border-primary-400 hover:bg-dark-hover'
          } ${uploading || preprocessing ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <input {...getInputProps()} />
          {uploading || preprocessing ? (
            <div className="space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-400 mx-auto"></div>
              <p className="text-gray-300">
                {uploading ? 'Uploading...' : 'Preprocessing...'}
              </p>
            </div>
          ) : uploadedFile ? (
            <div className="space-y-4">
              <CheckCircleIcon className="h-12 w-12 text-green-400 mx-auto" />
              <div>
                <p className="text-lg font-semibold text-white">{uploadedFile.filename}</p>
                <p className="text-sm text-gray-300">
                  {uploadedFile.rows} rows × {uploadedFile.columns} columns
                </p>
                {preprocessed && (
                  <p className="text-sm text-green-400 mt-2">✓ Preprocessed successfully</p>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <CloudArrowUpIcon className="h-12 w-12 text-gray-400 mx-auto" />
              <div>
                <p className="text-lg font-medium text-white">
                  {isDragActive ? 'Drop your CSV file here' : 'Drag & drop your CSV file here'}
                </p>
                <p className="text-sm text-gray-400 mt-2">
                  or click to browse (Max 10MB)
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-4 bg-red-900/30 border border-red-700 rounded-lg p-4 flex items-center gap-2">
            <XCircleIcon className="h-5 w-5 text-red-400" />
            <p className="text-sm text-red-300">{error}</p>
          </div>
        )}

        {/* File Info */}
        {uploadedFile && (
          <div className="mt-6 bg-dark-card rounded-lg p-6 border border-dark-border">
            <h3 className="text-lg font-semibold text-white mb-4">File Information</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-400">Rows</p>
                <p className="text-lg font-semibold text-white">{uploadedFile.rows.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Columns</p>
                <p className="text-lg font-semibold text-white">{uploadedFile.columns}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Memory Usage</p>
                <p className="text-lg font-semibold text-white">
                  {(uploadedFile.memory_usage / 1024).toFixed(2)} KB
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Column Names</p>
                <p className="text-sm font-medium text-gray-300">
                  {uploadedFile.column_names.slice(0, 3).join(', ')}
                  {uploadedFile.column_names.length > 3 && '...'}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Continue Button */}
        {uploadedFile && preprocessed && (
          <div className="mt-6 flex justify-end">
            <button
              onClick={handleContinue}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-500 transition-all duration-200 shadow-lg shadow-primary-600/50 hover:shadow-primary-500/50"
            >
              Continue to Analysis →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

