import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Function to generate Steel Utensil Manufacturing Dataset
def generate_steel_utensil_data(num_rows=10000):
    np.random.seed(42)
    data = {
        'UDI': np.arange(1, num_rows + 1),
        'Product ID': np.random.choice(['L', 'M', 'H'], size=num_rows, p=[0.5, 0.3, 0.2]),
        'Raw Material Quality': np.random.randint(6, 11, size=num_rows),
        'Air temperature [K]': np.random.normal(300, 2, size=num_rows).clip(295, 305),
        'Process temperature [K]': np.random.normal(310, 1, size=num_rows).clip(305, 315),
        'Tool Speed [rpm]': np.random.normal(2000, 50, size=num_rows).clip(1900, 2100),
        'Torque [Nm]': np.random.normal(45, 5, size=num_rows).clip(30, 60),
        'Tool Wear [min]': np.random.randint(0, 301, size=num_rows),
        'Machine Failure': np.random.choice([0, 1], size=num_rows, p=[0.9, 0.1]),
        'Vibration Level [g]': np.random.normal(2.0, 0.5, size=num_rows).clip(1.5, 3.5),
        'Humidity [%]': np.random.randint(40, 61, size=num_rows),
        'Energy Consumption [W]': np.random.normal(4000, 300, size=num_rows).clip(3500, 4500),
        'Pressure [Pa]': np.random.randint(100000, 200001, size=num_rows)
    }
    return pd.DataFrame(data)

# Function to generate Data Warehouse Dataset
def generate_data_warehouse_data(num_rows=10000):
    np.random.seed(42)
    data = {
        'UDI': np.arange(1, num_rows + 1),
        'Server Type': np.random.choice(['L', 'M', 'H'], size=num_rows, p=[0.5, 0.3, 0.2]),
        'CPU Utilization [%]': np.random.randint(10, 101, size=num_rows),
        'Memory Usage [%]': np.random.randint(10, 101, size=num_rows),
        'Air Temperature [K]': np.random.normal(295, 2, size=num_rows).clip(290, 300),
        'Disk I/O Operations': np.random.randint(1000, 5000, size=num_rows),
        'Network Latency [ms]': np.random.normal(30, 5, size=num_rows).clip(1,None),
        'Power Consumption [W]': np.random.normal(350 ,50 ,size = num_rows).clip(100,None),
        'Machine Failure': np.random.choice([0 ,1],size = num_rows),
        'Vibration Level [g]': np.random.normal(1.5 ,0.3 ,size = num_rows).clip(0.5 ,None),
        'Cooling Efficiency [%]': np.random.randint(50 ,101 ,size = num_rows),
        'Network Throughput [Mbps]': np.random.randint(100 ,1001 ,size = num_rows)
    }
    return pd.DataFrame(data)

# Train a Model on Steel Utensil Manufacturing Data
def train_steel_utensil_model():
    df = generate_steel_utensil_data()

    # Features and target variable
    X = df[['Raw Material Quality',
             'Air temperature [K]',
             'Process temperature [K]',
             'Tool Speed [rpm]',
             'Torque [Nm]',
             'Tool Wear [min]',
             'Vibration Level [g]',
             'Humidity [%]',
             'Energy Consumption [W]',
             'Pressure [Pa]']]

    y = df['Machine Failure'] # Binary classification

    # Split the dataset into training and testing sets
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2 ,random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Create and fit the model with increased max_iter
    model = LogisticRegression(max_iter=200)
    model.fit(X_train_scaled,y_train)

    # Predictions and evaluation
    predictions = model.predict(X_test_scaled)

    print("\nSteel Utensil Manufacturing Model Results:")
    print(classification_report(y_test,predictions))

    # Confusion Matrix
    cm = confusion_matrix(y_test,predictions)
    plt.figure(figsize=(8 ,6))
    sns.heatmap(cm ,annot=True ,fmt='d' ,cmap='Blues')
    plt.title('Confusion Matrix for Machine Failure Prediction')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# Train a Model on Data Warehouse Data
