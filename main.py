import requests
from lxml import html
import json
from tqdm import tqdm


def get_article_details(article_url):
    response = requests.get(article_url, cookies={'over18': '1'})
    tree = html.fromstring(response.content)

    # 找到 main-content 區塊
    main_content = tree.xpath('//*[@id="main-content"]')[0]

    # 提取推/噓數
    pushes = tree.xpath('//div[@class="push"]')

    upvotes = sum(1 for push in pushes if '推' in push.xpath('.//span/text()')[0])
    downvotes = sum(1 for push in pushes if '噓' in push.xpath('.//span/text()')[0])

    total_votes = upvotes + downvotes

    # 初始化變量
    title = 'N/A'
    author = 'N/A'
    date = 'N/A'

    # 遍歷 main-content 中的子元素
    for i in range(1, len(main_content.xpath('./div')) + 1):
        meta_tag = main_content.xpath(f'./div[{i}]/span[1]/text()')
        meta_value = main_content.xpath(f'./div[{i}]/span[2]/text()')
        if not meta_tag or not meta_value:
            continue

        # 如果標籤是 "作者"
        if meta_tag[0] == "作者":
            author = meta_value[0]

        # 如果標籤是 "標題"
        elif meta_tag[0] == "標題":
            title = meta_value[0]

        # 如果標籤是 "時間"
        elif meta_tag[0] == "時間":
            date = meta_value[0]

    # 提取文章內容
    content_main = ''.join(main_content.xpath('.//text()'))

    # 移除標題和 meta 數據
    for meta in main_content.xpath('./div | ./div[@class="article-metaline-right"]'):
        main_content.remove(meta)
    for push in main_content.xpath('.//div[@class="push"]'):
        main_content.remove(push)
    content_meta = ''.join(main_content.xpath('.//text()')).strip()



    content = ''.join((content_main + content_meta).split('標題')[1:]).split('※ 發信站')[0]
    content = ''.join(content.split('\n')[1:])
    return {
        'title': title,
        'author': author,
        'date': date,
        'url': article_url,  # 加入文章的原始 URL
        'content': content,
        'upvotes': upvotes,
        'downvotes': downvotes,
        'total_votes': total_votes
    }


def crawl_ptt_author(author_id, max_pages='1'):
    base_url = f'https://www.ptt.cc/bbs/CATCH/search?page='
    page = 1
    all_articles = []

    print(f"Starting to crawl articles for author: {author_id}")
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(base_url + str(page) + f'&q=author%3A{author_id}', cookies={'over18': '1'})
        tree = html.fromstring(response.content)

        articles = tree.xpath('//div[@class="title"]/a')
        if not articles:  # 如果沒有文章則跳出循環
            print("No more articles found. Stopping.")
            break

        for article in tqdm(articles, desc=f"Processing articles on page {page}", unit="article"):
            article_title = article.text_content()
            article_link = 'https://www.ptt.cc' + article.get('href')
            print(f"Fetching article: {article_title}")
            article_details = get_article_details(article_link)
            all_articles.append(article_details)

        page += 1  # 進入下一頁

        # 判斷是否達到最大頁數
        if max_pages != 'all' and page > int(max_pages):
            print(f"Reached the maximum number of pages: {max_pages}. Stopping.")
            break

    print(f"Finished crawling. Total articles collected: {len(all_articles)}")
    return all_articles


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")


# 使用範例
author_id = 'a0000000000v'
max_pages = 'all'  # 預設為1頁 ('all' 表示所有頁面, 也可以設置為 1 或 2 等數字)

articles = crawl_ptt_author(author_id, max_pages)
save_to_json(articles, 'ptt_articles.json')
