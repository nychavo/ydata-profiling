import os
import tempfile, random, string
from copy import deepcopy
import numpy as np

import pandas as pd
import seaborn as sns
from ydata_profiling import ProfileReport
from ydata_profiling.compare_reports import compare

class DemoYData:
    @staticmethod
    def load_sample_data() -> pd.DataFrame:
        return sns.load_dataset("titanic")

    @staticmethod
    def modify_data(df: pd.DataFrame) -> pd.DataFrame:
        df_mod = df.copy()

        # Modify existing values
        df_mod.loc[0, 'age'] = 99
        df_mod['fare'] = df_mod['fare'] * 1.2
        df_mod['sex'] = df_mod['sex'].replace('male', 'M').replace('female', 'F')

        # Add new columns
        df_mod['fare_category'] = pd.cut(df_mod['fare'], bins=3, labels=['Low', 'Medium', 'High'])
        df_mod['is_senior'] = df_mod['age'] > 60

        # Drop a column
        if 'embarked' in df_mod.columns:
            df_mod = df_mod.drop(columns=['embarked'])

        return df_mod

    @staticmethod
    def generate_profiles(df1: pd.DataFrame, df2: pd.DataFrame):
        ext_properties = {
            "flatSchema": [
                {
                    "columnName": "id",
                    "columnType": "long"
                },
                {
                    "columnName": "firstName",
                    "columnType": "string"
                },
                {
                    "columnName": "lastName",
                    "columnType": "string"
                }
            ]
        }
        ext_properties2 = deepcopy(ext_properties)
        ext_properties2['flatSchema'][0]['columnType'] = 'string'
        ext_properties2['flatSchema'].pop()

        profile1 = ProfileReport(df1, title="Titanic Original", explorative=True, external_properties=ext_properties)
        profile2 = ProfileReport(df2, title="Titanic Modified", explorative=True)
        # profile2 = ProfileReport(df2, title="Titanic Modified", explorative=True, external_properties=ext_properties2)
        return profile1, profile2

    # Function to generate a random 8-character string
    @staticmethod
    def generate_random_string(length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def compare_profiles(profile1: ProfileReport, profile2: ProfileReport):
        return compare([profile1, profile2])

    @staticmethod
    def save_comparison_to_temp_html(comparison_report):
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, "titanic_comparison_report.html")
        comparison_report.to_file(output_path)
        return output_path

def main():
    demo = DemoYData()
    df1 = demo.load_sample_data()
    df2 = demo.modify_data(df1)
    df1["password"] = [demo.generate_random_string() for _ in range(len(df1))]
    df2["password"] = [demo.generate_random_string() for _ in range(len(df2))]
    df1.loc[:199, "password"] = "password"
    df2.loc[df2.index[-30:], "password"] = np.nan

    profile1, profile2 = demo.generate_profiles(df1, df2)
    comparison = demo.compare_profiles(profile1, profile2)
    result_path = demo.save_comparison_to_temp_html(comparison)
    print(f"✅ Comparison report saved to: {result_path}")

if __name__ == "__main__":
    main()
