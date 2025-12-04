import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  DocumentCheckIcon,
  ChartBarIcon,
  ArrowDownTrayIcon 
} from '@heroicons/react/24/outline';
import { getModel, predict } from '../services/api';

export default function ResultsPage() {
  const [modelInfo, setModelInfo] = useState<any>(null);
  const [prediction, setPrediction] = useState<any>(null);
  const [predicting, setPredicting] = useState(false);
  const [predictionData, setPredictionData] = useState<Record<string, number>>({});
  const [uploadedFile, setUploadedFile] = useState<any>(null);
  const [trainingResult, setTrainingResult] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fileData = localStorage.getItem('uploadedFile');
    const trainingData = localStorage.getItem('trainingResult');

    if (fileData) {
      setUploadedFile(JSON.parse(fileData));
    }

    if (trainingData) {
      const result = JSON.parse(trainingData);
      setTrainingResult(result);
      loadModelInfo(result.model_id);
    } else {
      navigate('/training');
    }
  }, [navigate]);

  const loadModelInfo = async (modelId: string) => {
    try {
      const info = await getModel(modelId);
      setModelInfo(info);
    } catch (err) {
      console.error('Failed to load model info:', err);
    }
  };

  const handlePredict = async () => {
    if (!trainingResult || Object.keys(predictionData).length === 0) {
      return;
    }

    setPredicting(true);
    try {
      const result = await predict(trainingResult.model_id, predictionData);
      setPrediction(result);
    } catch (err: any) {
      console.error('Prediction failed:', err);
    } finally {
      setPredicting(false);
    }
  };

  const initializePredictionInputs = () => {
    if (uploadedFile?.column_names) {
      const inputs: Record<string, number> = {};
      uploadedFile.column_names.forEach((col: string) => {
        if (col !== trainingResult?.target) {
          inputs[col] = 0;
        }
      });
      setPredictionData(inputs);
    }
  };

  useEffect(() => {
    if (uploadedFile && trainingResult) {
      initializePredictionInputs();
    }
  }, [uploadedFile, trainingResult]);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm p-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Model Results</h2>
        <p className="text-gray-600 mb-8">
          View your trained model and make predictions.
        </p>

        {/* Model Information */}
        {trainingResult && (
          <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <DocumentCheckIcon className="h-6 w-6 text-primary-600" />
              <h3 className="text-lg font-semibold text-gray-900">Model Information</h3>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Model ID</p>
                <p className="text-lg font-semibold text-gray-900 font-mono">
                  {trainingResult.model_id}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Model Type</p>
                <p className="text-lg font-semibold text-gray-900">
                  {trainingResult.model_type}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Status</p>
                <p className="text-lg font-semibold text-green-600">
                  {modelInfo?.status || trainingResult.status}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Prediction Interface */}
        {uploadedFile && trainingResult && (
          <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <ChartBarIcon className="h-6 w-6 text-primary-600" />
              <h3 className="text-lg font-semibold text-gray-900">Make Predictions</h3>
            </div>

            <div className="space-y-4 mb-6">
              {Object.keys(predictionData).map((key) => (
                <div key={key}>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {key}
                  </label>
                  <input
                    type="number"
                    step="any"
                    value={predictionData[key]}
                    onChange={(e) =>
                      setPredictionData({
                        ...predictionData,
                        [key]: parseFloat(e.target.value) || 0,
                      })
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              ))}
            </div>

            <button
              onClick={handlePredict}
              disabled={predicting}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {predicting ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Predicting...
                </>
              ) : (
                <>
                  <ChartBarIcon className="h-5 w-5" />
                  Predict
                </>
              )}
            </button>
          </div>
        )}

        {/* Prediction Results */}
        {prediction && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Prediction Result</h3>
            <div className="bg-white rounded-lg p-4">
              {Array.isArray(prediction.predictions) ? (
                <div className="space-y-2">
                  {prediction.predictions.map((pred: number, idx: number) => (
                    <p key={idx} className="text-2xl font-bold text-primary-600">
                      Prediction {idx + 1}: {typeof pred === 'number' ? pred.toFixed(4) : pred}
                    </p>
                  ))}
                </div>
              ) : (
                <p className="text-2xl font-bold text-primary-600">
                  {typeof prediction.predictions === 'number' 
                    ? prediction.predictions.toFixed(4) 
                    : prediction.predictions}
                </p>
              )}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="mt-8 flex gap-4">
          <button
            onClick={() => navigate('/')}
            className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Start New Project
          </button>
          {trainingResult && (
            <button
              onClick={() => {
                const data = {
                  model_id: trainingResult.model_id,
                  model_type: trainingResult.model_type,
                  training_result: trainingResult,
                };
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${trainingResult.model_id}_results.json`;
                a.click();
              }}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors flex items-center gap-2"
            >
              <ArrowDownTrayIcon className="h-5 w-5" />
              Export Results
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

