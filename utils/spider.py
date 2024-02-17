# ----------------------- Modules -------------------------------- #
import requests
from bs4 import BeautifulSoup
import time, os, sys
import pandas as pd
from utils.cleaning_data import clean_and_convert
from utils.read_Data import read_file


# ----------------------- Save Data ------------------------------ #
def Saving_Data(Links,Heading,Price,Seller,Sold_Items,Country,Status,Seller_Rank,Shipping):
    # Saving the data
    df = pd.DataFrame({'Heading':Heading,'Price':Price,'Seller':Seller,'Sold_Items':Sold_Items,'Country':Country,'Status':Status,'Seller_Rank':Seller_Rank,'Shipping':Shipping})
    df.to_csv('Input/Items.csv', index=False, encoding='utf-8',mode='a',header=False)
    
    # Saving the links
    df = pd.DataFrame({'Links of Items':Links})
    df.to_csv('Input/Links.csv', index=False, encoding='utf-8',mode='a',header=False)


def Start(self):
    # ----------------------- Proxy Server ---------------------------- #
    with open('utils/txt_files/valid_proxy.txt', 'r') as f:
        proxies = f.read().split('\n')


    # --------------------- Getting Page no. ------------------------- #
    with open('utils/txt_files/page_no.txt', 'r') as f:
        page_no = f.read().split('\n')

    # converting in integer
    page_no = int(page_no[0])

    # ------------------------- Program ------------------------------ #
    # Running till 1M data
    while True:

        # ------------------------ Lists --------------------------------- #
        Links,Heading,Price,Seller,Sold_Items,Country,Status,Seller_Rank,Shipping = [],[],[],[],[],[],[],[],[]

        # Checking link length to terminate loop after getting 1M+ data
        if os.path.getsize('Input/Links.csv') > 1001000:
            break
        
        
        # Getting the required Url
        web = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Books&_sacat=0&_ipg=240&_pgn={page_no}'


        # Using the proxy
        res = requests.get(web, proxies={'http': proxies[page_no % len(proxies)]})
        time.sleep(10)


        # Making soup
        soup = BeautifulSoup(res.text, 'html.parser')


        try:
            # Getting the data
            data = soup.find('div', class_='srp-river-results clearfix')
            for val in data.find_all('div', class_='s-item__info clearfix'):
                # Getting the links
                link = val.find('a', attrs={'class':'s-item__link'})
                if link is not None:
                    Links.append(link['href'])
                else:
                    Links.append("None")


                # Getting the heading
                heading = val.find('span', attrs={'role':'heading'})            
                if heading is not None:
                    Heading.append(heading.text)
                else:
                    Heading.append("None")


                # Getting the price
                price = val.find('span', attrs={'class':'s-item__price'})
                if price is not None:
                    Price.append(price.text)
                else:
                    Price.append("None")


                # Getting the seller
                seller = val.find('span', attrs={'class':'s-item__seller-info-text'})
                if seller is not None:
                    Seller.append(seller.text)
                else:
                    Seller.append("None")


                # Getting the sold items
                sold_item = val.find('span', attrs={'class':'s-item__dynamic s-item__quantitySold'})
                if sold_item is not None:
                    Sold_Items.append(sold_item.text)
                else:
                    Sold_Items.append("None")


                # Getting the country
                country = val.find('span', attrs={'class':'s-item__location s-item__itemLocation'})
                if country is not None:
                    Country.append((country.text)[5:])
                else:
                    Country.append("None")


                # Getting the status
                status = val.find('span', attrs={'class':'SECONDARY_INFO'})
                if status is not None:
                    Status.append(status.text)
                else:
                    Status.append("None")


                # Getting the seller rank
                seller_rank = val.find('span', attrs={'class':'s-item__etrs-text'})
                if seller_rank is not None:
                    Seller_Rank.append(seller_rank.text)
                else:
                    Seller_Rank.append("None")


                # Getting the shipping
                shipping = val.find('span', attrs={'class':'s-item__shipping s-item__logisticsCost'})
                if shipping is not None:                
                    Shipping.append(shipping.text)
                else:
                    Shipping.append("None")


            # Converting the data
            Price = clean_and_convert(Price)
            Sold_Items = clean_and_convert(Sold_Items)
            Shipping = clean_and_convert(Shipping)


            # Incrementing page no.
            page_no += 1

            # Printing page no. in csv
            with open('utils/txt_files/page_no.txt', 'w') as f:
                f.write(str(page_no))

        except:
            continue
        
        finally:
            # Saving data in csv
            Saving_Data(Links,Heading,Price,Seller,Sold_Items,Country,Status,Seller_Rank,Shipping)

            # Sending the scrapped data
            self.scrappedData += read_file("Items.csv")
            self.scrapingIterationFinished.emit(self.scrappedData)

if __name__ == '__main__':
    Start()