from constants import (
    MINIMUM_RELEVANCE_SCORE,
    MINIMUM_CLICK_PROBABILITY
)


class AdFilter:
    """An ad filter object."""

    @staticmethod
    def filter(relevant_ads):
        """Filter out ads whose relevant score and click probability are below
        the bar.

        Args:
            relevant_ads: A list of relevant ads.

        Returns:
            a list of relevant ads which filters out unqualified ones.
        """
        def meet_criteria(relevant_ad):
            """Check whether the relevant_ad is qualified.

            Args:
                relevant_ad: a relevant ad object.

            Returns:
                A boolean indicating whether the relevant ad is qualified.
            """
            return (relevant_ad.relevance_score >= MINIMUM_RELEVANCE_SCORE and
                    relevant_ad.ad.click_probability >= MINIMUM_CLICK_PROBABILITY)

        return list(filter(meet_criteria, relevant_ads))
