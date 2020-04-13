# mangapanda_scrapper
download the entire manga series from [mangapanda](http://www.mangapanda.com] and [mangareader](http://www.mangareader.net) website, given need to provide the storing location and the manga URL like https://www.mangapanda.com/one-piece 

 

how to use:

1. install the requirements

     `python -m pip install -r requirements.txt`
     
2. assign storing location and manga url in the `main.py` (cli argument will be implemented, once i create a Object oriented Design)
   in `location` and `manga_url` 

3. command line argument is using 
    parameters are
    
       -u  (url) : url of the manga eg https://www.mangapanda.com/naruto
       -c (chapter): use to download a single chapter eg https://www.mangapanda.com/naruto/1
       -l (location) : speicify where the project need to be save, default it take the executable file addess 
                      (tested for linux : /home/user/manga ) use absolute address
       -s (start) : used when one want to download chapter in a range between (22-34)
       -e (end) : end of the chapter range where want to specify chapter
        
4. Download the manga by running the command

     a. `python main.py -u <manga url>`
     
     this will download all the entire manga at the script location, if use `-l` will download the manga
     at the desired location
     
     b. 
      `python main.py -u <manga url> -c <chapter_url>` 
      
      eg   `python main.py -u https://www.mangapanda.com/one-piece -c https://www.mangapanda.com/one-piece/1 `
      this will download that chaper only
     
     c. `python main.py -u <manga url> -s <starting chater>` 
      
      this will download chapter form  the starting chapter till the end chapter in mangaurl
     
     eg  `python main.py -u https://www.mangapanda.com/one-piece -s 11`
     
     d. 
     
     `python main.py -u <manga url> -e <end chater>`
      
     this will download chapter form  the starting chapter in manga url (ie 1) to  till the end soecified chapter in mangaurl
     
     eg `python main.py -u https://www.mangapanda.com/one-piece -e 11 `
     
     e.
     `python main.py -u <manga url> -s <starting chater> -e <end chapter>`  
     
     this will download chapter form  the specfoed  starting chapter till the end chapter in mangaurl
     
     eg `python main.py -u https://www.mangareader.net/one-piece -s 1 -e 10 `
     
Note:
     
   1. use `-l` to define the saving location path
   2. use of `-u` is necessary
   3. if chapter and range don't run together, if chapter is specified then only 
      that chapeter will be downloaded not the start or end chapter if mentioned
      
ToDo in future:

1. keep the history of downloaded data in the apllication so if the application is stopped in beetween , user able to start download from that point not for the begining.
2. Desktop application (electron js or qt )
