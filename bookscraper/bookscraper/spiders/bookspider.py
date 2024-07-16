import scrapy
from bookscraper.items import BookItem
import re

# create the bookspider spider class
class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    # define name of allowed domains so that it does not crawl outside of scope
    allowed_domains = ["www.gutenberg.org"]
    # starting url = Jane Austen
    start_urls = ["https://www.gutenberg.org/ebooks/author/68"]

    def parse(self, response):
         # get the list of books
         books = response.css('li.booklink')
         
         i = 0
         # extract the url of the books and directs to it for further extraction
         for book in books:
            book_item = BookItem()

            relative_url = book.css('a.link ::attr(href)').get()
            book_url = "https://www.gutenberg.org" + relative_url

            book_item['url'] = book_url
            book_item['title'] = book.css('span.title ::text').get()   
            filename = re.sub(r'[\W]','',book_item['title'])
            book_item['file_name'] = f"{filename}{i}.txt"

            request = response.follow(book_url, callback=self.parse_book_page)
            request.meta['book_item'] = book_item

            i += 1
            yield request

         # extract the link of the next page url - not very clean in the code of project gutenberg
         next_page = response.xpath('//a[@accesskey="+"]')

         if next_page:
            next_page_url = "https://www.gutenberg.org" + next_page[0].attrib['href']
            # follow the next_page_url and start over the function parse with the new page until there is no new page
            yield response.follow(next_page_url, callback=self.parse)

         

    def parse_book_page(self, response):
        book_item = response.meta['book_item']
        table_rows = response.css('table.bibrec tr')

        language = table_rows.xpath('//tr[@property="dcterms:language"]').css('td ::text').get()
        book_item['language'] = language

        url_txt = response.xpath('//a[@type="text/plain; charset=us-ascii"]')
        
        if len(url_txt) > 0:
            txt_page = "https://www.gutenberg.org" + url_txt.attrib['href']
            request = response.follow(txt_page, callback=self.parse_book_text)
            request.meta['book_item'] = book_item
            yield request
        else:
            book_item["full_text"] = ""
            yield book_item
            
    def parse_book_text(self, response):
        book_item = response.meta['book_item']

        full_text = response.css('body ::text').get()
        book_item['full_text'] = full_text
        yield book_item
        

        
