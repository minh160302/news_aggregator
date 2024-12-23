# import asyncio
import gdelt
import trends
import LLM
from redis_client import redis_client

from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.parse import unquote
from mangum import Mangum
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


"""
Saved in cache, or in-mem database
Index keywords
Scrawl Google trending to pre-fetch some keywords
"""


# * Search articles from trusted source by keywords
@app.post("/search/{keyword}")
def search_articles_by_keyword(keyword: str):
    keyword = unquote(keyword)
    # Trusted news sources
    sources = [
        "bbc.com",
        "cnn.com",
        "reuters.com",
        "nytimes.com",
        "theguardian.com",
        "washingtonpost.com",
        "nbcnews.com",
        "abcnews.go.com",
        "bloomberg.com",
        "techcrunch.com",
        "wsj.com",
        "aljazeera.com",
        "foxnews.com",
        "fox4news.com",
        "huffpost.com",
        "apnews.com",
        "investopedia.com"
    ]
    articles = gdelt.search_gdelt_by_keyword(keyword)
    trusted = gdelt.filter_by_trusted_sources(articles, sources)
    trusted.drop_duplicates(subset=['title'], keep="first", inplace=True)
    response = {s: [] for s in sources}
    for row in trusted.itertuples():
        response[row.domain].append({
            'title': row.title,
            'url': row.url,
        })
    return response


class ArticleUrlBody(BaseModel):
    url: str


@app.post("/summarize")
async def summarize_article_url(body: ArticleUrlBody):
    """
    Summarize an article with Llama
    """
    url = body.url
    try:
        value = await redis_client.get(url)
        if value is None:
            value = await LLM.send_article_then_summarize(body.url)
            await redis_client.set(url, value, ex=3600)
        else:
            value = value.decode("utf-8")
        return {'summary': value}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Redis read error: {str(e)}")


@app.get("/trends")
async def get_trending_keywords():
    """
    Get trending keywords
    """
    trends_df = trends.get_trending_keywords()
    data = []
    for row in trends_df.itertuples():
        data.append({
            'keyword': row.title,
            'geolocation': row.geolocation
        })
    return {'data': data}


lambda_handler = Mangum(app)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8080)
