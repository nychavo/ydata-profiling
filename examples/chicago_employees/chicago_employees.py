from pathlib import Path

import pandas as pd, json
import pickle
from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file
from ydata_profiling.config import Settings

if __name__ == "__main__":


    script_dir = Path(__file__).parent  # examples/chicago_employees/
    json_path = script_dir / "employee_data_properties.json"
    with open(json_path, "r", encoding="utf-8") as f:
        external_properties = json.load(f)

    file_name = cache_file(
        "chicago_employees.csv",
        "https://data.cityofchicago.org/api/views/xzkq-xp2w/rows.csv?accessType=DOWNLOAD",
    )

    df = pd.read_csv(file_name)

    config = Settings()
    config.variables.descriptions = {
        "name": "Full name of the employee",
        "job_titles": "Official job title",
        "department": "Department where the employee works",
        "annual_salary": "Annual salary in USD",
    }
    config.progress_bar = True


    profile = ProfileReport(df, title="Chicago Employees", explorative=True, config=config
                            , external_properties=external_properties)
    profile.to_file(Path(f"{script_dir}/chicago_employees_report.html"))
    pass
