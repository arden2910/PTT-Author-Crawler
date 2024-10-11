import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm


def get_article_details(article_url):
    response = requests.get(article_url, cookies={'over18': '1'})
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取標題
    title = soup.select_one('div.article-metaline span.article-meta-value').text if soup.select_one(
        'div.article-metaline span.article-meta-value') else 'N/A'

    # 提取作者
    author = soup.select_one('div.article-metaline:nth-of-type(1) span.article-meta-value').text if soup.select_one(
        'div.article-metaline:nth-of-type(1) span.article-meta-value') else 'N/A'

    # 提取時間
    date = soup.select_one('div.article-metaline:nth-of-type(3) span.article-meta-value').text if soup.select_one(
        'div.article-metaline:nth-of-type(3) span.article-meta-value') else 'N/A'

    # 提取文章內容
    main_content = soup.select_one('#main-content').text if soup.select_one('#main-content') else ''
    for meta in soup.select('.article-metaline, .article-metaline-right'):
        meta.extract()
    for push in soup.select('.push'):
        push.extract()
    content = soup.select_one('#main-content').text.strip() if soup.select_one('#main-content') else ''

    # 提取推/噓數
    pushes = soup.select('.push')
    upvotes = sum(1 for push in pushes if '推' in push.text)
    downvotes = sum(1 for push in pushes if '噓' in push.text)

    return {
        'title': title,
        'author': author,
        'date': date,
        'content': content,
        'upvotes': upvotes,
        'downvotes': downvotes
    }


def crawl_ptt_author(author_id):
    base_url = f'https://www.ptt.cc/bbs/CATCH/search?page='
    page = 1
    all_articles = []

    print(f"Starting to crawl articles for author: {author_id}")
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(base_url + str(page) + f'&q=author%3A{author_id}', cookies={'over18': '1'})
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.select('div.title a')
        if not articles:  # 如果沒有文章則跳出循環
            print("No more articles found. Stopping.")
            break

        for article in tqdm(articles, desc=f"Processing articles on page {page}", unit="article"):
            article_title = article.text
            article_link = 'https://www.ptt.cc' + article['href']
            print(f"Fetching article: {article_title}")
            article_details = get_article_details(article_link)
            all_articles.append(article_details)

        page += 1  # 進入下一頁

    print(f"Finished crawling. Total articles collected: {len(all_articles)}")
    return all_articles


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")


author_id = 'a0000000000v'
articles = crawl_ptt_author(author_id)
save_to_json(articles, 'ptt_articles.json')
