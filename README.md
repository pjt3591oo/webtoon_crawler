# 네이버 웹툰 크롤러
해당 크롤러는 네이버의 웹툰 정보를 수집하여 디비에 저장을 하는 크롤러 입니다.

# 사용디비
```
db : mysql or mariaDB
library : sqlalchepy(orm)
```

다른 디비를 사용 할 경우 /config/DB_config.py를 수정 해 주시면 됩니다
uri만 수정하여 사용. 나머지 정보는 부가적인 정보.

# 의존 모듈 설치
```bash
$ pip3 install -r requirements.txt
```

# 크롤러 실행
```bash
$ python3 webtoon.py
```

댓글을 저장하는 기본값은 3페이지 입니다
만약 더 많은 댓글을 수직하고 싶다면 data_parse에 3번쨰 인자로 수치를 넣어 주세요 


# 디비 테이블 구성
```mysql
CREATE TABLE webtoons(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(250),
    titleId VARCHAR(250),
    weekday VARCHAR(250)
);

CREATE TABLE webtoonCuts(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    titleId VARCHAR(250),
    no VARCHAR(250),
    no_title VARCHAR(250),
    rank FLOAT(10)
);

CREATE TABLE webtoonCuts(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    titleId VARCHAR(250),
    no VARCHAR(250),
    commentNo VARCHAR(250),
    content VARCHAR(250)
);
```