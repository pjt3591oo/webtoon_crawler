import json
import sys
from urllib.parse import urlparse, parse_qs, urljoin

import requests as rq
from bs4 import BeautifulSoup

from config import CR_config as WC
from database import db_session
from models.webtoonCommends import WebtoonCommends
from models.webtoonCuts import WebToonCuts
from models.webtoons import WebToons


def save(data, file_name):
    file = open(file_name, 'a')
    file.write(data + '\n')


def get_daylywebtoons():
    '''
    요일 웹툰을 수집
    '''
    webtoon_main_url = WC.TOP_URL
    res = rq.get(webtoon_main_url)
    main_soup = BeautifulSoup(res.content, 'lxml')

    webtoon_links = [{"title": a_tag.get('title'), "link": urljoin(WC.NAVER_URL, a_tag.get('href'))}
                      for a_tag in main_soup.select('.daily_all a.title')]

    return webtoon_links


def make_link(webtoon_url, page_count):
    return webtoon_url + '&page=' + str(page_count)


def get_qs(url, key):
    url_query = urlparse(url).query
    query_dict = parse_qs(url_query)
    value = query_dict[key][0]
    return value


def get_all_webtoon(webtoon, is_save):
    '''
    해당 웹 툰의  1화 ~ 마지막까지 수집
    '''
    page_count = 1

    target_webtoons = list()
    webtoon_url = webtoon['link']
    webtoon_title = webtoon['title']

    webtoon_id = get_qs(webtoon_url, 'titleId')
    weekday = get_qs(webtoon_url, 'weekday')

    is_unlast = True

    while is_unlast:
        link = make_link(webtoon_url, page_count)

        target_webtoon_res = rq.get(link)
        webtoon_soup = BeautifulSoup(target_webtoon_res.content, 'lxml')
        a_tags = webtoon_soup.select('.viewList td.title a')

        for a_tag in a_tags:
            t = a_tag.text.replace('\n', '').replace('\r', '').replace('\t', '')
            h = urljoin(WC.NAVER_URL, a_tag.get('href'))

            if h not in target_webtoons:
                target_webtoons.append(h)
            else:
                is_unlast = False

        page_count += 1

    if is_save:
        for webtoon in target_webtoons:
            save(webtoon_title + ':' + webtoon, 'all_webtoons.txt')

    return webtoon_title.strip(), webtoon_id, weekday, target_webtoons


def data_parse(soup, url, max_commend_page=3):

    rank = soup.select('#topPointTotalNumber')[0].text
    title = soup.title.text.split(':')[0]

    titleId = str(parse_qs(urlparse(url).query)['titleId'][0])
    no = str(parse_qs(urlparse(url).query)['no'][0])

    no_title = soup.select('.tit_area .view h3')[0].text

    webtoon_cut_db = db_session.query(WebToonCuts).\
        filter(WebToonCuts.titleId == titleId).\
        filter(WebToonCuts.no == no).all()

    print(title + ' ' + no_title)

    # 웹툰 n화저장
    if not len(webtoon_cut_db):
        webtoon_cut = WebToonCuts(titleId, no, title + ' ' + no_title, rank)
        try:
            db_session.add(webtoon_cut)
            db_session.commit()
        except:
            e = sys.exc_info()[0]
        finally:
            db_session.close()

    comment_url = WC.NAVER_URL + '/comment/comment.nhn?titleId=' + titleId + '&no=' + no
    objectId = titleId + '_' + no

    page_count = 1

    u = 'http://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=comic&templateId=webtoon&pool=cbox3&_callback=jQuery1113012327623800394427_1489937311100&lang=ko&country=KR&objectId=' +objectId+ '&categoryId=&pageSize=15&indexSize=10&groupId=&listType=OBJECT&sort=NEW&_=1489937311112'

    while page_count < max_commend_page:  # True를 주면 모든 댓글을 수집함
        comment_url = make_link(u, page_count)
        header = {
            "Host": "apis.naver.com",
            "Referer": "http://comic.naver.com/comment/comment.nhn?titleId=" + titleId + "&no=" + no,
            "Content-Type": "application/javascript"
        }

        res = rq.get(comment_url, headers = header)
        soup = BeautifulSoup(res.content, 'lxml')
        try:
            content_text = soup.select('p')[0].text
            one = content_text.find('(') + 1
            two = content_text.find(');')
            content = json.loads(content_text[one:two])

            comments = content['result']['commentList']

            for comment in comments:
                contents = comment['contents']
                commentNo = comment['commentNo']

                webtoon_commend_db = db_session.query(WebtoonCommends). \
                    filter(WebtoonCommends.titleId == titleId). \
                    filter(WebtoonCommends.no == no).\
                    filter(WebtoonCommends.commentNo == commentNo)\
                    .all()
                print(titleId, no, commentNo, contents)

                if not len(webtoon_commend_db) and len(contents)< 230:
                    try:
                        webtoon_commend = WebtoonCommends(titleId, no, commentNo, contents)
                        db_session.add(webtoon_commend)
                        db_session.commit()
                    except:
                        e = sys.exc_info()[0]
                    finally:
                        db_session.close()

            if not len(comments):
                # 댓글 마지막 페이지
                break
            else:
                page_count += 1
        except:
            pass


if __name__ == "__main__":
    webtoons = get_daylywebtoons()
    for webtoon in webtoons:
        webtoon_title, title_id, weekday, target_webtoons = get_all_webtoon(webtoon, False)

        webtoon = WebToons(webtoon_title, title_id, weekday)
        webtoons_db = db_session.query(WebToons).filter(WebToons.titleId == title_id).all()

        # 웹툰이름 저장
        if not len(webtoons_db):
            try:
                db_session.add(webtoon)
                db_session.commit()
            except:
                e = sys.exc_info()[0]
            finally:
                db_session.close()

        print(webtoon_title)

        for webtoon_page in target_webtoons:
            res = rq.get(webtoon_page)
            webtoon_page_soup = BeautifulSoup(res.content, 'lxml')
            data_parse(webtoon_page_soup, webtoon_page)


