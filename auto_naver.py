# coding: utf-8
 
import sys
import os
import urllib.request
import requests
import json
import re
import urllib.request
from selenium import webdriver

class naver:
  def get_logintoken(id, pw, client_id, client_secret, callback_url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36")
    webdriver_path = os.getcwd() + r"/chromedriver"

    driver = webdriver.Chrome(webdriver_path, options=options)
    driver.implicitly_wait(5)

    driver.get('https://nid.naver.com/nidlogin.login')
    driver.execute_script("document.getElementsByName('id')[0].value=\'"+ id + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'"+ pw + "\'")
    driver.find_element_by_xpath('//*[@id="label_login_chk"]').click()
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    driver.implicitly_wait(10)

    state = "Blog" # 아무거나 상관없음
    request_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=%s' % (client_id, callback_url, state)
    response = requests.request(method='GET', url=request_url, headers={ "Content-Type": "application/json;charset=UTF-8" })

    driver.get(request_url)
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
    data = 'grant_type=authorization_code' + '&client_id=' + client_id + '&client_secret=' + client_secret + '&redirect_uri=' + callback_url + '&code=' + code + '&state=' + state
    request = urllib.request.Request(url, data=data.encode("utf-8"))
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', callback_url)

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

  def write_product(blog_token, title, category_number, contents, img):
    blog_header = "Bearer " + blog_token # Bearer 다음에 공백 추가
    blog_write_api = "https://openapi.naver.com/blog/writePost.json"
    blog_data = {'title': title, 'categoryNo': category_number, 'contents': contents}
    blog_headers = {'Authorization': blog_header }

    response = requests.post(blog_write_api, headers=blog_headers, files=img, data=blog_data)
    rescode = response.status_code
    return rescode
