import streamlit as st
import plotly.express as px 

import os
import pandas as pd

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

from pycaret.regression import setup, compare_models, pull, save_model

with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("Auto Streamlit")
    choice = st.radio("Navigation", ["Upload", "Profile", "Machine Learning", "Download"])
    st.info("Hello")

if os.path.exists("dataset.csv"): 
    df = pd.read_csv('dataset.csv', index_col=None)


if choice == "Upload": 
    st.title("Upload")
    file = st.file_uploader("Upload Your Dataset")
    if file: 
        df = pd.read_csv(file, index_col=None)
        df.to_csv("dataset.csv", index=None)
        st.dataframe(df)

if choice == "Profile": 
    st.title("Profile")
    profile_df = df.profile_report()
    st_profile_report(profile_df)

if choice == "Machine Learning": 
    target = st.selectbox("Choose the Target", df.columns)
    if st.button("Run Modelling"): 
        setup(df, target=target, silent=True)
        setup_df = pull()
        st.dataframe(setup_df)
        best_model = compare_models()
        compare_df = pull()
        save_model(best_model, 'best_model')
        st.dataframe(compare_df)

if choice == "Download":
    with open("best_model.pkl", 'rb') as f: 
        st.download_button("Download Model", f, "best_model_test.pkl")

import unittest
import pandas as pd
import numpy as np
from pycaret.regression import setup, compare_models, pull
import os

class TestRasanAILabs(unittest.TestCase):
    def setUp(self):
        # Create sample dataset
        self.data = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'target': np.random.normal(0, 1, 100)
        })
        self.data.to_csv('test_dataset.csv', index=False)

    def test_data_loading(self):
        """Test if data can be loaded correctly"""
        df = pd.read_csv('test_dataset.csv')
        self.assertEqual(df.shape, (100, 3))
        self.assertTrue('target' in df.columns)

    def test_model_training(self):
        """Test if model training works"""
        try:
            setup(self.data, target='target', silent=True)
            best_model = compare_models()
            self.assertIsNotNone(best_model)
        except Exception as e:
            self.fail(f"Model training failed with error: {str(e)}")

    def tearDown(self):
        # Clean up test files
        if os.path.exists('test_dataset.csv'):
            os.remove('test_dataset.csv')
        if os.path.exists('best_model.pkl'):
            os.remove('best_model.pkl')

if __name__ == '__main__':
    unittest.main()
