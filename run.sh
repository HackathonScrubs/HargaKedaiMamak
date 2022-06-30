if [[ $1 == "scrape" ]]
then
	echo "Scraping from Lazada..."
	source priceshop_env/bin/activate
	cd lazada_scrapy/lazada_scrapy/spiders/
	scrapy crawl lazada -O ../../../input_files/lazada.json
elif [[ $1 == "match" ]]
then
	echo "Matching..."
	source priceshop_env/bin/activate
	python3 get_patterns.py
	python3 get_matches.py
else
	echo "Setting up..."
	pip3 install virtualenv
	source priceshop_env/bin/activate
fi