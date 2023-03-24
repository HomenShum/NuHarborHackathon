# Master Process Flow - Homen Shum

> The goal is to **create a model that learns from the alerts** what the equivalent alert is in Microsoft Defender for Endpoint vs in CrowdStrike Falcon. The **anticipated result** is the common ontology, or common **language to refer to and describe the same alert from different vendors.**
> 
1. Data Cleansing: Removed irrelevant keys from the JSON strings in All folder, 14 files did not have JSON at the end of them so I manually added the “.json”
2. Generation Task 1: Generated and appended UUIDs for each pair of keys in the key.xlsx file.
3. Generation Task 2: GPT 3.5 turbo with prompt-engineering generated training/ideal output/completion data composed of Common Name and Summary description using the JSON content from the 192 json files in "All" folder. They are appended to the corresponding rows as the alert pairs in key.xlsx by matching the json's alert event name/type/category/etc. to the event names on the key.xlsx.
4. Final Step: All_CS.json and All_MS.json files is updated with key.xlsx values by appending the UUID and summary from key.xlsx to the end of JSON.

Now that the result shows the key.xlsx file can be used to append the corresponding common ontology to each alert event JSON object in All CS and All MS json files, the future alerts that matches the existing data/alert pairing will be easily paired with the common ontology - which is what we are looking for based on the hackathon prompt.

Result so far, all of the alert event contents in each dictionary within the All-CS and All-MS json files can be paired with the common ontology/completion via the updated key.xlsx. It costed less than $1. This solution is only for the 192 alert event types for CS and MS, which is suited specifically for the hackathon.

Side Notes:
- Semantic Search was not necessary, it took longer and was not generating better result than a simple key word match program.
- Prompt-Engineering was the main contributor to the result.
- Will upload the All, All-CS, and All-MS folders to google drive 

# Original Prompt
Hello and welcome to the coding part of the challenge.  This will be your guide for working with the data. Please reach out via the Discord channel if you have any questions or issues

There are two zipped files at this link:
https://drive.google.com/drive/folders/1vE_OHbpvNBNKMwv7938f3YZr7NWG4JlO?usp=share_link

All-CS.zip is all of the test/training data for CrowdStrike Falcon. The individual alerts are json objects and the file is a collection of those objects.  The file itself doesn't have a top level elelemt so itself it is not a valid jsob object

All-MS.zip is all of the test/training data for Microsoft Defender for Endpoint. The individual alerts are json objects and the file is a collection of those objects.  The file itself doesn't have a top level elelemt so itself it is not a valid jsob object

All alerts are key value pairs.  The exact format vaires from alert to alert but all alerts within each vendor do have a consistent set of core elecments 

key.xls shows the correct mapping of Microsoft Defender for Endpoiont alerts to CrowdStrike Falcon alerts

The MS.zip folder contains one version each of the indiviudal alerts for Microsoft Defender for Endpoint. Each alert has it's own json file. 

The CS.zip folder contains one version each of the indiviudal alerts for CrowdStrike Falcon. Each alert has it's own json file. 

Notes:
The alerts were generated and manipulated for the hackathon. You should not make any inferences about the distributiuon patterns. There is no logic to that and in the real-world the distribution is unpredicitable and will vary from organization to organization

Ignore all time stamps and event_id or AlertID's. There is no logic to them and no correlation to the ID's and the meaning of any alert. `

Becuase there was manual manipulation in creating the events, it's possible there are human errors, ie spelling or duplicate or missing info. These should be at a very minimum number

The intent is for this to be an NLP solution however it is possible some inferences and predictions can be made from the fomrat and/or structure of the alerts. It's also possible you will need multiple layers and/or a fine tuning layer on top of the core model 

In either case the goal is to create a model that learns from the alerts what the equivalent alert is in Microsoft Defender for Endpoint vs in CrowdStrike Falcon. The anticipated result is the common ontology, or common langauge to refer to and describe the same alert from different vendors 
