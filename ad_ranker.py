from queue import PriorityQueue


class AdRanker:
    """An ad ranker object."""

    @staticmethod
    def fetch_top_k_relevant_ads(relevant_ads, k):
        """Fetch top k relevant ads based on their rank score.

        Args:
            relevant_ads: a list of relevant ads.
            k: number of relevant ads to fetch.

        Returns:
            A priority queue containing the top k relevant ads.
        """
        top_k_queue = PriorityQueue()
        for relevant_ad in relevant_ads:
            rank_score = relevant_ad.rank_score
            if top_k_queue.qsize() < k:
                top_k_queue.put((-1 * rank_score, relevant_ad))
            else:
                negative_rank_score = top_k_queue.queue[0][0]
                if -1 * rank_score < negative_rank_score:
                    top_k_queue.get()
                    top_k_queue.put((-1 * rank_score, relevant_ad))
        return top_k_queue
