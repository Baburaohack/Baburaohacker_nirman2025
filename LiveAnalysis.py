import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import display, clear_output

# Step 1: Dynamic Data Generation
def real_time_data_generator():
    """
    Generator function to simulate real-time sensor data.
    Yields one data point at a time.
    """
    while True:
        temperature = np.random.normal(75, 10)  # Mean = 75, StdDev = 10
        power_consumption = np.random.normal(200, 50)  # Mean = 200, StdDev = 50
        operating_duration = np.random.normal(50, 20)  # Mean = 50, StdDev = 20
        resource_allocation = np.random.uniform(50, 100)  # Range = [50, 100]

        # Simulated data point
        yield {
            "Temperature": temperature,
            "Power Consumption": power_consumption,
            "Operating Duration": operating_duration,
            "Resource Allocation": resource_allocation
        }
        time.sleep(1)  # Wait 1 second to simulate real-time flow

# Step 2: Pre-train the Model
def prepare_training_data():
    """
    Create a static dataset for training the machine learning model.
    """
    np.random.seed(42)
    data = {
        "Temperature": np.random.normal(75, 10, 500),
        "Power Consumption": np.random.normal(200, 50, 500),
        "Operating Duration": np.random.normal(50, 20, 500),
        "Resource Allocation": np.random.uniform(50, 100, 500),
    }
    df = pd.DataFrame(data)

    # Failure condition: High temp or power, low resources
    df["Failure"] = (
        (df["Temperature"] > 85) |
        (df["Power Consumption"] > 250) |
        (df["Resource Allocation"] < 60)
    ).astype(int)
    return df

def train_model():
    """
    Train a Random Forest model using the prepared dataset.
    """
    # Prepare data
    df = prepare_training_data()
    X = df.drop(columns=["Failure"])
    y = df["Failure"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(random_state=42, n_estimators=100)
    model.fit(X_train, y_train)

    # Evaluate the model
    print("Training Complete. Model Evaluation:")
    print(classification_report(y_test, model.predict(X_test)))
    return model

# Step 3: Real-Time Processing and Prediction with Graph Updates
def real_time_analysis(model):
    """
    Process and predict failures in real time using the dynamic data generator.
    Also, display graphs for real-time updates.
    """
    # Initialize the figure and axes for the plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.set_title("Real-Time Data")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Value")
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 300)

    ax2.set_title("Failure Probability")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Probability")
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 1)

    time_data = []
    temp_data = []
    power_data = []
    prob_data = []

    def update_plot(frame):
        data_point = next(generator)
        df = pd.DataFrame([data_point])

        # Predict failure probability
        prediction = model.predict_proba(df)[0][1]  # Probability of class 1 (failure)

        # Update data for the graph
        time_data.append(frame)
        temp_data.append(data_point["Temperature"])
        power_data.append(data_point["Power Consumption"])
        prob_data.append(prediction)

        # Limit the length of data for smooth scrolling
        if len(time_data) > 100:
            time_data.pop(0)
            temp_data.pop(0)
            power_data.pop(0)
            prob_data.pop(0)

        # Update graphs
        ax1.clear()
        ax2.clear()

        # Real-time data plot
        ax1.plot(time_data, temp_data, label="Temperature", color="r")
        ax1.plot(time_data, power_data, label="Power Consumption", color="b")
        ax1.legend(loc="upper right")

        # Failure probability plot
        ax2.plot(time_data, prob_data, label="Failure Probability", color="g")
        ax2.legend(loc="upper right")

        # Prediction below the graph
        ax2.text(0.5, 0.1, f"Latest Failure Probability: {prediction:.2f}", horizontalalignment='center', transform=ax2.transAxes)

        # Display failure prediction alert if necessary
        if prediction > 0.7:
            print("ALERT: High likelihood of failure! Immediate action required.\n")
        else:
            print("System Status: Normal.\n")
        
        # Update the plot on the Colab output
        clear_output(wait=True)
        display(fig)

    # Set up the real-time data generator
    generator = real_time_data_generator()

    # Create an animation for real-time graph updates
    for frame in range(100):  # Update 100 times (1 second interval for each)
        update_plot(frame)
        time.sleep(1)  # Wait for 1 second to simulate real-time data flow

# Step 4: Main Workflow
if __name__ == "__main__":
    # Train the model
    model = train_model()

    # Start real-time analysis with live graph updates
    real_time_analysis(model)
