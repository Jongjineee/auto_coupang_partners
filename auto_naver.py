# coding: utf-8
 
import sys
import os
import urllib.request
import requests
import json
import re
import auto_coupang
import urllib.request
from selenium import webdriver
from urllib.parse import urlencode

class naverMgr:
  def __init__(self, **kwargs):
    self.options = webdriver.ChromeOptions()
    self.options.add_argument('headless')
    self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
    self.webdriverpath = os.getcwd() + r"/chromedriver"

  def get_logintoken(self, id, pw, cid, csec, cburl):
    driver = webdriver.Chrome(self.webdriverpath, options=self.options)
    driver.implicitly_wait(5)

    driver.get('https://nid.naver.com/nidlogin.login')
    driver.execute_script("document.getElementsByName('id')[0].value=\'"+ id + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'"+ pw + "\'")
    driver.find_element_by_xpath('//*[@id="label_login_chk"]').click()
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    driver.implicitly_wait(10)

    state = "Blog" # 아무거나 상관없음
    req_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=%s' % (cid, cburl, state)
    response = requests.request(method='GET', url=req_url, headers={ "Content-Type": "application/json;charset=UTF-8" })

    driver.get(req_url)
    driver.implicitly_wait(5)

    # 첫 실행시 블로그글쓰기 권한 체크위해를 위한 코드
    try:
      driver.find_element_by_xpath('//*[@id="profile_optional_list"]/span/label').click()
      driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[2]/button').click()
    except:
      pass

    redirect_url = driver.current_url
    temp = re.split('code=', redirect_url)
    code = re.split('&state=', temp[1])[0]
    driver.quit()

    url = 'https://nid.naver.com/oauth2.0/token?'
    data = 'grant_type=authorization_code' + '&client_id=' + cid + '&client_secret=' + csec + '&redirect_uri=' + cburl + '&code=' + code + '&state=' + state
    request = urllib.request.Request(url, data=data.encode("utf-8"))
    request.add_header('X-Naver-Client-Id', cid)
    request.add_header('X-Naver-Client-Secret', cburl)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
      response_body = response.read()
      js = json.loads(response_body.decode('utf 8'))
      token = js['access_token']
      return token
    else:
      print("Error Code:", rescode)
      return ""

  def write_product(self, blogtoken, title, category_number, contents, img):
    blogheader = "Bearer " + blogtoken # Bearer 다음에 공백 추가
    blogwriteapi = "https://openapi.naver.com/blog/writePost.json"
    blogdata = {'title': title, 'categoryNo': category_number, 'contents': contents}
    blogheaders = {'Authorization': blogheader }

    response = requests.post(blogwriteapi, headers=blogheaders, files=img, data=blogdata)
    rescode = response.status_code
    return rescode

if __name__ == '__main__':
  # 네이버
  id = input('네이버 아이디를 입력하세요 : ')
  pw = input('네이버 비밀번호를 입력하세요 : ')
  client_id = input('네이버 API client_id를 입력하세요 : ')
  client_secret = input('네이버 API client_secret을 입력하세요 : ')
  callback_url = 'http://localhost:8080/'
  nav = naverMgr()
  token = nav.get_logintoken(id, pw, client_id, client_secret, callback_url)
  
  # 쿠팡
  method = 'GET'
  ACCESS_KEY = input('쿠팡 파트너스 ACCESS_KEY를 입력하세요 : ')
  SECRET_KEY = input('쿠팡 파트너스 SECRET_KEY를 입력하세요 : ')
  keyword = input("쿠팡 에서 가져올 keyword 입력하세요")
  limit = input("가져올 아이템의 개수를 입력하세요")
  category_number = int(input("네이버 블로그의 category number를 입력하세요"))
  URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)
  coupang = auto_coupang.coupang
  authorization = coupang.generateHmac(method, URL, SECRET_KEY, ACCESS_KEY)		# HMAC 생성
  productdata = coupang.getProduct(method, authorization, keyword, limit)
  for each_product in productdata:
    title, producturl, price, img = coupang.makeProductContent(each_product)
    contents_title = "[" + keyword + "추천" + "]" + title
    contents = f"<blockquote><div><p><span>{keyword} 추천</span></p></div></blockquote><div position='relative' margin-right='auto' margin-left='auto'><img src='#0' width='410px' /></div> <div text-align='center'><p font-size='24px' font-weight='bold' color='#ae0000'>{price}</div> <div text-align='center'><p font-size='24px'><a href={producturl}>쿠팡 상품 상세정보 확인하기</a></div> <div text-align='center'><p font-size='24px'><a href={producturl}>상품평 / 상품문의 / 배송.교환.반품 안내</a></div> <div margin-top='50px' font-size='13px'>본 포스팅은 파트너스 활동을 통해 일정액의 수수료를 제공받을 수 있습니다.</div>"
    ret = nav.write_product(token, contents_title, category_number, contents, img)
    if (ret == 200):
      print('성공')
    else:
      print('실패')
