import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd 
import time 
url = 'https://www.skechers.com/women/shoes/athletic-sneakers/?start=0&sz=168'
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(
    "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome('D:/chromedriver_win32/chromedriver.exe',options=options)
driver.get(url)
time.sleep(6)
pageSource = driver.page_source
soup = BeautifulSoup(pageSource, 'html.parser')
content= soup.find_all('div',class_='col-6 col-sm-4 col-xl-3 mb-2 mb-md-1 mb-lg-4 px-lg-3') 
skechersshoes=[]
#products_elements = driver.find_elements_by_xpath("//div[@class='product']")
#pid = [product.get_attribute('data-pid') for product in products_elements]
for item in content:
    #Product_id
    try:
        pid = item.select_one('div.product')['data-pid']
    except:
        pid=''
    #Product_Name
    try:
        patitle = item.find('div', class_='pdp-link c-product-tile__title__wrap')
        title =patitle.find('a',class_ ='link c-product-tile__title').text
    except:
        title=''
    # Gender_Selection
    try:
        gender = item.find('div',class_='c-product-tile__gender').text
    except:
        gender=''
    gender= gender[1:-1]
    # Product_Price 
    try:
        sprice = item.find('div',class_ ='price')
        sbprice = sprice.find('span',class_ ='sales')
        sale_price = sbprice.find('span',class_= 'value').text
    except:
        sale_price=''
    sale_price = sale_price.rstrip(',')
    sale_price= sale_price[1:-1]
    # Product_links
    try:
        links = item.find('a',{'class': 'link c-product-tile__title'})['href']
    except:
        links=''
    complete_link = ('https://www.skechers.com'+links)
    # Product_orignalprice_Sale
    try:
        ssale= item.find('span',class_='strike-through list d-inline-block')
        sale = ssale.find('span',{'class':'value'})['content']
        rdollar= '$'
        orignal_price =f'{rdollar}{sale}'
    except:orignal_price=''
    
    
    orignal_price= orignal_price[1:-1]
    # Product_Exclusive
    try:
        aexclusive= item.find('div', class_ = 'image-container c-product-tile__image-container')
        exclusive =item.find('span', class_ = 'c-product-tile__badge badge badge-primary').text
    except:
        exclusive=''
    exclusive= exclusive[1:-1]
    # Product_Wide
    try:
        inwide = item.find('div',class_= 'c-product-tile__also-in').text
    except:
        inwide=''
    inwide= inwide[1:-1]
    # Product_Color
    try:
        color =item.find('div', class_ = 'c-product-tile__color-swatches__label').text
    except:
        color=''
    color= color[1:-1]
    # Product_Promotion
    try:
       
        promotion =item.find('div', class_ = 'promotion').text.strip()
    except:
        promotion=''
    promotion= promotion[1:-1]
    
    
    print(pid,title,gender, orignal_price,sale_price,complete_link,exclusive,color,promotion,inwide)

    skechers={
            'product_id': pid,
            'productname':title,
            'Gender':gender,
            'product_color':color,
            'product_price': orignal_price,
            'Sale Price':sale_price,
            'Wide_badge':inwide,
            'promotion': promotion,
            'exclusive': exclusive,
            'links': complete_link
    }
    skechersshoes.append(skechers)
df = pd.DataFrame(skechersshoes)
print(df.head())
df.to_csv('skechers.csv')




