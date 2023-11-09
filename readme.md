# CS3103 Web Crawler

## Install Dependencies
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Running the Crawler
```
python src/main.py
```
Response times to the servers, IP addresses and geolocation of the servers will be written to `data/results.json`, along with all URLs found within the webpage.