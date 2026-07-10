# 일별 블로그 클리핑

인벤티지랩·알테오젠 등 관심 기업과 반도체·바이오·부동산·주식·선물 같은 관심 주제를
네이버 블로그 검색에서 매일 자동으로 모아서 탭별로 보여주는 사이트입니다.

카카오봇/메모리 대시보드와 같은 원리예요: GitHub Actions가 매일 스크립트를 돌려서
`index.html`을 새로 만들고, GitHub Pages가 그걸 자동으로 발행합니다.

---

## 1단계. 새 저장소 만들기

1. https://github.com/new
2. Repository name: `blog-tracker` (원하는 이름으로)
3. **Public** 선택
4. Create repository

## 2단계. 파일 업로드

- `template.html`, `generate_blogs.py`, `README.md` 는 [Add file → Upload files]로 업로드
- `.github/workflows/daily-blog.yml` 은 [Add file → Create new file] → 파일명에
  `.github/workflows/daily-blog.yml` 그대로 입력 → 내용 붙여넣기 → Commit

## 3단계. Secret 등록

Settings → Secrets and variables → Actions → New repository secret

| Name | Value |
|---|---|
| `NAVER_CLIENT_ID` | 네이버 개발자센터 Client ID (부동산 봇에 쓰던 것 재사용 가능) |
| `NAVER_CLIENT_SECRET` | 네이버 개발자센터 Client Secret (재사용 가능) |

## 4단계. GitHub Pages 켜기

Settings → Pages → Source: "Deploy from a branch" → Branch: main, 폴더: / (root) → Save

## 5단계. 첫 실행

Actions 탭 → "Daily Blog Clipping" → Run workflow → 완료되면 Pages 주소로 접속해서 확인

---

## 탭 구성 / 검색어 수정하기

`generate_blogs.py` 안의 `TABS` 리스트에서 탭을 추가/삭제/수정할 수 있어요:

```python
TABS = [
    {"id": "inventage", "label": "인벤티지랩", "group": "company", "query": "인벤티지랩"},
    {"id": "alteogen", "label": "알테오젠", "group": "company", "query": "알테오젠"},
    {"id": "semicon", "label": "반도체", "group": "topic", "query": "반도체"},
    {"id": "bio", "label": "바이오", "group": "topic", "query": "바이오"},
    {"id": "realestate", "label": "부동산", "group": "topic", "query": "부동산"},
    {"id": "stock", "label": "주식", "group": "topic", "query": "주식"},
    {"id": "futures", "label": "선물", "group": "topic", "query": "주식 선물"},
]
```

- `group`은 `"company"` 또는 `"topic"` 두 가지만 가능 (탭이 이 두 그룹으로 나뉘어 표시돼요)
- `query`는 실제 네이버 블로그 검색에 쓰이는 검색어예요. 새 기업/주제를 추가하고 싶으면
  이 리스트에 항목을 하나 더 추가하면 됩니다.
- 탭당 게시글 수는 상단의 `POSTS_PER_TAB = 12` 값을 바꾸면 돼요.

## 참고 / 한계

- 표시되는 건 제목·블로거 이름·작성일·링크뿐이에요. 본문 내용은 저작권 때문에 가져오지 않고,
  링크를 눌러 원문에서 확인하는 방식입니다.
- "선물"은 검색어를 "주식 선물"로 넣어서 일반적인 "선물(gift)" 글이 덜 섞이게 했어요.
  그래도 완벽히 걸러지지는 않을 수 있어요.
- 발행 시간을 바꾸고 싶으면 `.github/workflows/daily-blog.yml`의 `cron` 값을 수정하세요.
