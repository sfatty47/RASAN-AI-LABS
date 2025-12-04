# Training Error Debugging Guide

## Common Training Errors and Solutions

### 1. Target Column Not Found
**Error**: `Target column 'X' not found in dataset`

**Solution**:
- Check that the target column name matches exactly (case-sensitive)
- Verify the column exists in your uploaded file
- Ensure you selected the correct target column from the dropdown

### 2. Empty Dataset
**Error**: `Dataset is empty`

**Solution**:
- Check that your CSV file has data rows
- Verify file uploaded successfully
- Try re-uploading the file

### 3. Missing Values in Target
**Error**: Issues with missing target values

**Solution**:
- The system automatically removes rows with missing target values
- Ensure your target column has valid values
- Preprocess data before training if needed

### 4. PyCaret Setup Errors
**Error**: Various PyCaret-related errors

**Common Causes**:
- Data type issues (strings in numeric columns)
- Too few samples for training
- Incompatible problem type

**Solution**:
- Ensure data types are correct
- Need at least 10-20 samples for training
- Match problem type to your target variable

## How to Check for Errors

### Browser Console
1. Open Developer Tools (F12)
2. Go to Console tab
3. Look for red error messages
4. Copy the full error message

### Network Tab
1. Open Developer Tools (F12)
2. Go to Network tab
3. Click "Train Model"
4. Find the `/train` request
5. Check the Response tab for error details

### Backend Logs
Check your backend console/terminal for detailed error messages.

## Quick Fixes

1. **Clear Browser Cache**: Clear localStorage and refresh
2. **Re-upload Data**: Try uploading your CSV again
3. **Check Data Format**: Ensure CSV is properly formatted
4. **Select Correct Target**: Double-check target column selection
5. **Match Problem Type**: Regression vs Classification must match your data

## Getting Help

If you see an error:
1. Copy the full error message
2. Note what you were doing (which step)
3. Check the browser console
4. Check backend logs

