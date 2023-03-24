import uuid
import pandas as pd

def generate_UUID(filepath):
    df = pd.read_excel(filepath)
    df['UUID'] = df.apply(lambda x: uuid.uuid4(), axis=1)
    df.to_excel(filepath, index=False)

# Generate UUID for all rows in the excel under the UUID column
filepath = r'hackathon-solution\Key.xlsx'
generate_UUID(filepath)