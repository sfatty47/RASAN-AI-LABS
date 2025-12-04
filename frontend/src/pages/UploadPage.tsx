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
      <div className="bg-white rounded-lg shadow-sm p-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Upload Your Data</h2>
        <p className="text-gray-600 mb-8">
          Upload a CSV file to start your AutoML journey. We'll automatically process and analyze it.
        </p>

        {/* Upload Area */}
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          } ${uploading || preprocessing ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <input {...getInputProps()} />
          {uploading || preprocessing ? (
            <div className="space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <p className="text-gray-600">
                {uploading ? 'Uploading...' : 'Preprocessing...'}
              </p>
            </div>
          ) : uploadedFile ? (
            <div className="space-y-4">
              <CheckCircleIcon className="h-12 w-12 text-green-500 mx-auto" />
              <div>
                <p className="text-lg font-semibold text-gray-900">{uploadedFile.filename}</p>
                <p className="text-sm text-gray-600">
                  {uploadedFile.rows} rows × {uploadedFile.columns} columns
                </p>
                {preprocessed && (
                  <p className="text-sm text-green-600 mt-2">✓ Preprocessed successfully</p>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <CloudArrowUpIcon className="h-12 w-12 text-gray-400 mx-auto" />
              <div>
                <p className="text-lg font-medium text-gray-900">
                  {isDragActive ? 'Drop your CSV file here' : 'Drag & drop your CSV file here'}
                </p>
                <p className="text-sm text-gray-600 mt-2">
                  or click to browse (Max 10MB)
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-2">
            <XCircleIcon className="h-5 w-5 text-red-500" />
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* File Info */}
        {uploadedFile && (
          <div className="mt-6 bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">File Information</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Rows</p>
                <p className="text-lg font-semibold text-gray-900">{uploadedFile.rows.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Columns</p>
                <p className="text-lg font-semibold text-gray-900">{uploadedFile.columns}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Memory Usage</p>
                <p className="text-lg font-semibold text-gray-900">
                  {(uploadedFile.memory_usage / 1024).toFixed(2)} KB
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Column Names</p>
                <p className="text-sm font-medium text-gray-900">
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
              className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
            >
              Continue to Analysis →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

