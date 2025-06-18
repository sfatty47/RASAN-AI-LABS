import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pycaret.regression import setup, compare_models, pull, save_model, load_model
from pycaret.classification import setup as setup_clf, compare_models as compare_models_clf
import pandas_profiling
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
import os
import shap
import numpy as np
from datetime import datetime
import joblib
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score

# Page config
st.set_page_config(
    page_title="RASAN AI Labs",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def analyze_data_context(df):
    """Analyze the dataset to determine the appropriate analysis approach"""
    analysis_results = {
        'problem_type': None,
        'suitable_approaches': [],
        'data_characteristics': {},
        'recommended_visualizations': []
    }
    
    # Analyze target variable if exists
    if 'target' in df.columns:
        target = df['target']
        if target.nunique() == 2:
            analysis_results['problem_type'] = 'Binary Classification'
            analysis_results['suitable_approaches'].extend(['Logistic Regression', 'Decision Trees', 'Random Forest'])
        elif target.nunique() > 2 and target.nunique() < 10:
            analysis_results['problem_type'] = 'Multi-class Classification'
            analysis_results['suitable_approaches'].extend(['Multi-class Classification', 'Decision Trees', 'Random Forest'])
        else:
            analysis_results['problem_type'] = 'Regression'
            analysis_results['suitable_approaches'].extend(['Linear Regression', 'Random Forest', 'XGBoost'])
    
    # Check for A/B test potential
    if 'group' in df.columns and 'outcome' in df.columns:
        analysis_results['suitable_approaches'].append('A/B Testing')
    
    # Analyze data characteristics
    analysis_results['data_characteristics'] = {
        'numerical_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns),
        'missing_values': df.isnull().sum().sum(),
        'total_rows': len(df)
    }
    
    # Recommend visualizations
    if analysis_results['problem_type'] == 'Regression':
        analysis_results['recommended_visualizations'].extend([
            'Scatter Plot', 'Residual Plot', 'Feature Importance'
        ])
    elif analysis_results['problem_type'] in ['Binary Classification', 'Multi-class Classification']:
        analysis_results['recommended_visualizations'].extend([
            'Confusion Matrix', 'ROC Curve', 'Feature Importance'
        ])
    
    return analysis_results

def generate_visualizations(df, analysis_results):
    """Generate appropriate visualizations based on data analysis"""
    visualizations = {}
    
    if analysis_results['problem_type'] == 'Regression':
        # Scatter plot for numerical features
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 1:
            fig = px.scatter_matrix(df, dimensions=numerical_cols[:4])
            visualizations['scatter_matrix'] = fig
        
        # Correlation heatmap
        corr = df.select_dtypes(include=[np.number]).corr()
        fig = px.imshow(corr, title='Correlation Heatmap')
        visualizations['correlation_heatmap'] = fig
    
    elif analysis_results['problem_type'] in ['Binary Classification', 'Multi-class Classification']:
        # Distribution of target variable
        fig = px.histogram(df, x='target', title='Target Distribution')
        visualizations['target_distribution'] = fig
        
        # Box plots for numerical features by target
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols[:3]:  # Limit to first 3 numerical columns
            fig = px.box(df, x='target', y=col, title=f'{col} by Target')
            visualizations[f'box_plot_{col}'] = fig
    
    return visualizations

def perform_ab_test(df):
    """Perform A/B testing if applicable"""
    if 'group' in df.columns and 'outcome' in df.columns:
        group_a = df[df['group'] == 'A']['outcome']
        group_b = df[df['group'] == 'B']['outcome']
        
        t_stat, p_value = stats.ttest_ind(group_a, group_b)
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'group_a_mean': group_a.mean(),
            'group_b_mean': group_b.mean()
        }
    return None

# Initialize session state
if 'model_type' not in st.session_state:
    st.session_state.model_type = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'setup_data' not in st.session_state:
    st.session_state.setup_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Sidebar
with st.sidebar:
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png", width=200)
    st.title("RASAN AI Labs")
    st.markdown("---")
    
    # Navigation
    choice = st.radio("Navigation", ["Upload", "Smart Analysis", "Model Training", "Model Analysis", "Download"])
    
    st.markdown("---")
    st.info("""
    🤖 RASAN AI Labs - Your AI-Powered AutoML Platform
    
    Transform your data into actionable insights with our advanced machine learning platform.
    """)

# Main content
if choice == "Upload":
    st.title("📊 Data Upload")
    st.markdown("Upload your dataset to begin the machine learning journey")
    
    file = st.file_uploader("Upload Your Dataset (CSV format)", type=['csv'])
    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv('dataset.csv', index=None)
        st.success("Dataset uploaded successfully!")
        
        # Display basic dataset info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Number of Rows", df.shape[0])
        with col2:
            st.metric("Number of Columns", df.shape[1])
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage().sum() / 1024:.2f} KB")
        
        st.dataframe(df.head())

