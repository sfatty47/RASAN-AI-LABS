import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  DocumentCheckIcon,
  ChartBarIcon,
  ArrowDownTrayIcon,
  PhotoIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { getModel, predict, predictAndVisualize } from '../services/api';
import PlotlyChart from '../components/PlotlyChart';

export default function ResultsPage() {
  const [modelInfo, setModelInfo] = useState<any>(null);
  const [prediction, setPrediction] = useState<any>(null);
  const [predicting, setPredicting] = useState(false);
  const [predictionData, setPredictionData] = useState<Record<string, number>>({});
  const [uploadedFile, setUploadedFile] = useState<any>(null);
  const [trainingResult, setTrainingResult] = useState<any>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [visualizations, setVisualizations] = useState<Record<string, any>>({});
  const [loadingViz, setLoadingViz] = useState(false);
  const [targetColumn, setTargetColumn] = useState('');
  const [vizError, setVizError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fileData = localStorage.getItem('uploadedFile');
    const trainingData = localStorage.getItem('trainingResult');
    const analysisData = localStorage.getItem('analysisResult');

    if (fileData) {
      setUploadedFile(JSON.parse(fileData));
    }

    if (analysisData) {
      const analysis = JSON.parse(analysisData);
      setAnalysisResult(analysis);
      if (analysis.target_column) {
        setTargetColumn(analysis.target_column);
      }
    }

    if (trainingData) {
      const result = JSON.parse(trainingData);
      setTrainingResult(result);
      
      // Get target column from training result, analysis, or set from state
      if (result.target_column) {
        setTargetColumn(result.target_column);
      }
      
      loadModelInfo(result.model_id);
      
      // Auto-generate visualizations
      if (fileData) {
        const file = JSON.parse(fileData);
        const target = result.target_column || analysisResult?.target_column || targetColumn;
        if (target && file.filename) {
          setTimeout(() => {
            loadVisualizations(result.model_id, file.filename, target);
          }, 1500);
        }
      }
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

  const loadVisualizations = async (modelId: string, filename: string, target: string) => {
    if (!filename || !target) {
      setVizError('Missing filename or target column');
      return;
    }
    
    setLoadingViz(true);
    setVizError(null);
    setVisualizations({});
    
    try {
      console.log('Loading visualizations:', { modelId, filename, target });
      const result = await predictAndVisualize(modelId, filename, target);
      console.log('Visualization result:', result);
      
      if (result.visualizations) {
        const validViz = Object.entries(result.visualizations).filter(([key, value]) => {
          if (value && typeof value === 'object' && 'error' in value) {
            console.warn(`Chart ${key} failed:`, value.error);
            return false;
          }
          return true;
        });
        
        if (validViz.length === 0) {
          setVizError('All visualizations failed to generate. Check backend logs for details.');
        } else {
          setVisualizations(Object.fromEntries(validViz));
          if (validViz.length < Object.keys(result.visualizations).length) {
            setVizError(`Some charts failed to generate. ${validViz.length}/${Object.keys(result.visualizations).length} charts available.`);
          }
        }
      } else {
        setVizError('No visualizations returned from server');
      }
    } catch (err: any) {
      console.error('Failed to load visualizations:', err);
      
      // Extract readable error message
      let errorMsg = 'Failed to generate visualizations';
      
      if (err.response?.data) {
        const data = err.response.data;
        
        // Handle FastAPI validation errors (array of objects)
        if (Array.isArray(data.detail)) {
          errorMsg = data.detail
            .map((item: any) => {
              if (typeof item === 'string') return item;
              if (item?.msg) return item.msg;
              if (item?.loc && item?.msg) {
                return `${item.loc.join('.')}: ${item.msg}`;
              }
              if (item?.type && item?.msg) {
                return `${item.type}: ${item.msg}`;
              }
              try {
                return JSON.stringify(item, null, 2);
              } catch {
                return String(item);
              }
            })
            .join('; ');
        } else if (typeof data.detail === 'string') {
          errorMsg = data.detail;
        } else if (data.detail && typeof data.detail === 'object') {
          // Try to extract meaningful message from object
          if (data.detail.message) {
            errorMsg = data.detail.message;
          } else if (data.detail.error) {
            errorMsg = data.detail.error;
          } else {
            try {
              errorMsg = JSON.stringify(data.detail, null, 2);
            } catch {
              errorMsg = String(data.detail);
            }
          }
        } else if (data.message) {
          errorMsg = data.message;
        } else if (typeof data === 'string') {
          errorMsg = data;
        }
      } else if (err.message) {
        errorMsg = err.message;
      }
      
      console.error('Visualization error details:', {
        error: err,
        response: err.response,
        message: errorMsg
      });
      
      setVizError(errorMsg);
    } finally {
      setLoadingViz(false);
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
    if (uploadedFile?.column_names && trainingResult) {
      const inputs: Record<string, number> = {};
      uploadedFile.column_names.forEach((col: string) => {
        if (col !== targetColumn) {
          inputs[col] = 0;
        }
      });
      setPredictionData(inputs);
    }
  };

  useEffect(() => {
    if (uploadedFile && trainingResult && targetColumn) {
      initializePredictionInputs();
    }
  }, [uploadedFile, trainingResult, targetColumn]);

  const getChartTitle = (chartType: string) => {
    const titles: Record<string, string> = {
      'feature_importance': 'Feature Importance',
      'confusion_matrix': 'Confusion Matrix',
      'roc_curve': 'ROC Curve',
      'prediction_distribution': 'Prediction Distribution',
      'classification_metrics': 'Classification Metrics',
      'regression_metrics': 'Regression Metrics',
      'correlation_heatmap': 'Correlation Heatmap',
    };
    return titles[chartType] || chartType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Model Information */}
      {trainingResult && (
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="flex items-center gap-2 mb-4">
            <DocumentCheckIcon className="h-6 w-6 text-primary-600" />
            <h2 className="text-3xl font-bold text-gray-900">Model Results</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-600">Model ID</p>
              <p className="text-lg font-semibold text-gray-900 font-mono text-sm">
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
            <div>
              <p className="text-sm text-gray-600">Problem Type</p>
              <p className="text-lg font-semibold text-gray-900">
                {analysisResult?.problem_type || trainingResult.model_type}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Visualizations Section */}
      <div className="bg-white rounded-lg shadow-sm p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <PhotoIcon className="h-6 w-6 text-primary-600" />
            <h3 className="text-2xl font-bold text-gray-900">Visualizations</h3>
          </div>
          {uploadedFile && trainingResult && (targetColumn || analysisResult?.target_column) && (
            <button
              onClick={() => loadVisualizations(
                trainingResult.model_id, 
                uploadedFile.filename, 
                targetColumn || analysisResult?.target_column || ''
              )}
              disabled={loadingViz}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {loadingViz ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Generating...
                </>
              ) : (
                <>
                  <SparklesIcon className="h-4 w-4" />
                  Regenerate Charts
                </>
              )}
            </button>
          )}
        </div>

        {loadingViz && Object.keys(visualizations).length === 0 && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Generating visualizations...</p>
          </div>
        )}

        {Object.keys(visualizations).length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(visualizations).map(([chartType, chartData]) => (
              <div key={chartType} className="bg-gray-50 rounded-lg p-4">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">
                  {getChartTitle(chartType)}
                </h4>
                <PlotlyChart data={chartData} />
              </div>
            ))}
          </div>
        )}

        {vizError && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 text-sm">{vizError}</p>
          </div>
        )}

        {!loadingViz && Object.keys(visualizations).length === 0 && !vizError && (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <PhotoIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-2">No visualizations generated yet</p>
            <p className="text-sm text-gray-500">Click "Regenerate Charts" to create visualizations</p>
          </div>
        )}
      </div>

      {/* Prediction Interface */}
      {uploadedFile && trainingResult && (
        <div className="bg-white rounded-lg shadow-sm p-8">
          <div className="flex items-center gap-2 mb-4">
            <ChartBarIcon className="h-6 w-6 text-primary-600" />
            <h3 className="text-2xl font-bold text-gray-900">Make Predictions</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {Object.keys(predictionData).slice(0, 6).map((key) => (
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

          {Object.keys(predictionData).length > 6 && (
            <p className="text-sm text-gray-500 mb-4">
              Showing first 6 features. All features are included in prediction.
            </p>
          )}

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

          {prediction && (
            <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-2">Prediction Result</h4>
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
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-4">
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
                visualizations: Object.keys(visualizations),
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
  );
}
