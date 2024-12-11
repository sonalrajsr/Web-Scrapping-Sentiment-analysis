## Overview
This project extracts article texts from URLs provided in an Excel file, performs text analysis, and computes various metrics such as sentiment scores, readability indices, and word statistics. The results are saved in an Excel file (`Output.xlsx`).

---

## Project Structure
- **Input File:** `Test Assignment/Input.xlsx`
- **Stopwords Files:** Located in `Test Assignment/StopWords/`
- **Master Dictionary Files:** `positive-words.txt`, `negative-words.txt`
- **Output Directory:** Extracted text files saved in `Test Assignment/Extracted Text/`

---

## Dependencies
The following Python libraries are required:
- `pandas`
- `requests`
- `BeautifulSoup` from `bs4`
- `nltk`
- `re`
- `os`
- `textstat`

Run the following command to install required libraries:
```bash
pip install pandas requests beautifulsoup4 nltk textstat
```

---

## Steps and Function Descriptions

### 1. Load Excel File
```python
data = pd.read_excel(r'Test Assignment/Input.xlsx')
```
Loads the input Excel file containing URLs.

### 2. Initialize NLTK Modules
```python
nltk.download('punkt_tab')
nltk.download('stopwords')
```
Downloads necessary NLTK resources for text processing.

### 3. Extract Article Text
```python
def extract_article_text(url):
```
- Extracts the article title and text from the URL.
- Collects text from `<p>` and `<li>` tags.
- Cleans and consolidates the text.

### 4. Clean Text
```python
def clean_text(text, stop_words):
```
- Removes non-alphabetic characters.
- Tokenizes text using NLTK.
- Removes stopwords from the tokenized list.

### 5. Load Word Dictionaries
```python
def load_word_dict(file_path):
```
- Loads words from specified dictionary files.
- Returns a set of words for positive and negative sentiment analysis.

### 6. Load Stop Words
```python
stopword_files = [ ... ]
```
- Loads custom stopword lists from provided files.
- Combines all stopwords into a single set.

### 7. Calculate Syllables
```python
def syllable_count(word):
```
- Counts vowels in a word.
- Excludes words ending in "es" or "ed."

### 8. Process Each URL
The program processes each URL by performing the following steps:
- Extracts and saves the article text.
- Cleans the text.
- Computes sentiment scores:
  - **Positive Score:** Count of positive words.
  - **Negative Score:** Count of negative words.
  - **Polarity Score:**
    ```python
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    ```
  - **Subjectivity Score:**
    ```python
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)
    ```
- Computes readability metrics:
  - **Average Sentence Length:** Total words divided by number of sentences.
  - **Complex Word Count:** Words with more than two syllables.
  - **Syllable per Word:** Average syllables per word.
  - **Personal Pronouns Count:** Count of personal pronouns like 'I,' 'we,' 'my.'
  - **Average Word Length:** Average length of words in the text.
  - **Fog Index:**
    ```python
    fog_index = 0.4 * (avg_sentence_length + (complex_word_count / total_words))
    ```

### 9. Save Results
```python
output.to_excel('Output.xlsx', index=False)
```
Saves the computed metrics in an Excel file named `Output.xlsx.`

---

## Execution
Run the script using:
```bash
python text_analysis.py
```

---

## Notes
- Ensure that all required files are in the correct directory.
- Verify internet connectivity for URL extraction.
- Use appropriate file paths according to your directory structure.

---
