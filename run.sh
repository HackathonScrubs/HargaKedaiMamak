if [[ $1 == "scrape" ]]
then
	echo "Scraping from Lazada..."
	source priceshop_env/bin/activate
	cd lazada_scrapy/lazada_scrapy/spiders/
	scrapy crawl lazada -O ../../../input_files/lazada.json
	cd ../../..
	deactivate
elif [[ $1 == "match" ]]
then
	echo "Matching..."
	source priceshop_env/bin/activate
	python3 source_files/get_patterns.py
	python3 source_files/get_matches.py
	deactivate
else
	echo "Setting up..."
	pip3 install virtualenv
	python3 -m venv priceshop_env
	source priceshop_env/bin/activate
	pip3 install Scrapy
	pip3 install spacy
	pip3 install pandas
	pip3 install rapidfuzz
	deactivate
fi
