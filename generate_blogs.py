"""
기업/주제별 네이버 블로그를 매일 수집해서 index.html을 새로 생성하는 스크립트.
디자인은 template.html에 고정, 이 스크립트는 "내용(JSON)"만 매일 새로 만들어서 끼워넣음.
GitHub Actions에서 매일 자동 실행됩니다. (직접 실행할 필요 없음)

필요한 환경변수 (GitHub Secrets로 등록):
  NAVER_CLIENT_ID      네이버 개발자센터 애플리케이션 Client ID
  NAVER_CLIENT_SECRET  네이버 개발자센터 애플리케이션 Client Secret
"""

import os
import re
import json
from datetime import datetime, timezone, timedelta
import requests

KST = timezone(timedelta(hours=9))
NAVER_CLIENT_ID = os.environ["NAVER_CLIENT_ID"]
NAVER_CLIENT_SECRET = os.environ["NAVER_CLIENT_SECRET"]

POSTS_PER_TAB = 12

# id: 내부 식별자, label: 탭에 보이는 이름, group: company | topic, query: 네이버 검색어
TABS = [
    {"id": "inventage", "label": "인벤티지랩", "group": "company", "query": "인벤티지랩"},
    {"id": "alteogen", "label": "알테오젠", "group": "company", "query": "알테오젠"},
    {"id": "semicon", "label": "반도체", "group": "topic", "query": "반도체"},
    {"id": "bio", "label": "바이오", "group": "topic", "query": "바이오"},
    {"id": "realestate", "label": "부동산", "group": "topic", "query": "부동산"},
    {"id": "stock", "label": "주식", "group": "topic", "query": "주식"},
    {"id": "futures", "label": "선물", "group": "topic", "query": "주식 선물"},
]

TAG_RE = re.compile(r"<.*?>")


def clean(text: str) -> str:
    text = TAG_RE.sub("", text or "")
    return (
        text.replace("&quot;", '"')
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .strip()
    )


def fetch_blog_posts(query: str, count: int):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    res = requests.get(
        "https://openapi.naver.com/v1/search/blog.json",
        headers=headers,
        params={"query": query, "display": count, "sort": "date"},
        timeout=15,
    )
    res.raise_for_status()
    items = []
    for item in res.json().get("items", []):
        postdate = item.get("postdate", "")
        date_fmt = f"{postdate[:4]}.{postdate[4:6]}.{postdate[6:8]}" if len(postdate) == 8 else ""
        items.append(
            {
                "title": clean(item.get("title", "")),
                "link": item.get("link", ""),
                "blogger": clean(item.get("bloggername", "")),
                "date": date_fmt,
            }
        )
    return items


def build_data() -> dict:
    tabs_out = []
    for tab in TABS:
        try:
            posts = fetch_blog_posts(tab["query"], POSTS_PER_TAB)
        except Exception as e:
            print(f"[{tab['label']}] 블로그 수집 실패:", e)
            posts = []
        tabs_out.append(
            {
                "id": tab["id"],
                "label": tab["label"],
                "group": tab["group"],
                "posts": posts,
            }
        )
    return {
        "updated": datetime.now(KST).strftime("%Y-%m-%d %H:%M"),
        "tabs": tabs_out,
    }


def build_html(data: dict) -> str:
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()
    json_str = json.dumps(data, ensure_ascii=False)
    json_str = json_str.replace("</", "<\\/")  # </script> 파싱 깨짐 방지
    return template.replace("__BLOG_DATA__", json_str)


def main():
    data = build_data()
    html = build_html(data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    total = sum(len(t["posts"]) for t in data["tabs"])
    print(f"생성 완료! 총 {total}개 게시글, {len(html)}자")


if __name__ == "__main__":
    main()
