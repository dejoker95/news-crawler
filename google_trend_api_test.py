from pytrends.request import TrendReq
pytrends = TrendReq(hl='ko', tz=540)
df = pytrends.trending_searches(pn='south_korea')


print(list(df.columns))

print(df[0].tolist())
