import pandas as pd
import datetime
from dateutil.parser import parse

def fetchTimeSeries(tweets, propName):
    df = pd.DataFrame(tweets)
    df['created_at'] = [unixTimeSeconds(parse(created_at).date()) for created_at in df['created_at'].tolist()]
    df = df.groupby(['created_at']).sum()
    return df.to_dict()

def unixTimeSeconds(date_time, includeTime=False):
    epoch = datetime.datetime.utcfromtimestamp(0)
    if includeTime is False:
        date_time = datetime.datetime.combine(date_time, datetime.time())
    return int((date_time - epoch).total_seconds())