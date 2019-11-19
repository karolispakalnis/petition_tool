import json
from datetime import datetime as dt
import matplotlib.pyplot as plt
import scrapy
import pandas as pd
from petitions.items import PetitionsItem

class RedditSpider(scrapy.Spider):
    name = 'petitions'

    def start_requests(self):
        yield scrapy.Request('https://petition.parliament.uk/petitions/266638')

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 15
    }

    def parse(self, response):
        item = PetitionsItem()
        item['petition_id'] = int(response.url.split("/")[-1])
        item['snapshot_url'] = response.request.url
        item['signature_count'] = int(response.css("span[class='count']::attr(data-count)").extract_first())
        item['timestamp'] = dt.fromtimestamp(response.meta['wayback_machine_time'].timestamp()).strftime('%d/%m/%Y , %H:%M:%S')
        final_json_url = f'{response.url}.json'

        yield item
        # yield scrapy.Request(url=final_json_url, callback=self.parse_json)

    @staticmethod
    def parse_json(self, response):

        null = None
        data = json.loads(response.text)
        data = data["data"]
        data = data["attributes"]
        data = data["signatures_by_constituency"]

        df = pd.DataFrame(data)
        x = df.filter(["name", "signature_count"])
        plt.rcParams["figure.figsize"] = (15, 200)
        ax = x.plot.barh(y='signature_count', x='name', rot=0)
        y = ax.get_figure()
        y.savefig("constituencies.png")

    def close(spider, reason):
        with open('a.json') as scraped_items:
            data = json.load(scraped_items)
            dataframe = pd.DataFrame.from_dict(data, orient='columns')
            dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])
            pd.to_datetime(dataframe['timestamp'])
            x = dataframe.filter(["signature_count", "timestamp"])
            plt.rcParams["figure.figsize"] = (20, 10)
            ax = x.plot(y='signature_count', x='timestamp', rot=35)
            y = ax.get_figure()
            y.savefig("total_signatures.png")





