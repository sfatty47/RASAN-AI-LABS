# Deploying RASAN AI Labs

This guide will help you deploy the RASAN AI Labs application to Streamlit Cloud.

## Prerequisites

1. A GitHub account
2. A Streamlit Cloud account (https://streamlit.io/cloud)

## Deployment Steps

1. **Create a GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the main file path to `app.py`
   - Click "Deploy"

## Local Development

To run the application locally:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Troubleshooting

If you encounter any issues:

1. Check the Streamlit Cloud logs
2. Ensure all dependencies are listed in requirements.txt
3. Verify the Python version in runtime.txt
4. Check file permissions and paths

## Support

For support, please contact support@rasanailabs.com 