from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class QueryParser:
    """Tokenize the user's query.

    We use python nltk library to tokenize and clean user's query.
    """
    @staticmethod
    def parse(query):
        """Tokenize and clean user's query.

        Args:
            query: an user's input string.

        Returns:
            a set of tokenized words.
        """
        result = set([])
        stop_words = set(stopwords.words("english"))
        for word in word_tokenize(query):
            if word not in stop_words:
                result.add(word)
        return result

