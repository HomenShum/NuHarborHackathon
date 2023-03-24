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
    tokens=500, # Limit the output to 256 tokens so that the completion is not too wordy
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

def summarize_gpt_completion(content):
    prompt = f"Look through the contents and state a common name that is adaptable across all cybersecurity protection services. Then in 100 words, concisely summarize the alerts into one alert:\n{content}\n The format should be as follows:\n\nCommon Name: <Name>\nSummary: <Summary>\n"

    retries = 3
    for attempt in range(retries):
        try:
            summary = gpt_completion(prompt)  # Using GPT-3.5-turbo chat completion
            print (summary)
            return summary
        except openai.error.APIError as e:
            if attempt < retries - 1:  # if this is not the last attempt
                print(f"APIError occurred: {e}. Retrying...")
                sleep(5)  # wait for 5 seconds before retrying
            else:
                raise

# Summarize the contents of the "MS Summary" and "CS Summary" columns
df['Summary'] = df.apply(lambda row: summarize_gpt_completion(str(row['MS Summary']) + ' ' + str(row['CS Summary'])), axis=1)

df.to_excel(filepath, index=False)

print("Excel file updated with GPT completions and summaries!")
