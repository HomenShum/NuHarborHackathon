import glob
import json
import pandas as pd
import re
from time import sleep
import openai
import tenacity

json_files = glob.glob('hackathon-solution/All/*.json')
filepath = r'hackathon-solution\Key.xlsx'

# Read the Excel file
df = pd.read_excel(filepath)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai.api_key = open_file('openaiapikey.txt')

@tenacity.retry(
    stop=tenacity.stop_after_delay(30),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=30),
    retry=tenacity.retry_if_exception_type(openai.error.APIError),
    reraise=True,
)
def gpt_completion(
    prompt,
    engine="gpt-3.5-turbo",
    temp=0, # set at 0 to ensure consistent completion, increase accuracy along with UUID
    top_p=1.0,
    tokens=256, # Limit the output to 256 tokens so that the completion is not too wordy
    freq_pen=0.25,
    pres_pen=0.0,
    stop=["<<END>>"],
):
    prompt = prompt.encode(encoding="ASCII", errors="ignore").decode()
    response = openai.ChatCompletion.create(
        model=engine,
        messages=[
            {"role": "system", "content": "Your task is to help summarize cybersecurity alerts from different vendors."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=tokens,
        temperature=temp,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop,
    )
    text = response["choices"][0]["message"]["content"].strip()
    text = re.sub("\s+", " ", text)
    return text

def generate_gpt_completion(json_file):
    with open(json_file, 'r') as f:
        raw_content = f.read()

    prompt = f"Limit to 250 tokens. State the Name, and create a concise cybersecurity ontology about attack vectors and vulnerabilities for the following JSON content:\n{raw_content}\n"

    retries = 3
    for attempt in range(retries):
        try:
            completion = gpt_completion(prompt)  # Using GPT-3.5-turbo chat completion
            return completion
        except openai.error.APIError as e:
            if attempt < retries - 1:  # if this is not the last attempt
                print(f"APIError occurred: {e}. Retrying...")
                sleep(5)  # wait for 5 seconds before retrying
            else:
                raise


def update_excel_file(json_file, df):
    with open(json_file, 'r') as f:
        data = json.load(f)

    completion = generate_gpt_completion(json_file)  # Generate GPT completion
    data["GPT Summary"] = completion
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    if json_file.endswith("MS.json"):
        column_name = "MS Summary"
    elif json_file.endswith("CS.json"):
        column_name = "CS Summary"
    else:
        print(f"File {json_file} has an unsupported extension.")
        return

    def clean_value(value):
        # Remove any non-alphanumeric characters from the value
        return re.sub('[^0-9a-zA-Z]+', '', str(value))

    for index, row in df.iterrows():
        for column in ['Microsoft', 'CrowdStrike']:
            current_value = row[column]
            if current_value is not None and not pd.isnull(current_value):
                current_value_clean = clean_value(current_value)
                completion_clean = clean_value(completion)

                if current_value_clean.lower() in completion_clean.lower():
                    df.loc[index, column_name] = completion  # Update the GPT completion to the specified column

    # Write to the excel file
    df.to_excel(filepath, index=False)

    print(f"Updated GPT completion for {json_file}")
    print(completion)

# Process all JSON files
for json_file in json_files:
    update_excel_file(json_file, df)

print("Excel file updated with GPT completions!")


"""
--- DESCRIPTION ---

The python file is used to generate the completion data for the JSON files.
There are two summaries generated, one from Microsoft and one from CrowdStrike.
Then, a "Summary" column combines the two summaries using gpt-3.5-turbo.

"""