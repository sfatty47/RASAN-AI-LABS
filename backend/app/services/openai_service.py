from typing import Dict, Any, Optional
import json
from app.config import settings

class OpenAIService:
    """Service for OpenAI LLM-powered features"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.enabled = bool(self.api_key and self.api_key.strip())
        
        if self.enabled:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                # OpenAI package not installed - that's okay, service will be disabled
                self.enabled = False
                self.client = None
            except Exception as e:
                # Other errors initializing OpenAI - log but don't crash
                print(f"OpenAI initialization warning: {e}")
                self.enabled = False
                self.client = None
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        return self.enabled and self.client is not None
    
    async def generate_data_insights(
        self, 
        data_summary: Dict[str, Any],
        analysis_results: Dict[str, Any]
    ) -> Optional[str]:
        """Generate natural language insights about the data"""
        if not self.is_available():
            return None
        
        try:
            prompt = f"""You are a data science expert. Analyze this dataset and provide concise, actionable insights.

Dataset Summary:
- Rows: {data_summary.get('total_rows', 'N/A')}
- Columns: {data_summary.get('total_columns', 'N/A')}
- Numerical columns: {data_summary.get('numerical_columns', 0)}
- Categorical columns: {data_summary.get('categorical_columns', 0)}
- Missing values: {data_summary.get('missing_values', 0)}

Analysis Results:
- Problem Type: {analysis_results.get('problem_type', 'Unknown')}
- Target Column: {analysis_results.get('target_column', 'Not specified')}
- Suitable Approaches: {', '.join(analysis_results.get('suitable_approaches', []))}

Provide 3-5 key insights about this dataset and recommendations for the machine learning approach. Keep it concise and actionable."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful data science expert. Provide clear, concise insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI insights generation failed: {e}")
            return None
    
    async def explain_model_results(
        self,
        model_type: str,
        metrics: Dict[str, Any],
        feature_importance: Optional[Dict[str, float]] = None
    ) -> Optional[str]:
        """Generate natural language explanation of model results"""
        if not self.is_available():
            return None
        
        try:
            metrics_str = json.dumps(metrics, indent=2)
            
            prompt = f"""You are a machine learning expert. Explain these model results in clear, non-technical language.

Model Type: {model_type}
Metrics:
{metrics_str}
"""
            
            if feature_importance:
                top_features = sorted(
                    feature_importance.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:5]
                prompt += f"\nTop 5 Important Features:\n"
                for feature, importance in top_features:
                    prompt += f"- {feature}: {importance:.4f}\n"
            
            prompt += "\nProvide a concise explanation (2-3 paragraphs) of what these results mean and what they tell us about the model's performance."
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful ML expert. Explain results clearly."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI explanation generation failed: {e}")
            return None
    
    async def recommend_next_steps(
        self,
        problem_type: str,
        current_metrics: Dict[str, Any],
        has_missing_values: bool = False
    ) -> Optional[str]:
        """Generate recommendations for next steps"""
        if not self.is_available():
            return None
        
        try:
            prompt = f"""You are a data science consultant. Based on this ML project status, provide actionable next steps.

Problem Type: {problem_type}
Current Metrics: {json.dumps(current_metrics, indent=2)}
Has Missing Values: {has_missing_values}

Provide 3-4 specific, actionable recommendations for improving the model or next steps in the ML workflow. Keep it concise."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful data science consultant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI recommendations generation failed: {e}")
            return None
    
    async def answer_question(
        self,
        question: str,
        context: Dict[str, Any]
    ) -> Optional[str]:
        """Answer questions about the data or model"""
        if not self.is_available():
            return None
        
        try:
            context_str = json.dumps(context, indent=2)
            
            prompt = f"""You are a data science assistant. Answer this question based on the provided context.

Context:
{context_str}

Question: {question}

Provide a clear, helpful answer based on the context. If you cannot answer from the context, say so."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful data science assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI Q&A failed: {e}")
            return None

openai_service = OpenAIService()

