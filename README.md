# # auto_coupang_partners
쿠팡 파트너스 API와 네이버 API를 이용해 쿠팡 파트너스의 물건을 네이버 블로그에 포스팅 합니다.

### Python Version
* Python 3.8.0

### Chromedriver 설치

```
webdriverpath = os.getcwd() + r"/chromedriver"
```
Chromedriver를 설치하고 설치 경로를 본인 환경에 맞게 변경해줍니다.
코드는 프로젝트 폴더에 있다는 가정하에 작성되었습니다.

### config.py 파일 생성
- config.py 파일을 다른 파일과 같은 위치에 생성해줍니다.
- 아래와 같은 형식으로 네이버 Key와 쿠팡 Key를 넣어줍니다.
```
API_KEY = {
  'NAVER_CLIENT_ID': 'xxxxxxxxxxxxxxxxx',
  'NAVER_CLIENT_SECRET': 'xxxxxxxxxx',
  'COUPANG_ACCESS_KEY': 'xxxxxxxxxxxxxxxxxxxxxxxxx',
  'COUPANG_SECRET_KEY': 'xxxxxxxxxxxxxxxxxxxxxxxxx'
}
```
- 위 파일은 main.py에서 사용하기 때문에 넣어서 사용해주시면 편하게 이용하실 수 있습니다.

### API KEY 입력 및 네이버 로그인
  - 네이버 로그인을 위한 ID와 PW를 입력합니다.
  - 네이버 블로그 API를 이용하기 위한 KEY를 입력합니다. (client_id, client_secret)
  - 쿠팡 파트너스에서 발급 받은 KEY를 입력합니다. (ACCESS_KEY, SECRET_KEY)
  - 쿠팡에서 가져올 상품의 카테고리를 입력합니다.
  - 가져올 상품의 개수를 입력합니다.
  - 네이버 블로그에 포스팅할 카테고리 번호를 입력합니다.
  
