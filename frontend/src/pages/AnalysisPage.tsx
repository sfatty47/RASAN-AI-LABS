import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ChartBarIcon, 
  CheckCircleIcon,
  SparklesIcon,
  InformationCircleIcon 
} from '@heroicons/react/24/outline';
import { analyzeData } from '../services/api';

export default function AnalysisPage() {
  const [analyzing, setAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fileData = localStorage.getItem('uploadedFile');
    if (fileData) {
      setUploadedFile(JSON.parse(fileData));
    } else {
      navigate('/');
    }
  }, [navigate]);

  const handleAnalyze = async () => {
    if (!uploadedFile) return;

    setError(null);
    setAnalyzing(true);

    try {
      const result = await analyzeData(uploadedFile.filename, targetColumn || undefined);
      setAnalysis(result);
      localStorage.setItem('analysisResult', JSON.stringify(result));
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleContinue = () => {
    if (analysis) {
      navigate('/training');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm p-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Data Analysis</h2>
        <p className="text-gray-600 mb-8">
          Analyze your data to understand problem type and get ML recommendations.
        </p>

        {/* Target Column Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target Column (Optional)
          </label>
          <select
            value={targetColumn}
            onChange={(e) => setTargetColumn(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={analyzing}
          >
            <option value="">Select target column...</option>
            {uploadedFile?.column_names?.map((col: string) => (
              <option key={col} value={col}>{col}</option>
            ))}
          </select>
          <p className="mt-2 text-sm text-gray-500">
            Select the column you want to predict. Leave empty for general analysis.
          </p>
        </div>

        {/* Analyze Button */}
        <button
          onClick={handleAnalyze}
          disabled={analyzing || !uploadedFile}
          className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {analyzing ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Analyzing...
            </>
          ) : (
            <>
              <SparklesIcon className="h-5 w-5" />
              Analyze Data
            </>
          )}
        </button>

        {/* Error Message */}
        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && (
          <div className="mt-8 space-y-6">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center gap-2">
              <CheckCircleIcon className="h-5 w-5 text-green-500" />
              <p className="text-sm font-medium text-green-800">Analysis Complete!</p>
            </div>

            {/* Problem Type */}
            {analysis.problem_type && (
              <div className="bg-primary-50 rounded-lg p-6">
                <div className="flex items-center gap-2 mb-4">
                  <ChartBarIcon className="h-6 w-6 text-primary-600" />
                  <h3 className="text-lg font-semibold text-gray-900">Problem Type</h3>
                </div>
                <p className="text-2xl font-bold text-primary-700">{analysis.problem_type}</p>
                {analysis.target_column && (
                  <p className="text-sm text-gray-600 mt-1">Target: {analysis.target_column}</p>
                )}
              </div>
            )}

            {/* Suitable Approaches */}
            {analysis.suitable_approaches && analysis.suitable_approaches.length > 0 && (
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended Approaches</h3>
                <div className="grid grid-cols-2 gap-3">
                  {analysis.suitable_approaches.map((approach: string, idx: number) => (
                    <div
                      key={idx}
                      className="px-4 py-2 bg-gray-50 rounded-lg text-sm font-medium text-gray-700"
                    >
                      {approach}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Data Characteristics */}
            {analysis.data_characteristics && (
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Characteristics</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Total Rows</p>
                    <p className="text-xl font-semibold text-gray-900">
                      {analysis.data_characteristics.total_rows?.toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Total Columns</p>
                    <p className="text-xl font-semibold text-gray-900">
                      {analysis.data_characteristics.total_columns}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Numerical</p>
                    <p className="text-xl font-semibold text-gray-900">
                      {analysis.data_characteristics.numerical_columns}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Categorical</p>
                    <p className="text-xl font-semibold text-gray-900">
                      {analysis.data_characteristics.categorical_columns}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Continue Button */}
            <div className="flex justify-end">
              <button
                onClick={handleContinue}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
              >
                Continue to Training →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

