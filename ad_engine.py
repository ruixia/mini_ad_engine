from ad import Ad
from ad_selector import AdSelector
from ad_filter import AdFilter
from ad_ranker import AdRanker
from ad_pricing import AdPricing
from ad_index import AdIndex
from query_parser import QueryParser
from sample_data import ADS


class AdEngine:
    """A class provides public APIs to serve ads.

    Attributes:
        ad_index: an ad index object.
    """
    def __init__(self):
        self.ad_index = AdIndex()
        for data in ADS:
            ad = Ad(data["id"], data["keywords"],
                    data["bid_price"], data["click_probability"], data["budget"])
            self.ad_index.add_ad(ad)

    def fetch_ad(self, query):
        """Fetch an ad based on user's query.

        Args:
            query: an user's input string.

        Returns:
            An targeted relevant ad.
        """
        tokenized_words = QueryParser.parse(query)
        if not tokenized_words: return None

        relevant_ads = AdFilter.filter(AdSelector.select(tokenized_words, self.ad_index))
        if not relevant_ads: return None

        top_3_relevant_ads = AdRanker.fetch_top_k_relevant_ads(relevant_ads, 3)
        return AdPricing.charge_target_ad(top_3_relevant_ads)


if __name__ == "__main__":
    engine = AdEngine()
    relevant_ad = engine.fetch_ad("Nike basketball shoe")
    print(relevant_ad)