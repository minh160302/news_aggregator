import httpx
import json
import pandas as pd
from datetime import datetime


def get_trending_keywords() -> pd.DataFrame:
    """
    Get trending keywords in the past few days in a specific geolocation
    """
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime('%Y%m%d')
    result = []
    geo_location = "US"
    days = 2

    # Decrement the date parameter to get trends data of previous days
    for day in range(int(formatted_date), int(formatted_date) - days, -1):

        url = f"https://trends.google.com/trends/api/dailytrends?hl=en-{geo_location}&tz=-180&ed={day}&geo=US&hl=en-US&ns=15"

        response = httpx.get(url=url)
        data = json.loads(response.text.replace(")]}',", ""))

        # Extract the formatted date from the JSON data
        date = data["default"]["trendingSearchesDays"][0]["formattedDate"]

        for trend in data["default"]["trendingSearchesDays"][0]["trendingSearches"]:
            trend_object = {
                "title": trend["title"]["query"],
                "traffic_volume": trend["formattedTraffic"],
                "link": "https://trends.google.com/" + trend["title"]["exploreLink"],
                "type": "Trend_topic",
                "date": date,
                "geolocation": geo_location
            }
            result.append(trend_object)
    df = pd.DataFrame(result)

    # Sort by traffic volume
    for index, row in df.iterrows():
        s = str(row["traffic_volume"])[:-1]
        row["traffic_volume"] = int(
            s[:-1]) * (10**3 if s[-1] == 'K' else 10**6)

    df.sort_values(by='traffic_volume', inplace=True, ascending=False)
    return df
