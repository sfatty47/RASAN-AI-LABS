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
      <div className="bg-dark-surface rounded-lg shadow-xl border border-dark-border p-8">
        <h2 className="text-3xl font-bold text-white mb-2">Data Analysis</h2>
        <p className="text-gray-300 mb-8">
          Analyze your data to understand problem type and get ML recommendations.
        </p>

        {/* Target Column Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Target Column (Optional)
          </label>
          <select
            value={targetColumn}
            onChange={(e) => setTargetColumn(e.target.value)}
            className="w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            disabled={analyzing}
          >
            <option value="" className="bg-dark-card">Select target column...</option>
            {uploadedFile?.column_names?.map((col: string) => (
              <option key={col} value={col} className="bg-dark-card">{col}</option>
            ))}
          </select>
          <p className="mt-2 text-sm text-gray-400">
            Select the column you want to predict. Leave empty for general analysis.
          </p>
        </div>

        {/* Analyze Button */}
        <button
          onClick={handleAnalyze}
          disabled={analyzing || !uploadedFile}
          className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg shadow-primary-600/50 hover:shadow-primary-500/50"
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
          <div className="mt-4 bg-red-900/30 border border-red-700 rounded-lg p-4">
            <p className="text-sm text-red-300">{error}</p>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && (
          <div className="mt-8 space-y-6">
            <div className="bg-green-900/30 border border-green-700 rounded-lg p-4 flex items-center gap-2">
              <CheckCircleIcon className="h-5 w-5 text-green-400" />
              <p className="text-sm font-medium text-green-300">Analysis Complete!</p>
            </div>

            {/* Problem Type */}
            {analysis.problem_type && (
              <div className="bg-primary-900/20 border border-primary-700 rounded-lg p-6">
                <div className="flex items-center gap-2 mb-4">
                  <ChartBarIcon className="h-6 w-6 text-primary-400" />
                  <h3 className="text-lg font-semibold text-white">Problem Type</h3>
                </div>
                <p className="text-2xl font-bold text-primary-400">{analysis.problem_type}</p>
                {analysis.target_column && (
                  <p className="text-sm text-gray-300 mt-1">Target: {analysis.target_column}</p>
                )}
              </div>
            )}

            {/* Suitable Approaches */}
            {analysis.suitable_approaches && analysis.suitable_approaches.length > 0 && (
              <div className="bg-dark-card border border-dark-border rounded-lg p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Recommended Approaches</h3>
                <div className="grid grid-cols-2 gap-3">
                  {analysis.suitable_approaches.map((approach: string, idx: number) => (
                    <div
                      key={idx}
                      className="px-4 py-2 bg-dark-surface border border-dark-border rounded-lg text-sm font-medium text-gray-300"
                    >
                      {approach}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* AI Insights */}
            {analysis.ai_insights && (
              <div className="bg-gradient-to-r from-primary-900/30 to-purple-900/30 border border-primary-700 rounded-lg p-6">
                <div className="flex items-center gap-2 mb-4">
                  <SparklesIcon className="h-6 w-6 text-primary-400" />
                  <h3 className="text-lg font-semibold text-white">AI-Powered Insights</h3>
                  <span className="ml-auto px-2 py-1 bg-primary-900/50 text-primary-300 text-xs font-medium rounded border border-primary-700">
                    Powered by OpenAI
                  </span>
                </div>
                <div className="prose prose-sm max-w-none">
                  <p className="text-gray-300 whitespace-pre-line">{analysis.ai_insights}</p>
                </div>
              </div>
            )}

            {/* AI Not Available Notice */}
            {analysis.ai_enabled === false && (
              <div className="bg-yellow-900/30 border border-yellow-700 rounded-lg p-4">
                <div className="flex items-start gap-2">
                  <InformationCircleIcon className="h-5 w-5 text-yellow-400 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-yellow-300">AI Insights Unavailable</p>
                    <p className="text-sm text-yellow-200 mt-1">
                      Set OPENAI_API_KEY in your environment variables to enable AI-powered insights and recommendations.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Data Characteristics */}
            {analysis.data_characteristics && (
              <div className="bg-dark-card border border-dark-border rounded-lg p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Data Characteristics</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-sm text-gray-400">Total Rows</p>
                    <p className="text-xl font-semibold text-white">
                      {analysis.data_characteristics.total_rows?.toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Total Columns</p>
                    <p className="text-xl font-semibold text-white">
                      {analysis.data_characteristics.total_columns}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Numerical</p>
                    <p className="text-xl font-semibold text-white">
                      {analysis.data_characteristics.numerical_columns}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Categorical</p>
                    <p className="text-xl font-semibold text-white">
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
                className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-500 transition-all duration-200 shadow-lg shadow-primary-600/50 hover:shadow-primary-500/50"
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
