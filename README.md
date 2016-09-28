# Mini Ads Engine
This project is to build a mini ads engine.  The engine takes an user's query string, executes the following tasks and returns one relevant ad.

```
Parse Query

    |
    |
    
Select Ads  <------------------------- Ad Index
    
    |
    |
    
Filter Ads
    
    |
    |
    
Rank Ads
    
    |
    |
    
Select Top K Ads ----------------------> Pricing ---------------------> Return Ad
```

## Classes
**Ad:** An ad object with attributes: id, keywords, bid_price, click_probability and budget.

**RelevantAd:** An object wraps an ad and its relevance_score, quality_score and rank_score.  We use these scores to filter/rank ads.

**AdIndex:** An ad index supports fast ads lookup.  It has two components: a forward index and an inverted index.  The forward index is used to fast retrieve ad by id.  The inverted index is used to fast retrieve ad by keyword.

**QueryParser:** A parser used to clean and tokenize user's query string.

**AdSelector:** A selector used to fetch ads from AdIndex based on a set of tokenized keywords.  Each ad, once retrieved, is wrapped into an relevant ad object for filter/rank.

**AdFilter:** filters out the ads whose relevance score and click probability are below the bar.

**AdRanker:** uses a heap to fetch top k relevant ads by their rank scores.

**AdPricing:** calculates cost per click and charges the target ad.  The cost per click is usually different from/below the ad's bid price.  The formula is: cost_per_click = next ad rank score / target ad quality score + 0.01

## Usage
Modify the sample_data.py and execute the following code.
```
from ad_engine import AdEngine
engine = AdEngine()
relevant_ad = engine.fetch_ad(query_string)
```

## Future Improvements
- provide additional sample data.
- add more tests to tests.py. use python factory_boy library to generate test data.
- imporve query parser. stem and rewrite tokens when necessary.
- ad.click_probability should be user centric and calculated by some machine learning algorithms.
