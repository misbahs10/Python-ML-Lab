from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pandas as pd #type: ignore

class CSVInfoInput(BaseModel):
    """Input schema for CSVInfoTool."""
    file_path: str = Field(..., description="Path to the CSV file that needs to be annalyzed.")

class CSVInfoTool(BaseTool):
    """Tool to analyze CSV file and provides basic information about it."""
    name: str = "CSV Info Tool"
    description: str = """
    Reads a CSV file and provides basic information about the dataset.

    It includes:
    - Number of rows
    - Number of columns
    - Column names
    - Data types
    - Missing values
    - Duplicate rows
    """
    args_schema: Type[BaseModel] = CSVInfoInput

    def _run(self, file_path: str) -> str:
        df = pd.read_csv(file_path)
        result = f"""
Dataset Information:

Number of rows: {len(df)}
Number of columns: {len(df.columns)}

Column names:
{list(df.columns)}

Data types:
{df.dtypes.to_string()}

Missing values:
{df.isnull().sum().to_string()}

Duplicate rows:
{df.duplicated().sum()}
"""
        return result