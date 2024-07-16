# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import re


class BookscraperPipeline:
    def process_item(self, item, spider):
        output_dir = 'output'
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = os.path.join(output_dir, self.clean_bookname(item['title']) + '.txt')

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(item.get('full_text',''))

        return item
    
    def clean_bookname(self, title):
        pattern_alphanum = r'[\W]'
        clean_title = re.sub(pattern_alphanum,'',title)
        return clean_title


