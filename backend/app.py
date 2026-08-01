import joblib
import pandas as pd
from flask import Flask, request, jsonify
import io

# Initialize Flask app
superkart_api = Flask("SuperKart Sales Predictor")

# Load the trained SuperKart model pipeline
# Note: This pipeline includes the ColumnTransformer (preprocessing)
model = joblib.load("superkart_model.joblib")

@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

@superkart_api.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()

    # Extract features in the format expected by the model pipeline
    # The pipeline handles scaling and encoding internally
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_Type': data['Product_Type'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Store_Age': data['Store_Age']
    }

    # Convert to DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    prediction = model.predict(input_data).tolist()[0]

    return jsonify({'Predicted_Product_Store_Sales_Total': prediction})

@superkart_api.post('/v1/predictbatch')
def predict_batch():
    # Get the uploaded CSV file
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    input_data = pd.read_csv(file)

    # Make predictions
    predictions = model.predict(input_data).tolist()

    # Add predictions to response
    input_data['Predicted_Sales'] = predictions
    result = input_data.to_dict(orient="records")

    return jsonify(result)

if __name__ == '__main__':
    superkart_api.run(host='0.0.0.0', port=7860, debug=True)
