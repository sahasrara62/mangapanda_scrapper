# mangapanda_scrapper
download the entire manga series from mangapanda website, given need to provide the storing location and the manga URL like https://www.mangapanda.com/one-piece 

i hve used `xpath` for finding the data element and `requests` to  
communicate/crawl links. 


how to use:

1. install the requirements

     `python -m pip install -r requirements.txt`
     
2. assign storing location and manga url in the `main.py` (cli argument will be implemented, once i create a Object oriented Design)
   in `location` and `manga_url` 

3. run `main.py` by
     `python main.py`
     
   
