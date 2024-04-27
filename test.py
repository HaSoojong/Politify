from pytrends.request import TrendReq
pytrend = TrendReq()
#It is the term that you want to search
pytrend.build_payload(kw_list=["Drake"], geo='US')
# Find which region has searched the term
df = pytrend.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)

print(df)
