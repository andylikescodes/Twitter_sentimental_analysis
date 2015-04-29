import re
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords

class DataProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.retokenizer = RegexpTokenizer("[\w]+")
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'
        self.english_stops = set(stopwords.words('english'))

    # a function to get the lemma of the words 
    def lemmatize(self, word):
        return self.lemmatizer.lemmatize(word)

    # get the stem of the word
    def stem(self, word):
        return self.stemmer.stem(word)
    # regular expression tokenizer
    def reTokenize(self, string):
        return self.retokenizer.tokenize(string)

    # replace words with repeated letters
    def RepeatReplace(self, word):
        if wordnet.synsets(word):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)

        if repl_word != word:
            return self.RepeatReplace(repl_word)
        else:
            return repl_word

    # Process original tweets into feature process ready tweets
    def processTweet(self, tweets):
        processed_tweet = []
        processed_tweet_collection = []
        for tweet in tweets:
            tokenized_tweet = self.reTokenize(tweet)
            for word in tokenized_tweet:
                word = self.RepeatReplace(word)
                word = self.lemmatize(word)
                if word not in self.english_stops and len(word)>1:
                    processed_tweet.append(word)
            processed_tweet_collection.append(processed_tweet)
            processed_tweet = []
        return processed_tweet_collection

    # get rid of special characters of a tweet
    def cleanSpecialChar(self, data):
        specialChar = '#$%^&*()_+-={}|[]\\:\"<>/'
        data = re.sub(r'[^\x00-\x7f]',r'', data)
        wordList = data.lower().split()
        wordHolder=[]
        for word in wordList:
            if '@' in word or 'http:' in word or '.com' in word:
                pass
            else:
                for i in range(0, len(specialChar)):
                    word = word.replace(specialChar[i],"")
                if len(word) > 0:
                    wordHolder.append(word)
        clean = " ".join(wordHolder)
        return clean




