from pytrends.request import TrendReq

def get_trends(hl, tz, pn):
    pytrends = TrendReq(hl=hl, tz=tz)
    trends_df = pytrends.trending_searches(pn=pn)
    return trends_df[0].to_list()