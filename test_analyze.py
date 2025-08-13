import unittest
import pandas as pd
import os

from analyze_sensor_data import load_sensor_data, clean_sensor_data, process_sensor_data

DATA_FILE = "data/capteur_temp.csv"


class TestSensorDataAnalysis(unittest.TestCase):

    def test_load_sensor_data_file_exists(self):
        """Test that the CSV loads correctly and returns a DataFrame"""
        self.assertTrue(os.path.exists(DATA_FILE), f"Test file {DATA_FILE} is missing")
        df = load_sensor_data(DATA_FILE)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0, "DataFrame should not be empty")

    def test_clean_sensor_data_no_nulls_in_key_columns(self):
        """Test that cleaning removes NaNs from important columns"""
        df = load_sensor_data(DATA_FILE)
        df_cleaned = clean_sensor_data(df)
        for col in ['PM2.5 (μg/m³) corrected', 'Temperature (°C) corrected', 'Humidity (%) corrected']:
            self.assertFalse(df_cleaned[col].isnull().any(), f"{col} still has NaNs after cleaning")

    def test_process_sensor_data_structure(self):
        """Test that process_sensor_data returns all expected keys"""
        results = process_sensor_data(DATA_FILE)
        expected_keys = {
            "daily_averages",
            "correlations",
            "most_polluted_location",
            "peak_hours_count",
            "cleaned_rows"
        }
        self.assertTrue(expected_keys.issubset(results.keys()), "Missing expected result keys")

    def test_process_sensor_data_values(self):
        """Test that results contain non-empty values"""
        results = process_sensor_data(DATA_FILE)
        self.assertIsInstance(results["daily_averages"], dict)
        self.assertGreater(len(results["daily_averages"]), 0, "Daily averages should not be empty")
        self.assertIsInstance(results["correlations"], dict)
        self.assertIsInstance(results["most_polluted_location"], str)
        self.assertIsInstance(results["peak_hours_count"], int)
        self.assertIsInstance(results["cleaned_rows"], int)


if __name__ == "__main__":
    unittest.main()

# To run the tests, use the command:
# python -m unittest test_analyze.py
