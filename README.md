# Project Solution Documentation

## **1. Project Overview**
The goal of this project was to extract article text from a list of URLs, analyze the text using various sentiment and readability metrics, and output the results in an Excel file. The analysis includes computing sentiment scores, readability indices, and text statistics such as word count, syllable count, and personal pronoun counts.

---

## **2. Approach to the Solution**

### **2.1. Directory Structure**
To maintain clarity and organization, the project follows the directory structure shown below:

```
Test Assignment/
├── Input.xlsx                      # Input file with URLs and unique IDs
├── MasterDictionary/               # Directory containing sentiment word lists
│   ├── positive-words.txt
│   ├── negative-words.txt
├── StopWords/                      # Directory containing various stopword lists
│   ├── StopWords_Auditor.txt
│   ├── StopWords_Currencies.txt
│   ├── StopWords_DatesandNumbers.txt
│   ├── StopWords_Generic.txt
│   ├── StopWords_GenericLong.txt
│   ├── StopWords_Geographic.txt
│   ├── StopWords_Names.txt
├── Extracted Text/                 # Directory for storing extracted text files
│   ├── <URL_ID>.txt                # Extracted text for each URL
├── Output.xlsx                     # Final output file
├── app.py                          # Main program file
├── helper.py                       # Helper functions for modularity
├── requirements.txt                # Python dependencies
├── README.md                       # Project readme file
└── .gitignore                      # Git ignore file
```

### **2.2. Data Loading**
- The project starts by loading an Excel file (`Input.xlsx`) containing URLs and unique IDs.
- We use the `pandas` library for efficient data management.

```python
import pandas as pd
# Load Excel file
data = pd.read_excel(r'Test Assignment/Input.xlsx')
```

### **2.3. Text Extraction**
- We used the `requests` library to fetch webpage content.
- `BeautifulSoup` from `bs4` was used for HTML parsing.
- Text was extracted from key HTML tags such as `<p>` and `<li>`.

```python
from bs4 import BeautifulSoup
import requests

def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract title and text
    title = soup.find('h1', class_='entry-title').get_text(strip=True) if soup.find('h1', 'entry-title') else 'No Title'
    article_text = ' '.join(p.get_text(strip=True) for p in soup.find_all(['p', 'li']))
    return f"Title: {title}\nArticle Text: {article_text}"
```

---

### **2.4. Text Cleaning**
- Text was cleaned by:
  - Removing special characters and numbers using `re`.
  - Tokenizing using `nltk.word_tokenize()`.
  - Removing stopwords from a custom list and NLTK’s default list.

```python
import re
import nltk
from nltk.corpus import stopwords

def clean_text(text, stop_words):
    text = re.sub(r'[^a-zA-Z]', ' ', text).lower()
    words = nltk.word_tokenize(text)
    cleaned_words = [word for word in words if word not in stop_words]
    return cleaned_words
```

---

### **2.5. Sentiment and Readability Metrics Calculation**
We computed the following metrics based on the cleaned text:

- **Sentiment Analysis**:
  - Positive Score: Count of positive words from a custom dictionary.
  - Negative Score: Count of negative words.
  - Polarity Score: Calculated using:
    ```python
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    ```
  - Subjectivity Score:
    ```python
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)
    ```

- **Readability Metrics**:
  - Average Sentence Length: Total words / number of sentences.
  - Percentage of Complex Words:
    ```python
    percentage_complex_words = (complex_word_count / total_words) * 100
    ```
  - Fog Index:
    ```python
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words / 100)
    ```

- **Text Statistics**:
  - Average Number of Words per Sentence.
  - Complex Word Count (words with more than two syllables).
  - Word Count, Syllable Count per Word, and Personal Pronouns Count.

---

### **2.6. Saving the Results**
- We used `pandas` to create and save a well-formatted Excel output file.

```python
output.to_excel('Output.xlsx', index=False)
print("Processing completed!")
```

---

## **3. Challenges and Solutions**

### **Challenge 1: Missing Text from Some Websites**
- **Solution:** Added support for multiple HTML tags such as `<div>`, `<p>`, and `<li>`.

### **Challenge 2: Handling Encoding Issues**
- **Solution:** Used UTF-8 encoding while saving text files.

### **Challenge 3: Inconsistent Data Formats**
- **Solution:** Added error handling and default values for missing data.

---

## **4. Libraries and Tools Used**
- **Libraries:**
  - `pandas`: For data manipulation and saving results.
  - `requests`: For webpage fetching.
  - `BeautifulSoup`: For HTML parsing.
  - `nltk`: For text tokenization and stopword removal.
  - `re`: For regular expressions.
  - `textstat`: For readability metrics.

---

## **5. Steps to Run the Project**

### **Prerequisites**
- Install Python 3.8 or higher.
- Install required libraries using:

```bash
pip install -r requirements.txt
```

### **Execution**
1. Place all input files in the `Test Assignment` directory.
2. Run the program:

```bash
python app.py
```
3. The results will be saved in `Output.xlsx` and extracted text files will be stored in the `Extracted Text` directory.

---

## **6. Summary**
This project efficiently extracts, processes, and analyzes textual data from web pages using modern text processing techniques. By integrating sentiment analysis, readability metrics, and word statistics, the program generates valuable insights and outputs them in an Excel file.

---

**Note:** Ensure all required files are in the correct directory before running the program. Adjust file paths as necessary based on your system.

---