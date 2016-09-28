from collections import defaultdict


class AdIndex:
    """An ad index supports fast ads lookup.

    It has two components: a forward index and an inverted index. The forward index is used
    to fast retrieve ad by id. The inverted index is used to fast retrieve ad by keyword.

    Attributes:
        forward_index: a dict whose key is ad.id. Value is the ad.
        inverted_index: a dict whose key is a keyword. Value is a set of ads.
    """
    def __init__(self):
        self.forward_index = {}
        self.inverted_index = defaultdict(set)

    def add_ad(self, ad):
        """Add an ad to forward index and inverted index.

        Args:
            ad: an ad object.

        Returns:
            None
        """
        self.forward_index[ad.id] = ad
        for keyword in ad.keywords:
            self.inverted_index[keyword.lower()].add(ad)
        return

    def fetch_ads_by_word(self, word):
        """Given a word, fetch ads in inverted_index.

        Args:
            word: a key word string.

        Returns:
            a set of ads.
        """
        return self.inverted_index[word.lower()]
