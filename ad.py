from constants import (
    CLICK_WEIGHT,
    RELEVANCE_WEIGHT,
)


class Ad:
    """An ad object.

    Attributes:
        id: an unique identifier.
        keywords: a list of keywords this ad targets on.
        bid_price: the highest price advertisers are willing to pay.
        click_probability: it defines how likely the audience will click the ad. This value
            should be user centric and calculated by some advanced machine learning algorithms.
            For simplification, we hard code the value.
        budget: the budget advertiser set to run the ad.
    """
    def __init__(self, id, keywords, bid_price, click_probability,
                 budget):
        self.id = id
        self.keywords = keywords
        self.bid_price = bid_price
        self.click_probability = click_probability
        self.budget = budget

    def charge(self, price):
        """Charge the price from the budget.

        The charge price can be different from and usually is lower than bid_price.

        Attributes:
            price: the money charged.

        Returns:
            A boolean indicating whether the charge succeeded.
        """
        if price > self.budget:
            return False
        self.budget -= price
        return True


class RelevantAd:
    """An ad object decorated with a relevant score, quality score and a rank score.

    When select ads from the ad index, we calculate a relevance score of the ad.
    We use relevance score and click_probability to get a quality score.
    The quality score is used to filter out unqualified ads. At rank stage, we provide a
    rank score to the ad. We use rank score to get/charge the target ad.

    Attributes:
        relevance_score: it defines how relevant the ad is with the user's query.
        quality_score: it defines the quality of the ad. We use the following formula for calculation:
            quality_score = (CLICK_WEIGHT * click_probability +
                              RELEVANCE_WEIGHT * relevance_score)
        rank_score: we use this number to get/charge the target ad.  Its calculation is:
            rank_score = quality_score * bid_price
    """
    def __init__(self, ad, relevance_score):
        self.ad = ad
        self.relevance_score = relevance_score
        self.quality_score = (CLICK_WEIGHT * self.ad.click_probability +
                              RELEVANCE_WEIGHT * self.relevance_score)
        self.rank_score = self.quality_score * self.ad.bid_price

    def __str__(self):
        return "id:{id}, relevance_score:{relevance_score}, rank_score:{rank_score}".format(
            id=self.ad.id, relevance_score=self.relevance_score, rank_score=self.rank_score)