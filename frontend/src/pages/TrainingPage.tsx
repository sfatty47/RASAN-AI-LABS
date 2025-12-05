import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  CpuChipIcon, 
  CheckCircleIcon,
  ArrowPathIcon 
} from '@heroicons/react/24/outline';
import { trainModel } from '../services/api';

export default function TrainingPage() {
  const [training, setTraining] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<any>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [problemType, setProblemType] = useState('Regression');
  const navigate = useNavigate();

  useEffect(() => {
    const fileData = localStorage.getItem('uploadedFile');
    const analysisData = localStorage.getItem('analysisResult');
    
    if (fileData) {
      setUploadedFile(JSON.parse(fileData));
    } else {
      navigate('/');
      return;
    }

    if (analysisData) {
      const analysis = JSON.parse(analysisData);
      setAnalysis(analysis);
      if (analysis.problem_type) {
        setProblemType(analysis.problem_type);
      }
      if (analysis.target_column) {
        setTargetColumn(analysis.target_column);
      }
    }
  }, [navigate]);

  const handleTrain = async () => {
    if (!uploadedFile || !targetColumn) {
      setError('Please select a target column');
      return;
    }

    setError(null);
    setTraining(true);

    try {
      const preprocessedFile = localStorage.getItem('preprocessedData');
      const filename = preprocessedFile 
        ? JSON.parse(preprocessedFile).preprocessed_path.split('/').pop() || uploadedFile.filename
        : uploadedFile.filename;

      const trainResult = await trainModel({
        filename: filename,
        target: targetColumn,
        problem_type: problemType,
      });

      setResult(trainResult);
      // Store target column with training result for visualizations
      const trainingResultWithTarget = {
        ...trainResult,
        target_column: targetColumn,
      };
      localStorage.setItem('trainingResult', JSON.stringify(trainingResultWithTarget));
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Training failed');
    } finally {
      setTraining(false);
    }
  };

  const handleContinue = () => {
    if (result) {
      navigate('/results');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-dark-surface rounded-lg shadow-xl border border-dark-border p-8">
        <h2 className="text-3xl font-bold text-white mb-2">Train Model</h2>
        <p className="text-gray-300 mb-8">
          Train your ML model with automated hyperparameter tuning.
        </p>

        {/* Training Configuration */}
        <div className="space-y-6 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Target Column *
            </label>
            <select
              value={targetColumn}
              onChange={(e) => setTargetColumn(e.target.value)}
              className="w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
              disabled={training}
            >
              <option value="" className="bg-dark-card">Select target column...</option>
              {uploadedFile?.column_names?.map((col: string) => (
                <option key={col} value={col} className="bg-dark-card">{col}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Problem Type *
            </label>
            <select
              value={problemType}
              onChange={(e) => setProblemType(e.target.value)}
              className="w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
              disabled={training}
            >
              <option value="Regression" className="bg-dark-card">Regression</option>
              <option value="Binary Classification" className="bg-dark-card">Binary Classification</option>
              <option value="Multi-class Classification" className="bg-dark-card">Multi-class Classification</option>
            </select>
          </div>
        </div>

        {/* Train Button */}
        <button
          onClick={handleTrain}
          disabled={training || !targetColumn || !uploadedFile}
          className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg shadow-primary-600/50 hover:shadow-primary-500/50"
        >
          {training ? (
            <>
              <ArrowPathIcon className="h-5 w-5 animate-spin" />
              Training Model... This may take a few minutes
            </>
          ) : (
            <>
              <CpuChipIcon className="h-5 w-5" />
              Train Model
            </>
          )}
        </button>

        {/* Error Message */}
        {error && (
          <div className="mt-4 bg-red-900/30 border border-red-700 rounded-lg p-4">
            <p className="text-sm text-red-300">{error}</p>
          </div>
        )}

        {/* Training Progress */}
        {training && (
          <div className="mt-6 bg-blue-900/30 border border-blue-700 rounded-lg p-6">
            <div className="flex items-center gap-3">
              <ArrowPathIcon className="h-6 w-6 text-blue-400 animate-spin" />
              <div>
                <p className="font-medium text-blue-300">Training in progress...</p>
                <p className="text-sm text-blue-200 mt-1">
                  Our AI is finding the best model and tuning hyperparameters. This may take a few minutes.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Training Results */}
        {result && (
          <div className="mt-8 space-y-6">
            <div className="bg-green-900/30 border border-green-700 rounded-lg p-4 flex items-center gap-2">
              <CheckCircleIcon className="h-5 w-5 text-green-400" />
              <p className="text-sm font-medium text-green-300">Training Complete!</p>
            </div>

            <div className="bg-dark-card border border-dark-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Training Summary</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-400">Model ID</p>
                  <p className="text-lg font-semibold text-white font-mono">
                    {result.model_id}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Model Type</p>
                  <p className="text-lg font-semibold text-white">
                    {result.model_type}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Status</p>
                  <p className="text-lg font-semibold text-green-400">
                    {result.status}
                  </p>
                </div>
              </div>
            </div>

            {/* Metrics */}
            {result.metrics && result.metrics.length > 0 && (
              <div className="bg-dark-card border border-dark-border rounded-lg p-6">
                <h3 className="text-lg font-semibold text-white mb-4">Model Metrics</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-dark-border">
                    <thead className="bg-dark-surface">
                      <tr>
                        {Object.keys(result.metrics[0]).map((key) => (
                          <th
                            key={key}
                            className="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider"
                          >
                            {key}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-dark-card divide-y divide-dark-border">
                      {result.metrics.slice(0, 5).map((metric: any, idx: number) => (
                        <tr key={idx}>
                          {Object.values(metric).map((value: any, valIdx: number) => (
                            <td key={valIdx} className="px-4 py-3 text-sm text-white">
                              {typeof value === 'number' ? value.toFixed(4) : String(value)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Continue Button */}
            <div className="flex justify-end">
              <button
                onClick={handleContinue}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-500 transition-all duration-200 shadow-lg shadow-primary-600/50 hover:shadow-primary-500/50"
              >
                View Results →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
