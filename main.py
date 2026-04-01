
from fastapi import FastAPI, Query
import pandas as pd
from typing import List

app = FastAPI()

try:
    df = pd.read_csv(r"C:\Users\sanga\Downloads\archive (7)\A_Z_medicines_dataset_of_India.csv")
    # Pre-process: ensure medicine names are strings and handle missing values
    medicine_list = df['name'].dropna().astype(str).tolist()
except FileNotFoundError:
    medicine_list = []
    print("Error: 'medicines.csv' not found. Please ensure the file exists.")

@app.get("/suggestions")
def get_suggestions(q: str = Query(..., min_length=1)):
    """
    Returns a list of medicine names that match the query 'q'.
    """
    query = q.lower()

    # Filter: find medicines that START with the query or CONTAIN the query
    # We prioritize 'starts with' for better UX in suggestions
    starts_with = [m for m in medicine_list if m.lower().startswith(query)]
    contains = [m for m in medicine_list if query in m.lower() and not m.lower().startswith(query)]

    # Combine and limit results to top 10
    suggestions = (starts_with + contains)[:10]

    return {"query": q, "suggestions": suggestions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
