
# PTT Author Crawler
![PTT Author Crawler.jpg](images%2FPTT%20Author%20Crawler.jpg)
PTT Author Crawler is a Python-based tool for scraping articles from the Taiwanese forum PTT (批踢踢) based on a specific author's ID. This tool extracts details such as the article's title, author, date, content, upvote and downvote counts, and saves the results in a structured JSON format. It provides real-time progress updates using `tqdm` for better user experience.

PTT Author Crawler 是一個基於 Python 的工具，用於從台灣的論壇 PTT（批踢踢）中，根據特定作者的 ID 來爬取文章。這個工具會提取文章的詳細資訊，例如文章標題、作者、發文日期、內容、推文和噓文數量，並將結果儲存為結構化的 JSON 格式。它還使用 `tqdm` 提供即時的進度更新，以提升使用者體驗。

## Features
- Extracts article information including title, author, date, and detailed content.
- Counts and records upvotes and downvotes for each article.
- Saves the scraped data in JSON format for easy storage and analysis.
- Displays progress using a terminal-based progress bar (tqdm).

## Prerequisites
- Python 3.x
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `tqdm`

You can install the required libraries using:
```
pip install requests beautifulsoup4 tqdm
```

## How to Use
1. Clone or download this repository to your local machine.
2. Ensure you have Python 3 installed along with the required libraries (`requests`, `beautifulsoup4`, and `tqdm`).
3. Update the `author_id` variable in the script to the PTT ID of the author whose articles you want to scrape.
4. Run the script:
```
python ptt_author_crawler.py
```

The script will crawl all articles by the specified author and save the results to a file named `ptt_articles.json`.

## Example Output
```
Data saved to ptt_articles.json
```

This file will contain a JSON array of articles with detailed information such as:
```json
[
    {
        "title": "Re: [請益] 男生大約薪水多少or多少財富再交女友較好",
        "author": "a0000000000v",
        "date": "Wed Nov 29 11:49:36 2023",
        "content": "假設A男 年收1100萬 ...",
        "upvotes": 10,
        "downvotes": 2
    },
    ...
]
```

## Code Overview
- **`get_article_details`**: Fetches and parses the details of a single article, including its title, author, date, content, and interactions.
- **`crawl_ptt_author`**: Crawls the list of articles based on a given author ID and collects detailed information for each article.
- **`save_to_json`**: Saves the collected articles into a JSON file for further analysis.

## Notes
- The tool bypasses the "over 18" confirmation page by setting a cookie. This might need updating if PTT changes its anti-crawling measures.
- Ensure that you follow PTT's rules and guidelines when scraping data to avoid being banned.

## Future Improvements
- Support for multi-threaded scraping to enhance speed.
- Options to filter articles by date or keyword.
- Integration with databases for more efficient data storage and querying.

## License
This project is open-source and available under the MIT License.
```