elif choice == "Smart Analysis":
    st.title("🔍 Smart Analysis")
    
    if os.path.exists('./dataset.csv'):
        df = pd.read_csv('dataset.csv', index_col=None)
        
        # Perform contextual analysis
        if st.button("Analyze Dataset"):
            with st.spinner("Analyzing dataset..."):
                st.session_state.analysis_results = analyze_data_context(df)
                
                # Display analysis results
                st.subheader("📊 Analysis Results")
                st.write("Problem Type:", st.session_state.analysis_results['problem_type'])
                st.write("Recommended Approaches:", ", ".join(st.session_state.analysis_results['suitable_approaches']))
                
                # Display data characteristics
                st.subheader("📈 Data Characteristics")
                st.write(st.session_state.analysis_results['data_characteristics'])
                
                # Generate and display visualizations
                st.subheader("🎨 Recommended Visualizations")
                visualizations = generate_visualizations(df, st.session_state.analysis_results)
                for name, fig in visualizations.items():
                    st.plotly_chart(fig)
                
                # Perform A/B test if applicable
                ab_results = perform_ab_test(df)
                if ab_results:
                    st.subheader("📊 A/B Test Results")
                    st.write(ab_results)
    else:
        st.warning("Please upload a dataset first!")

elif choice == "Model Training":
    st.title("🤖 Model Training")
    
    if os.path.exists('./dataset.csv'):
        df = pd.read_csv('dataset.csv', index_col=None)
        
        if st.session_state.analysis_results:
            st.write("Recommended Approach:", st.session_state.analysis_results['problem_type'])
            
            # Target Selection
            chosen_target = st.selectbox('Choose the Target Column', df.columns)
            st.session_state.chosen_target = chosen_target
            
            # Feature Selection
            st.subheader("Feature Selection")
            features = st.multiselect(
                'Select Features (Optional - leave empty to use all features)',
                [col for col in df.columns if col != chosen_target],
                default=[col for col in df.columns if col != chosen_target]
            )
            
            if st.button('Train Models'):
                with st.spinner("Training models..."):
                    try:
                        if st.session_state.analysis_results['problem_type'] == 'Regression':
                            setup(df, target=chosen_target, silent=True)
                            best_model = compare_models()
                        else:
                            setup_clf(df, target=chosen_target, silent=True)
                            best_model = compare_models_clf()
                        
                        setup_df = pull()
                        st.session_state.setup_data = setup_df
                        st.dataframe(setup_df)
                        
                        compare_df = pull()
                        st.dataframe(compare_df)
                        
                        # Save model
                        save_model(best_model, 'best_model')
                        st.session_state.model = best_model
                        st.success("Model training completed successfully!")
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please run Smart Analysis first to determine the appropriate approach!")
    else:
        st.warning("Please upload a dataset first!")

elif choice == "Model Analysis":
    st.title("📈 Model Analysis")
    
    if os.path.exists('./best_model.pkl'):
        model = load_model('best_model')
        df = pd.read_csv('dataset.csv', index_col=None)
        
        # Model Performance Metrics
        st.subheader("Model Performance")
        if st.session_state.setup_data is not None:
            st.dataframe(st.session_state.setup_data)
        
        # Feature Importance
        st.subheader("Feature Importance")
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(df.drop(columns=[st.session_state.chosen_target]))
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df.drop(columns=[st.session_state.chosen_target]).columns,
                y=np.abs(shap_values).mean(0),
                name='Feature Importance'
            ))
            fig.update_layout(
                title="Feature Importance Analysis",
                xaxis_title="Features",
                yaxis_title="SHAP Value (Impact on Model Output)"
            )
            st.plotly_chart(fig)
        except:
            st.info("Feature importance analysis is not available for this model type.")
        
        # Prediction Analysis
        st.subheader("Make Predictions")
        input_data = {}
        for col in df.columns:
            if col != st.session_state.chosen_target:
                input_data[col] = st.number_input(f"Enter {col}", value=float(df[col].mean()))
        
        if st.button("Predict"):
            try:
                prediction = model.predict(pd.DataFrame([input_data]))
                st.success(f"Predicted Value: {prediction[0]:.2f}")
            except:
                st.error("Error making prediction. Please check input values.")
    else:
        st.warning("Please train a model first!")

elif choice == "Download":
    st.title("📥 Download")
    
    if os.path.exists('./best_model.pkl'):
        with open('best_model.pkl', 'rb') as f:
            st.download_button(
                'Download Model',
                f,
                file_name=f"rasan_ai_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
            )
        
        # Export model details
        if st.session_state.setup_data is not None:
            st.download_button(
                'Download Model Report',
                st.session_state.setup_data.to_csv().encode('utf-8'),
                file_name=f"model_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
    else:
        st.warning("No trained model available for download. Please train a model first.")