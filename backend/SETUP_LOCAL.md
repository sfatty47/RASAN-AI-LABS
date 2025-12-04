# 🔧 Local Backend Setup Guide

## Problem

Python 3.13 is too new - `pandas 2.1.4` doesn't compile with it.

## Solution: Use Python 3.11 or 3.12

### Option 1: Use Python 3.11/3.12 (Recommended)

1. **Install Python 3.11 or 3.12** (if not already installed):
   ```bash
   # Using Homebrew (Mac):
   brew install python@3.11
   # or
   brew install python@3.12
   ```

2. **Create virtual environment**:
   ```bash
   cd backend
   python3.11 -m venv venv
   # or
   python3.12 -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run backend**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Option 2: Use Conda (If you have Anaconda/Miniconda)

```bash
cd backend
conda create -n rasan-ai python=3.11 -y
conda activate rasan-ai
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Option 3: Upgrade pandas (May work, but may break PyCaret)

If you want to try Python 3.13, you could upgrade pandas, but this might break PyCaret compatibility:

```bash
pip install pandas>=2.2.0
# But this may conflict with pycaret 3.3.0 which requires pandas<2.2.0
```

## Recommended: Python 3.11

Use Python 3.11 for best compatibility with all dependencies.

