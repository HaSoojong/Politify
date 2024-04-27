# trend_fetcher.py
from pytrends.request import TrendReq
from models import Trend
import pandas as pd

def fetch_google_trends(keyword):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword], geo ='US')
    df = pytrend.interest_by_region(resolution='STATE', inc_low_vol=True, inc_geo_code=False)
    return df

def store_in_database(keyword, df, db):
    sorted_df = df.sort_values(by=keyword, ascending=False).head(5)
    top_regions = {state: {state: int(value)} for state, value in sorted_df.iterrows()}

    trend_entry = Trend(
        keyword=keyword,
        top1={sorted_df.index[0]: int(sorted_df.iloc[0][keyword])},
        top2={sorted_df.index[1]: int(sorted_df.iloc[1][keyword])},
        top3={sorted_df.index[2]: int(sorted_df.iloc[2][keyword])},
        top4={sorted_df.index[3]: int(sorted_df.iloc[3][keyword])},
        top5={sorted_df.index[4]: int(sorted_df.iloc[4][keyword])}
    )
    
    db.add(trend_entry)
    db.commit()