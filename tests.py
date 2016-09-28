from unittest import TestCase
from sample_data import ADS
from ad import (
    Ad,
    RelevantAd,
)
from constants import (
    CLICK_WEIGHT,
    RELEVANCE_WEIGHT
)
from ad_filter import AdFilter
from ad_index import AdIndex
from ad_selector import AdSelector
from ad_ranker import AdRanker
from ad_engine import AdEngine


class BaseTestCase(TestCase):

    def setUp(self):
        self.ads = []
        for data in ADS:
            ad = Ad(data["id"], data["keywords"],
                    data["bid_price"], data["click_probability"], data["budget"])
            self.ads.append(ad)


class TestAd(BaseTestCase):

    def test_charge_failed(self):
        ad = self.ads.pop()
        ad.budget = -1
        self.assertFalse(ad.charge(1))

    def test_charge_succeed(self):
        ad = self.ads.pop()
        ad.budget = 100
        self.assertTrue(ad.charge(1))


class TestRelevantAd(BaseTestCase):

    def test_init(self):
        ad = self.ads.pop()
        relevant_ad = RelevantAd(ad, 1)
        self.assertEqual(relevant_ad.relevance_score, 1)
        quality_score = (CLICK_WEIGHT * relevant_ad.ad.click_probability +
                         RELEVANCE_WEIGHT * 1)
        self.assertEqual(relevant_ad.quality_score, quality_score)
        self.assertEqual(relevant_ad.rank_score, relevant_ad.quality_score * relevant_ad.ad.bid_price)


class TestAdFilter(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.relevant_ad = RelevantAd(self.ads.pop(), 0)

    def test_relevance_score_is_not_met(self):
        self.assertEqual(len(AdFilter.filter([self.relevant_ad])), 0)

    def test_click_probability_is_not_met(self):
        self.relevant_ad.ad.click_probability = 0
        self.assertEqual(len(AdFilter.filter([self.relevant_ad])), 0)

    def test_one_failed_to_meet_criteria(self):
        ad0, ad1 = self.ads[0], self.ads[1]
        relevant0 = RelevantAd(ad0, 1)
        relevant1 = RelevantAd(ad1, 0)

        self.assertEqual(len(AdFilter.filter([relevant0, relevant1])), 1)


class TestAdIndex(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.ad_index = AdIndex()

    def test_add_ad(self):
        ad = self.ads.pop()
        self.assertIsNone(self.ad_index.add_ad(ad))
        self.assertEqual(self.ad_index.forward_index[ad.id], ad)
        self.assertEqual(len(self.ad_index.forward_index), 1)
        self.assertEqual(len(self.ad_index.inverted_index), len(ad.keywords))
        for keyword in ad.keywords:
            self.assertIn(ad, self.ad_index.inverted_index[keyword.lower()])

    def test_fetch_ads_by_word(self):
        for ad in self.ads:
            self.ad_index.add_ad(ad)

        self.assertEqual(len(self.ad_index.fetch_ads_by_word("NIKE")), 2)
        self.assertEqual(len(self.ad_index.fetch_ads_by_word("shoe")), 3)


class TestAdSelector(BaseTestCase):

    def test_select(self):
        ad_index = AdIndex()
        for ad in self.ads:
            ad_index.add_ad(ad)

        tokenized_words = ["nike", "basketball", "shoe"]
        relevant_ads = AdSelector.select(tokenized_words, ad_index)
        relevant_ads.sort(key=lambda relevant_ad: relevant_ad.ad.id)
        self.assertEqual(3, len(relevant_ads))
        self.assertEqual(1, relevant_ads[0].relevance_score)
        self.assertEqual(2/3.0, relevant_ads[1].relevance_score)
        self.assertEqual(1/3.0, relevant_ads[2].relevance_score)


class TestAdRanker(BaseTestCase):

    def test_fetch_top_2_relevant_ads(self):
        relevant_ad_list = []
        for ad in self.ads:
            relevant_ad_list.append(RelevantAd(ad, 1))

        top_2_queue = AdRanker.fetch_top_k_relevant_ads(relevant_ad_list, 2)
        self.assertEqual(2, top_2_queue.qsize())
        _, top1 = top_2_queue.get()
        _, top2 = top_2_queue.get()
        self.assertEqual(top1.ad.id, 1)
        self.assertEqual(top2.ad.id, 2)


class TestAdEngine(BaseTestCase):

    def test_fetch_ad(self):
        engine = AdEngine()
        relevant_ad = engine.fetch_ad("Nike basketball shoe")
        self.assertEqual(relevant_ad.ad.id, 1)
        self.assertEqual(relevant_ad.relevance_score, 1)