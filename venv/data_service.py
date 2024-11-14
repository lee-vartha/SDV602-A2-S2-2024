import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np

# Define the class to handle data reading, uploading, and merging
class DataService:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_data()

    # Reading data from local file (CSV, JSON, etc.)
    def read_data(self):
        if os.path.exists(self.file_path):
            return pd.read_csv(self.file_path)
        else:
            return pd.DataFrame()  # Return an empty DataFrame if the file does not exist

    # Merging new data with the existing dataset
    def merge_data(self, new_data):
        if not self.data.empty:
            self.data = pd.concat([self.data, new_data], ignore_index=True)
        else:
            self.data = new_data
        self.save_data()

    # Saving the merged data back to the local file
    def save_data(self):
        self.data.to_csv(self.file_path, index=False)

    # Plotting the data for each DES (for example, Bar chart for DES1)
    def create_chart_des1(self):
        if self.data.empty:
            return None
        source = self.data['source']
        usage = self.data['usage']

        figure, axis = plt.subplots()
        axis.bar(source, usage, color=['green', 'red', 'blue', 'orange', 'gray', 'yellow', 'purple'])
        axis.set_title('Music Consumption Source (%)', fontsize=10)
        axis.set_ylabel('Percentage', fontsize=8)

        buf = io.BytesIO()
        plt.savefig(buf, format='PNG')
        plt.close(figure)
        buf.seek(0)
        return buf

    def create_chart_des2(self):
        if self.data.empty:
            return None
        services = self.data['service']
        usage = self.data['usage']

        figure, axis = plt.subplots()
        axis.pie(usage, labels=services, autopct='%1.1f%%')
        axis.set_title('Music Pie Chart (%)', fontsize=10)

        buf = io.BytesIO()
        plt.savefig(buf, format='PNG')
        plt.close(figure)
        buf.seek(0)
        return buf

    def create_chart_des3(self):
        if self.data.empty:
            return None
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        figure, axis = plt.subplots()
        axis.plot(t, s)
        axis.set(xlabel='time (s)', ylabel='voltage (mV)', title='Simple Plot')
        axis.grid()

        buf = io.BytesIO()
        plt.savefig(buf, format='PNG')
        plt.close(figure)
        buf.seek(0)
        return buf
