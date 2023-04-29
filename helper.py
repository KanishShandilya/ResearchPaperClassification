import re
import string
def preprocess(text):
    text=re.sub(r'\n', ' ', text)
    text=re.sub(r'-', ' ', text)
    text=re.sub(r'\s+', ' ', text)
    text=re.sub(r'\([A-za-z\d]*\)', '', text)
    text=text.strip()
    text="".join([i for i in text if i not in string.punctuation])
    text=text.lower()
    return text