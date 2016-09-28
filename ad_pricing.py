class AdPricing:
    """An ad pricing object."""

    @staticmethod
    def charge_target_ad(top_k_relevant_ad_queue):
        """Calculate cost per click and charge the target ad.

        We don't charge the target ad by bid price when size of top_k_queue >= 2.
        Instead, we use the following formula to calculate cost per click.
        cost_per_click = next ad rank score / target ad quality score + 0.01

        If the target ad has no enough budget, we pick the next ad as the target ad.  If
        there is only one target ad left, we charge it by its bid price.

        Args:
            top_k_relevant_ad_queue: a priority queue containing top k ranked relevant ads.

        Returns:
            a target relevant ad.
        """
        if not top_k_relevant_ad_queue:
            return None

        _, target = top_k_relevant_ad_queue.get()
        while top_k_relevant_ad_queue.qsize() > 0:
            _, next_relevant_ad = top_k_relevant_ad_queue.get()
            next_rank_score = next_relevant_ad.rank_score
            cost_per_click = next_rank_score / float(target.quality_score) + 0.01
            if target.ad.charge(cost_per_click):
                return target
            target = next_relevant_ad

        cost_per_click = target.ad.bid_price
        if target.ad.charge(cost_per_click):
            return target
        return None