def train_data_warehouse_model():
    df = generate_data_warehouse_data()

    # Features and target variable
    X = df[['Memory Usage [%]',
             'Air Temperature [K]',
             'Disk I/O Operations',
             'Network Latency [ms]',
             'Power Consumption [W]',
             'Vibration Level [g]',
             'Cooling Efficiency [%]',
             'Network Throughput [Mbps]']]

    y = df['CPU Utilization [%]'] # Regression problem

    # Split the dataset into training and testing sets
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2 ,random_state=42)

    # Create and fit the model
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train,y_train)

    # Predictions and evaluation
    predictions = model.predict(X_test)

    print("\nData Warehouse Model Results:")
    print(f"Mean Absolute Error: {mean_absolute_error(y_test,predictions):.2f}")
    print(f"Mean Squared Error: {mean_squared_error(y_test,predictions):.2f}")
    print(f"R-squared: {r2_score(y_test,predictions):.2f}")

# Function to get user input for prediction
def user_input_prediction():

   print("\nEnter values for prediction:")

   # Parameter descriptions and limits for Steel Utensil Manufacturing
   params_desc = {
       "Raw Material Quality": "Quality of raw materials (6-10)",
       "Air temperature [K]": "Air temperature during production (295-305 K)",
       "Process temperature [K]": "Process temperature (305-315 K)",
       "Tool Speed [rpm]": "Speed of cutting tool (1900-2100 rpm)",
       "Torque [Nm]": "Torque applied (30-60 Nm)",
       "Tool Wear [min]": "Cumulative time tool has been used (0-300 min)",
       "Vibration Level [g]": "Measured vibration levels of machinery (1.5-3.5 g)",
       "Humidity [%]": "Humidity levels in production environment (40-60%)",
       "Energy Consumption [W]": "Power usage during operation (3500-4500 W)",
       "Pressure [Pa]": "Pressure levels in hydraulic systems (100000-200000 Pa)"
   }

   user_input_values = {}

   for param in params_desc:
       value = float(input(f"{param} ({params_desc[param]}): "))

       # Validate input ranges based on parameter description
       if param == "Raw Material Quality" and not (6 <= value <= 10):
           print("Invalid value! Must be between 6 and 10.")
           return

       if param == "Air temperature [K]" and not (295 <= value <= 305):
           print("Invalid value! Must be between 295 K and 305 K.")
           return

       if param == "Process temperature [K]" and not (305 <= value <= 315):
           print("Invalid value! Must be between 305 K and 315 K.")
           return

       if param == "Tool Speed [rpm]" and not (1900 <= value <= 2100):
           print("Invalid value! Must be between 1900 rpm and 2100 rpm.")
           return

       if param == "Torque [Nm]" and not (30 <= value <= 60):
           print("Invalid value! Must be between 30 Nm and 60 Nm.")
           return

       if param == "Tool Wear [min]" and not (0 <= value <= 300):
           print("Invalid value! Must be between 0 min and 300 min.")
           return

       if param == "Vibration Level [g]" and not (1.5 <= value <= 3.5):
           print("Invalid value! Must be between 1.5 g and 3.5 g.")
           return

       if param == "Humidity [%]" and not (40 <= value <= 60):
           print("Invalid value! Must be between 40% and 60%.")
           return

       if param == "Energy Consumption [W]" and not (3500 <= value <= 4500):
           print("Invalid value! Must be between 3500 W and 4500 W.")
           return

       if param == "Pressure [Pa]" and not (100000 <= value <= 200000):
           print("Invalid value! Must be between 100000 Pa and 200000 Pa.")
           return

       user_input_values[param] = value

   # Make prediction based on user input values
   input_array = pd.DataFrame([user_input_values])

   # Train the model again to use it for prediction based on user input.
   df = generate_steel_utensil_data()

   X_train = df[['Raw Material Quality',
                  'Air temperature [K]',
                  'Process temperature [K]',
                  'Tool Speed [rpm]',
                  'Torque [Nm]',
                  'Tool Wear [min]',
                  'Vibration Level [g]',
                  'Humidity [%]',
                  'Energy Consumption [W]',
                  'Pressure [Pa]']]

   y_train = df['Machine Failure']

   model = LogisticRegression(max_iter=200)
   model.fit(X_train,y_train)

   prediction = model.predict(input_array)[0]

   print(f"\nPredicted Machine Failure Probability: {prediction:.2f}.")

# Main Execution Flow
if __name__ == "__main__":

   # Train models for both datasets
   train_steel_utensil_model()
   train_data_warehouse_model()

   # Allow user to enter values for prediction
   user_input_prediction()
