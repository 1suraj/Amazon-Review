
import urllib
from bs4 import BeautifulSoup
import time


url="https://www.amazon.in/Maniac-Fullsleeve-Round-Cotton-Tshirt/product-reviews/B06Y3VLQBZ/ref=cm_cr_dp_d_acr_sr?ie=UTF8&reviewerType=all_reviews"


#opened_file = open("Amazon_Review.txt","w")


rev_date_header = 'Date'
rev_title_header = 'Title'
rev_rate_header = 'Rate'
rev_text_header = 'Text'
rev_vote_header = 'Votes'
date,title,review_tx,rating=[],[],[],[]

url1st = url+"&pageNumber={}".format(1)
req = urllib.request.Request(
                url1st, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )            
url2 = urllib.request.urlopen(req)
page=url2.read().lower()
soup = BeautifulSoup(page, "lxml")
Total_Review_Count = soup.find_all('span', {'data-hook' : 'total-review-count'})[0]
Total_Review_Count = int(Total_Review_Count.text.replace(',',''))
Page_Count=round(Total_Review_Count/10)+1

print("Extracting Review from "+str(Page_Count-1)+" pages..Have patience :)")



for u in range(1,Page_Count):
    while True:
        
        try:
            
            url2nd = url+"&pageNumber={}".format(u)
            req = urllib.request.Request(
                url2nd, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )            
            url2 = urllib.request.urlopen(req)
            page=url2.read().lower()
            soup = BeautifulSoup(page, "lxml")
            time.sleep(0.1)
            
            
            for reviewList in soup.find_all('div', {'id' : 'cm_cr-review_list'}):
                for review in reviewList.find_all('div', {'class' : 'review'}):
                    rev_date_element = review.find('span',{'class' : 'review-date'})
                    rev_date = '' if (rev_date_element is None or rev_date_element.text is None) else rev_date_element.text.strip().replace(',','')
                    rev_title_element = review.find('a',{'class' : 'review-title'})
                    rev_title = '' if (rev_title_element is None or rev_title_element.text is None) else rev_title_element.text.strip().replace(',','')
                    rev_rate_element = review.find('i',{'class' : 'review-rating'})
                    rev_rate = '' if (rev_rate_element is None) else '' if rev_rate_element.find('span') is None or rev_rate_element.find('span').text is None else rev_rate_element.find('span').text.strip().replace(',','')
                    rev_text_element = review.find('span', {'class' : 'review-text'})
                    rev_text =  '' if (rev_text_element is None or rev_text_element.text is None) else rev_text_element.text.strip().replace(',','')
                    rev_vote_element = review.find('span', {'class' : 'review-votes'})
                    rev_vote =  '' if (rev_vote_element is None or rev_vote_element.text is None) else rev_vote_element.text.strip().replace(',','')
                    date.append(rev_date.strip('on '))
                    title.append(rev_title)
                    review_tx.append(rev_text)
                    rating.append(int(rev_rate[0]))
                    
#                    opened_file.write(rev_date +'|'+ rev_title +'|'+ rev_text +'|'+ rev_rate +'|'+ rev_vote +'|'+"\n")
                    
            print("Page {} Extraction Done :)".format(u))
            time.sleep(0.1)

            break # Only triggered if input is valid...
        except Exception:
            
            print('Retrying Page '+ str(u))
#opened_file.close()

import pandas as pd
df = pd.DataFrame(list(map(list, zip(date,title,review_tx,rating))),columns=['date','title','review','rating'])
df.to_csv('Review_suraj.csv', index=False)

#--------------------------------------------------------            



