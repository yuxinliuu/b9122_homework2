from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request



seed_url = "https://www.sec.gov/news/pressreleases/" #the website we're starting with
root_url = "https://www.sec.gov/news/press-release/" # all childurls should contain the root

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen and checked so far
opened = []          #we keep track of seen urls so that we don't revisit them
chosen = []          #we choose the url if its main paragraph contains the searched word 
searched_word = 'charges'
num_found = 0        #number of urls containing the searched word we have found
max_found = 20       #we only want the first 20 urls we found
article_body = []

maxNumUrl = 500; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl and num_found <= max_found:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup

    for tag in soup.find_all('a', href = True):
                childUrl = tag.get("href")
                childUrl = urllib.parse.urljoin(root_url, childUrl)
                print(childUrl)
                if childUrl not in seen and root_url in childUrl: #avoid going the some external websites
                    print("***urls.append and seen.append***")
                    urls.append(childUrl)
                    seen.append(childUrl)
                else:
                    print("######")
                    
    content = soup.find(class_ = "article-body")
    if content != None:   # making sure that the url contains such class
        main_content = content.find("p")
        main_text = main_content.text.lower()
        words = main_text.split()
        if searched_word in words:
            chosen.append(curr_url)
            num_found = num_found + 1
            article_body.append(main_text)
                
      
           

print("######HERE###ARE###THE###OUTPUT########")
print("Here are the first 20 urls containing the given word and their article body:")
for i in range(max_found):
    print("Number ", i+1)
    print(chosen[i])
    print("---------------------------------------")
    print(article_body[i])
    print("---------------------------------------")

