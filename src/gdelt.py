from pandas import DataFrame
from gdeltdoc import GdeltDoc, Filters
from typing import List


def search_gdelt_by_keyword(keyword: str) -> DataFrame:
    timespan = '1d'
    country = 'US'

    f = Filters(
        keyword=keyword,
        # start_date = "2020-05-10",
        # end_date = "2020-05-11",
        country=country,
        timespan=timespan,
    )

    gd = GdeltDoc()

    # Search for articles matching the filters
    articles = gd.article_search(f)

    # Get a timeline of the number of articles matching the filters
    # timeline = gd.timeline_search("timelinevol", f)
    return articles


def filter_by_trusted_sources(articles: DataFrame, sources: List[int]) -> DataFrame:
    trusted_sources = set(sources)
    trusted = DataFrame() if articles.empty else articles[articles['domain'].isin(trusted_sources)]
    return trusted
