import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    precision_recall_curve,
    mean_squared_error,
    r2_score,
    mean_absolute_error
)
from pycaret.regression import predict_model as predict_reg
from pycaret.classification import predict_model as predict_clf
import shap

class VisualizationService:
    """Service for generating ML visualizations"""
    
    def generate_feature_importance(self, model, X: pd.DataFrame, top_n: int = 10) -> Dict[str, Any]:
        """Generate feature importance chart data"""
        try:
            # Try to get feature importance from model
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
            elif hasattr(model, 'coef_'):
                importances = np.abs(model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_)
            else:
                # Use SHAP as fallback
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X.head(100))  # Use sample for speed
                if isinstance(shap_values, list):
                    importances = np.abs(shap_values[0]).mean(0)
                else:
                    importances = np.abs(shap_values).mean(0)
            
            feature_names = list(X.columns)
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False).head(top_n)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=importance_df['importance'],
                    y=importance_df['feature'],
                    orientation='h',
                    marker=dict(color=importance_df['importance'], colorscale='Blues')
                )
            ])
            fig.update_layout(
                title='Feature Importance',
                xaxis_title='Importance',
                yaxis_title='Features',
                height=max(400, len(importance_df) * 40),
                template='plotly_white'
            )
            
            return json.loads(json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder))
        except Exception as e:
            return {"error": f"Failed to generate feature importance: {str(e)}"}
    
    def generate_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray, labels: Optional[List] = None) -> Dict[str, Any]:
        """Generate confusion matrix heatmap"""
        try:
            cm = confusion_matrix(y_true, y_pred, labels=labels)
            
            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=['Predicted ' + str(i) for i in (labels if labels is not None else range(len(cm)))],
                y=['Actual ' + str(i) for i in (labels if labels is not None else range(len(cm)))],
                colorscale='Blues',
                text=cm,
                texttemplate='%{text}',
                textfont={"size": 12},
                hoverongaps=False
            ))
            fig.update_layout(
                title='Confusion Matrix',
                xaxis_title='Predicted',
                yaxis_title='Actual',
                template='plotly_white',
                height=400
            )
            
            return json.loads(json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder))
        except Exception as e:
            return {"error": f"Failed to generate confusion matrix: {str(e)}"}
    
    def generate_roc_curve(self, y_true: np.ndarray, y_pred_proba: np.ndarray, labels: Optional[List] = None) -> Dict[str, Any]:
        """Generate ROC curve for binary/multi-class classification"""
        try:
            from sklearn.preprocessing import label_binarize
            from sklearn.metrics import roc_curve, auc
            from itertools import cycle
            
            if len(np.unique(y_true)) == 2:
                # Binary classification
                fpr, tpr, _ = roc_curve(y_true, y_pred_proba[:, 1] if y_pred_proba.ndim > 1 else y_pred_proba)
                roc_auc = auc(fpr, tpr)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=fpr,
                    y=tpr,
                    mode='lines',
                    name=f'ROC (AUC = {roc_auc:.2f})',
                    line=dict(width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=[0, 1],
                    y=[0, 1],
                    mode='lines',
                    name='Random',
                    line=dict(dash='dash', color='gray')
                ))
                fig.update_layout(
                    title=f'ROC Curve (AUC = {roc_auc:.2f})',
                    xaxis_title='False Positive Rate',
                    yaxis_title='True Positive Rate',
                    template='plotly_white',
                    height=400
                )
            else:
                # Multi-class
                y_bin = label_binarize(y_true, classes=np.unique(y_true))
                n_classes = y_bin.shape[1]
                
                fig = go.Figure()
                colors = cycle(['blue', 'red', 'green', 'orange', 'purple'])
                
                for i, color in zip(range(n_classes), colors):
                    fpr, tpr, _ = roc_curve(y_bin[:, i], y_pred_proba[:, i])
                    roc_auc = auc(fpr, tpr)
                    fig.add_trace(go.Scatter(
                        x=fpr,
                        y=tpr,
                        mode='lines',
                        name=f'Class {i} (AUC = {roc_auc:.2f})',
                        line=dict(color=color, width=2)
                    ))
                
                fig.add_trace(go.Scatter(
                    x=[0, 1],
                    y=[0, 1],
                    mode='lines',
                    name='Random',
                    line=dict(dash='dash', color='gray')
                ))
                fig.update_layout(
                    title='Multi-class ROC Curves',
                    xaxis_title='False Positive Rate',
                    yaxis_title='True Positive Rate',
                    template='plotly_white',
                    height=400
                )
            
            return json.loads(json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder))
        except Exception as e:
            return {"error": f"Failed to generate ROC curve: {str(e)}"}
    
    def generate_prediction_distribution(self, y_true: np.ndarray, y_pred: np.ndarray, problem_type: str) -> Dict[str, Any]:
        """Generate prediction distribution charts"""
        try:
            if problem_type == "Regression":
                # Residual plot
                residuals = y_true - y_pred
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=y_pred,
                    y=residuals,
                    mode='markers',
                    name='Residuals',
                    marker=dict(size=6, opacity=0.6)
                ))
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                fig.update_layout(
                    title='Residual Plot',
                    xaxis_title='Predicted Values',
                    yaxis_title='Residuals (Actual - Predicted)',
                    template='plotly_white',
                    height=400
                )
            else:
                # Classification: Distribution comparison
                fig = go.Figure()
                unique_values = np.unique(y_true)
                
                for val in unique_values:
                    pred_counts = np.sum(y_pred == val)
                    fig.add_trace(go.Bar(
                        x=[f'Class {val}'],
                        y=[pred_counts],
                        name=f'Class {val}',
                        text=[pred_counts],
                        textposition='auto'
                    ))
                
                fig.update_layout(
                    title='Prediction Distribution',
                    xaxis_title='Class',
                    yaxis_title='Count',
                    template='plotly_white',
                    height=400,
                    barmode='group'
                )
            
            return json.loads(json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder))
        except Exception as e:
            return {"error": f"Failed to generate distribution: {str(e)}"}
    
    def generate_correlation_heatmap(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate correlation heatmap for numerical features"""
        try:
            # Only numerical columns
            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                return {"error": "No numerical columns found"}
            
            corr = numeric_df.corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.index,
                colorscale='RdBu',
                zmid=0,
                text=corr.round(2).values,
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False
            ))
            fig.update_layout(
                title='Correlation Heatmap',
                template='plotly_white',
                height=max(500, len(corr) * 30),
                width=max(500, len(corr) * 30)
            )
            
            return json.loads(json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder))
        except Exception as e:
            return {"error": f"Failed to generate correlation heatmap: {str(e)}"}
    
    def generate_classification_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """Generate classification metrics bar chart"""
        try:
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            
            metrics = {
                'Accuracy': accuracy_score(y_true, y_pred),
                'Precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
                'Recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
                'F1 Score': f1_score(y_true, y_pred, average='weighted', zero_division=0)
            }
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(metrics.keys()),
                    y=list(metrics.values()),
                    marker=dict(color=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'])
                )
            ])
            fig.update_layout(
                title='Classification Metrics',
                xaxis_title='Metric',
                yaxis_title='Score',
                yaxis=dict(range=[0, 1]),
                template='plotly_white',
                height=400
            )
            
            return json.loads(json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder))
        except Exception as e:
            return {"error": f"Failed to generate metrics: {str(e)}"}
    
    def generate_regression_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """Generate regression metrics"""
        try:
            mse = mean_squared_error(y_true, y_pred)
            mae = mean_absolute_error(y_true, y_pred)
            r2 = r2_score(y_true, y_pred)
            rmse = np.sqrt(mse)
            
            metrics = {
                'R² Score': r2,
                'RMSE': rmse,
                'MAE': mae,
                'MSE': mse
            }
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(metrics.keys()),
                    y=list(metrics.values()),
                    marker=dict(color=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'])
                )
            ])
            fig.update_layout(
                title='Regression Metrics',
                xaxis_title='Metric',
                yaxis_title='Value',
                template='plotly_white',
                height=400
            )
            
            return json.loads(json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder))
        except Exception as e:
            return {"error": f"Failed to generate metrics: {str(e)}"}

visualization_service = VisualizationService()

