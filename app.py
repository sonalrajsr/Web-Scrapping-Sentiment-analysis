import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
import re
import os
from nltk.corpus import stopwords
from textstat import textstat

# Load Excel File
data = pd.read_excel(r'Test Assignment/Input.xlsx')

# Initialize NLTK modules
nltk.download('punkt_tab')
nltk.download('stopwords')

# Define Functions
def extract_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract Title
        title = soup.find('h1', class_='entry-title').get_text(strip=True)

        # Extract Article Text
        content = soup.find('div', class_='td-post-content')
        paragraphs = content.find_all('p') if content else []
        article_text = ' '.join(p.get_text(strip=True) for p in paragraphs)

        return title + '\n' + article_text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return ""

def clean_text(text, stop_words):
    text = re.sub(r'[^a-zA-Z]', ' ', text).lower()
    words = nltk.word_tokenize(text)
    cleaned_words = [word for word in words if word not in stop_words]
    return cleaned_words

def load_word_dict(file_path):
    try:
        with open(file_path, 'r') as file:
            words = {line.strip().lower() for line in file.readlines()}
            return words
    except FileNotFoundError:
        print(f"Dictionary file {file_path} not found.")
        return set()

# Load Stop Words from Multiple Files
stop_words = set(stopwords.words('english'))
stopword_files = [
    'Test Assignment\StopWords\StopWords_Auditor.txt',
    'Test Assignment\StopWords\StopWords_Currencies.txt',
    'Test Assignment\StopWords\StopWords_DatesandNumbers.txt',
    'Test Assignment\StopWords\StopWords_Generic.txt',
    'Test Assignment\StopWords\StopWords_GenericLong.txt',
    'Test Assignment\StopWords\StopWords_Geographic.txt',
    'Test Assignment\StopWords\StopWords_Names.txt'
]

# Load each stopword file
for file_path in stopword_files:
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            custom_words = {line.strip().lower() for line in file.readlines()}
            stop_words.update(custom_words)
    else:
        print(f"File {file_path} not found.")

# Load Positive and Negative Words
positive_words = load_word_dict('Test Assignment/MasterDictionary/positive-words.txt')
negative_words = load_word_dict('Test Assignment/MasterDictionary/negative-words.txt')

# Create Output DataFrame
output = pd.DataFrame(columns=[
    'URL_ID', 'POSITIVE_SCORE', 'NEGATIVE_SCORE', 'POLARITY_SCORE', 
    'SUBJECTIVITY_SCORE', 'AVG_SENTENCE_LENGTH', 'COMPLEX_WORD_COUNT', 
    'WORD_COUNT', 'SYLLABLE_PER_WORD', 'PERSONAL_PRONOUNS', 'AVG_WORD_LENGTH',
    'FOG_INDEX'
])

# Calculate number of syllables in a word
def syllable_count(word):
    word = word.lower()
    syllables = 0
    vowels = "aeiou"
    if word in ['es', 'ed']:  # Exclude words ending in "es" or "ed"
        return 0
    for char in word:
        if char in vowels:
            syllables += 1
    return syllables

# Process Each URL
for index, row in data.iterrows():
    url_id, url = row['URL_ID'], row['URL']
    text = extract_article_text(url)
    if text:
        # Save extracted text
        with open(f"Test Assignment/Extracted Text/{url_id}.txt", 'w', encoding='utf-8') as file:
            file.write(text)
        
        # Clean text and compute metrics
        cleaned_words = clean_text(text, stop_words)

        # Calculate sentiment scores
        positive_score = sum(1 for word in cleaned_words if word in positive_words)
        negative_score = sum(1 for word in cleaned_words if word in negative_words)
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)

        # Readability metrics
        num_sentences = len(re.findall(r'\.', text))  # Simple sentence count by period
        avg_sentence_length = len(cleaned_words) / num_sentences if num_sentences > 0 else 0
        complex_word_count = sum(1 for word in cleaned_words if syllable_count(word) > 2)
        total_words = len(cleaned_words)
        syllable_per_word = sum(syllable_count(word) for word in cleaned_words) / total_words if total_words > 0 else 0
        personal_pronouns = sum(1 for word in cleaned_words if word in ['i', 'we', 'my', 'ours', 'us'])
        avg_word_length = sum(len(word) for word in cleaned_words) / total_words if total_words > 0 else 0
        fog_index = 0.4 * (avg_sentence_length + (complex_word_count / total_words)) if total_words > 0 else 0

        # Populate output DataFrame
        output = pd.concat([output, pd.DataFrame([{
            'URL_ID': url_id,
            'POSITIVE_SCORE': positive_score,
            'NEGATIVE_SCORE': negative_score,
            'POLARITY_SCORE': polarity_score,
            'SUBJECTIVITY_SCORE': subjectivity_score,
            'AVG_SENTENCE_LENGTH': avg_sentence_length,
            'COMPLEX_WORD_COUNT': complex_word_count,
            'WORD_COUNT': total_words,
            'SYLLABLE_PER_WORD': syllable_per_word,
            'PERSONAL_PRONOUNS': personal_pronouns,
            'AVG_WORD_LENGTH': avg_word_length,
            'FOG_INDEX': fog_index
        }])], ignore_index=True)

# Save Final Output
output.to_excel('Output.xlsx', index=False)
print("Processing completed!")
