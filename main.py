import auto_coupang
import auto_naver
import urllib.request
import config


if __name__ == '__main__':
  # 네이버
  id = input('네이버 아이디를 입력하세요 : ')
  pw = input('네이버 비밀번호를 입력하세요 : ')
  client_id = config.API_KEY['NAVER_CLIENT_ID']
  client_secret = config.API_KEY['NAVER_CLIENT_SECRET']
  callback_url = 'http://localhost:8080/'
  naver = auto_naver.naver
  token = naver.get_logintoken(id, pw, client_id, client_secret, callback_url)
  
  # 쿠팡
  method = 'GET'
  ACCESS_KEY = config.API_KEY['COUPANG_ACCESS_KEY']
  SECRET_KEY = config.API_KEY['COUPANG_SECRET_KEY']
  keyword = input("쿠팡 에서 가져올 keyword 입력하세요")
  limit = input("가져올 아이템의 개수를 입력하세요")
  category_number = int(input("네이버 블로그의 category number를 입력하세요"))
  URL = "/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=" + urllib.parse.quote(keyword) + "&limit=" + str(limit)
  coupang = auto_coupang.coupang
  authorization = coupang.generate_hmac(method, URL, SECRET_KEY, ACCESS_KEY)		# HMAC 생성
  products = coupang.get_product(method, authorization, keyword, limit)
  for product in products:
    title, producturl, price, img = coupang.make_product_content(product)
    contents_title = "[" + keyword + " 추천" + "]" + title
    contents = f"<blockquote><div><p><span>{keyword} 추천</span></p></div></blockquote><div position='relative' margin-right='auto' margin-left='auto'><img src='#0' width='410px' /></div> <div text-align='center'><p font-size='24px' font-weight='bold' color='#ae0000'>{price}원</div> <div text-align='center'><p font-size='24px'><a href={producturl}>쿠팡 상품 상세정보 확인하기</a></div> <div text-align='center'><p font-size='24px'><a href={producturl}>상품평 / 상품문의 / 배송.교환.반품 안내</a></div> <div margin-top='50px' font-size='13px'>본 포스팅은 파트너스 활동을 통해 일정액의 수수료를 제공받을 수 있습니다.</div>"
    write_product = naver.write_product(token, contents_title, category_number, contents, img)
    if (write_product == 200):
      print('성공')
    else:
      print('실패')