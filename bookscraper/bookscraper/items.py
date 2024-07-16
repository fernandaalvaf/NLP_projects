from scrapy.item import Item, Field

class BookItem(Item):
    title = Field()
    url = Field()
    language = Field()
    full_text = Field()
