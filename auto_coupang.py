import hmac
import hashlib
import binascii
import os
import time
import requests
import json
import urllib.request
from selenium import webdriver
import secrets
from urllib.parse import urlencode
from PIL import Image
from io import BytesIO

class coupang:
  def generateHmac(method, url, secretKey, accessKey):
      path, *query = url.split("?")
      os.environ["TZ"] = "GMT+0"
      datetime = time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
      message = datetime + method + path + (query[0] if query else "")
      signature = hmac.new(bytes(secretKey, "utf-8"),
                          message.encode("utf-8"),
                          hashlib.sha256).hexdigest()

      return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetime, signature)

  def getProduct(request_method, authorization, keyword, limit):
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)
    url = "{}{}".format(DOMAIN, URL)
    response = requests.request(method=request_method, url=url, headers={ "Authorization": authorization, "Content-Type": "application/json;charset=UTF-8" })
    retdata = json.dumps(response.json(), indent=4).encode('utf-8')
    jsondata = json.loads(retdata)
    data = jsondata['data']
    productdata = data['productData']
    return productdata
  
  def makeProductContent(each_product):
    if not os.path.isdir('imgs'): 
      os.makedirs('imgs')
    imgpath = os.getcwd() + r"/imgs"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
    options.add_argument("lang=ko_KR")
    webdriverpath = os.getcwd() + r"/chromedriver"
  
    driver = webdriver.Chrome(webdriverpath, options=options)
    time.sleep(5)

    producturl = each_product['productUrl']
    driver.get(producturl)
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
    time.sleep(5)

    title = driver.find_element_by_class_name("prod-buy-header__title").text
    price = driver.find_element_by_class_name("total-price").find_element_by_tag_name('strong').text
    # img = driver.find_elements_by_xpath("//*[@class='detail-item']//img") # 쿠팡 제품 상세페이지 이미지 가져오는 코드 -> 너무 이미지가 천차만별
    img = driver.find_elements_by_class_name("prod-image__detail")[0]
    img_src = img.get_attribute('src')
    fname = secrets.token_hex(16)[0:10] + ".png"
    fnamefull = imgpath + "/" + fname
    urllib.request.urlretrieve(img_src, fnamefull)
    img = [('image', (fname, open(fnamefull, 'rb'), 'image/png', {'Expires': '0'}))]
    # images = []
    # for each_img in img:
    #   src = each_img.get_attribute('src')
    #   if 'vendor_inventory' not in src and ('thumbnail' not in src or 'remote' not in src):
    #     continue
    #   fname = secrets.token_hex(16)[0:10] + ".png" 
    #   fnamefull = imgpath + "/" + fname
    #   urllib.request.urlretrieve(src, fnamefull)
    #   images.append(('image', (fname, open(fnamefull, 'rb'), 'image/png', {'Expires': '0'})))
    driver.close()
    return title, producturl, price, img
