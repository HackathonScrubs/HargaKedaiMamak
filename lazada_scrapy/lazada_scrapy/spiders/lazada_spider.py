import scrapy
import re
import os
import json
import csv

class LazadaSpider(scrapy.Spider):
    name = "lazada"

    def start_requests(self):
        #lazada_urls = [
        ##   'https://www.lazada.com.my/products/redmi-note-11-11s10s6gb8gb128gboriginal-xiaomi-malaysia-ready-stock-i2804862797-s13429928234.html',
        ##   'https://www.lazada.com.my/products/samsung-galaxy-a23-lte-6gb128gbnew-model-original-samsung-malaysia-i2885763883-s13949701011.html',
        ##   'https://www.lazada.com.my/products/huawei-matepad-t10s-23gb3264gb-original-huawei-malaysai-ready-stock-i2019269555-s8017813986.html',
        ##   'https://www.lazada.com.my/products/apple-ipad-mini-6th-gen-wi-fi-i2481158753-s10856138295.html',
        ##   'https://www.lazada.com.my/products/apple-129-inch-ipad-pro-5th-gen-wi-fi-cellular-i2116141204-s8577165743.html',
        ##   'https://www.lazada.com.my/products/xiaomi-mi-11-lite-5g-ne8gb128256gb-original-xiaomi-malaysia-i2063198705-s8230256789.html',
        ##   'https://www.lazada.com.my/products/redmi-note-11-11s10s6gb8gb128gboriginal-xiaomi-malaysia-ready-stock-i2804862797-s13429928238.html'
        ##   'https://www.lazada.com.my/products/oppo-a54-4gb64128gb-original-oppo-malaysia-ready-stock-i2063114741.html',
        ##   'https://www.lazada.com.my/products/redmi-10c4gb64128gb-original-xiaomi-malaysia-10c-ready-stock-i2888409397-s13965567738.html?'
        ##   'https://www.lazada.com.my/products/oppo-reno-66-pro6z5f5-5-pro-5g-8gb12gb-128gb256gb-original-oppo-malaysiaready-stock-i1937644220.html',
        #    'https://www.lazada.com.my/products/redmi-9a-2gb32gb-original-xiaomi-malaysia-i1732434547.html'
        #]
        lazada_urls = []
        with open("../../../input_files/lazada_links.csv") as links_csv:
            csv_reader = csv.reader(links_csv)
            for row in csv_reader:
                lazada_urls.append(row[0])

        for url in lazada_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'url':url})
            #yield scrapy.Request(url=url, callback=self.get_html)
    
    def parse(self, response):
        pattern = re.compile(r"var __moduleData__ = ({.*?});", re.MULTILINE | re.DOTALL)
        locations = response.xpath('//script[contains(., "var __moduleData__")]/text()').re(pattern)[0]
        locations = json.loads(locations)

        prices = locations["data"]["root"]["fields"]["skuInfos"]
        properties = locations["data"]["root"]["fields"]["productOption"]["skuBase"]["properties"]
        sku_match = locations["data"]["root"]["fields"]["productOption"]["skuBase"]["skus"]
        title = locations["data"]["root"]["fields"]["product"]["title"]
        
        #print(response.meta['url'])
        
        match_back = {}
        for p in sku_match:
            #match_back.[{"skuId" : p["skuId"], "propPath": 
            prop = p["propPath"]
            match_back[p["skuId"]] = prop[prop.rfind(":") + 1:]

        match_front = {}
        for p in sku_match:
            prop = p["propPath"]
            match_front[p["skuId"]] = prop[prop.find(":") + 1 : 
                    prop.find(";")
                    if prop.find(";") >= 1
                    else len(prop)]

        storage = {}
        for p in properties:
            for v in p["values"]:
                if (p["name"] == "Storage Capacity"):
                    storage[v["vid"]] = v["name"]

        colour = {}
        for p in properties:
            for v in p["values"]:
                if (p["name"] == "Color Family"):
                    colour[v["vid"]] = v["name"]

        model = {}
        for p in properties:
            for v in p["values"]:
                if (p["name"] == "MODEL"):
                    model[v["vid"]] = v["name"]

        variation = {}
        for p in properties:
            for v in p["values"]:
                if (p["name"] == "Variation"):
                    variation[v["vid"]] = v["name"]

        spec = {}
        for p in properties:
            for v in p["values"]:
                if (p["name"] == "SPEC"):
                    spec[v["vid"]] = v["name"]

        res = []
        #print("match_back", match_back, "\n")
        #print("match_front", match_front, "\n")
        #print("storage", storage, "\n")
        #print("colour",colour, "\n")
        #print("model",model, "\n")
        #print("variation", variation, "\n")

        for sku in prices:
            if (sku != "0"):
                #print(match_back[sku])
                #print("sku:", sku)
                #print("match_front[sku]:", match_front[sku])
                #if match_front[sku] in colour:
                #    print("in:", colour[match_front[sku]])
                final = (storage[match_back[sku]] + " "
                        if match_back[sku] in storage else storage[match_front[sku]] + " "
                        if match_front[sku] in storage else "") + (colour[match_front[sku]] + " "
                        if match_front[sku] in colour else colour[match_back[sku]] + " "
                        if match_back[sku] in colour else "") + (model[match_back[sku]] + " "
                        if match_back[sku] in model else model[match_front[sku]] + " "
                        if match_front[sku] in model else "") + (variation[match_back[sku]] + " "
                        if match_back[sku] in variation else variation[match_front[sku]] + " "
                        if match_front[sku] in variation else "") + (spec[match_back[sku]] + " "
                        if match_back[sku] in spec else spec[match_front[sku]] + " "
                        if match_front[sku] in spec else "")
                #print("final", final)
                res.append({
                    "productURL" : response.meta['url'],
                    "productName from URL" : title,
                    #"sku": sku, 
                    "productVariant from URL" :  final,
                    #"productStorage" : 
                    #    storage[match_back[sku]]
                    #    if match_back[sku] in storage else storage[match_front[sku]]
                    #    if match_front[sku] in storage else None,
                    #"productColour" : 
                    #    colour[match_front[sku]]
                    #    if match_front[sku] in colour else colour[match_back[sku]]
                    #    if match_back[sku] in colour else None,
                    #"productModel" :
                    #    model[match_back[sku]]
                    #    if match_back[sku] in model else model[match_front[sku]]
                    #    if match_front[sku] in model else None,
                    #"productVariation" :
                    #    variation[match_back[sku]]
                    #    if match_back[sku] in variation else variation[match_front[sku]]
                    #    if match_front[sku] in variation else None,
                    #"productSpec" :
                    #    spec[match_back[sku]]
                    #    if match_back[sku] in spec else spec[match_front[sku]]
                    #    if match_front[sku] in spec else None,
                    "Stock Status from URL" : 
                        prices[sku]["quantity"]["text"] 
                        if prices[sku]["quantity"]["text"] != ""
                        else "Only " + str(prices[sku]["quantity"]["limit"]["max"]) + " items left",
                    "price" : prices[sku]["price"]["salePrice"]["text"],
                })

        #for r in res:
        #    print(r)
        #print("\n\n")
        return (res)

    def get_html(self,response):
        page = response.url.split("/")[2]
        name = response.url.split("/")[-1]
        filename = f'{page}-{name}'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
