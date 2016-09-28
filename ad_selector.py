from collections import defaultdict
from ad import RelevantAd


class AdSelector:
    """An ad selector object."""

    @staticmethod
    def select(tokenized_words, ad_index):
        """Select ads based on a set of tokenized words.

        We return a list of relevant ads with their corresponding relevance score,
        quality score and rank score.

        The relevance score calculation is simplified. The equation is:
        relevance_score = number of ad matched words / total number of words in key words

        Args:
            tokenized_words: a set of tokenized words.
            ad_index: an ad index object.

        Returns:
            A list of relevant ads.
        """
        result = []
        count_match = defaultdict(int)
        word_size = len(tokenized_words)

        for word in tokenized_words:
            ads = ad_index.fetch_ads_by_word(word)
            for ad in ads:
                count_match[ad] += 1

        for ad, count in count_match.items():
            result.append(RelevantAd(ad, count/float(word_size)))

        return result
