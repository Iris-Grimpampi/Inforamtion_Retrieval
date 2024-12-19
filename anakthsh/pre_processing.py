import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Αρχικοποίηση για Stop-words
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Συνάρτηση για προεπεξεργασία του κειμένου
def preprocess_text(text):
    # Αφαίρεση ειδικών χαρακτήρων (μόνο γράμματα και αριθμοί)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    # Tokenization: Διάσπαση κειμένου σε λέξεις
    tokens = word_tokenize(text)
    # Αφαίρεση stop-words
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return filtered_tokens
