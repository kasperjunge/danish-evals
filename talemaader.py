import requests
import fitz  
import pandas as pd
import re
import datasets

# download pdf
pdf_url = 'https://www.overlevelsesguiden.dk/files/annes_liste_over_talemaader.pdf'
response = requests.get(pdf_url)

# Save pdf
pdf_path = '/content/doc.pdf'
with open(pdf_path, 'wb') as f:
    f.write(response.content)

# load pdf text
doc = fitz.open(pdf_path)

## clean
all_rows = []

# trim pages
all_rows += doc[0].get_text().split("\n")[:-5] # special for first page
all_rows += doc[1].get_text().split("\n")[:-3]
all_rows += doc[2].get_text().split("\n")[:-3]
all_rows += doc[3].get_text().split("\n")[:-3]
all_rows += doc[4].get_text().split("\n")[:-3]
all_rows += doc[5].get_text().split("\n")[:-3]
all_rows += doc[6].get_text().split("\n")[:-3]
all_rows += doc[7].get_text().split("\n")[:-3]
all_rows += doc[8].get_text().split("\n")[:-3]

# special handling of last page
last_page = doc[9].get_text().split("\n")[-20:][:-9]
last_page_ØÆ = last_page[-4:]
last_page = last_page[:-4]
manual_ØÆ = [
    "Æ",
    "Æblet falder ikke langt fra stammen", 
    "Man ligner eller gør som sine forældre",
    "Ø",
    "Ønske nogen hen hvor peberet gror",
    "Slippe for en besværlig person"
]
all_rows += last_page
all_rows += manual_ØÆ

# filter all index letters
all_rows = [x for x in all_rows if len(x) != 1]

# organize data
expressions, meanings = [], []
for i, x in enumerate(all_rows):
  if (i % 2) == 0:
    expressions.append(x)
  else:
    meanings.append(x)

# convert to dataframe
df = pd.DataFrame(data={"expression": expressions, "meaning": meanings})

# convert dataset to hugging face
ds = datasets.Dataset.from_pandas(df)

# upload to hugging face
huggingface_token = "..."
ds.push_to_hub(repo_id="Juunge/danske-talemaader", token=huggingface_token)
