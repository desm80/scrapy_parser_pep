import csv
import datetime as dt
from collections import Counter

from pep_parse.constants import BASE_DIR, DATETIME_FORMAT


class PepParsePipeline:
    """Дополнительная обработка статистической информации о статусах Pep и
    сохранение результата в csv файл."""
    def open_spider(self, spider):
        self.result = []
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        self.result.append(item['status'])
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = self.results_dir / file_name
        for_output = [('Статус', 'Количество')]
        for_output.extend(dict(Counter(self.result)).items())
        for_output.append(('Total', len(self.result)))

        with open(file_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(for_output)
