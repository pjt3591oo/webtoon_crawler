from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base
from database import init_db


class WebToonCuts(Base):
    __tablename__ = 'webtoonCuts'
    id = Column(Integer, primary_key=True)
    titleId = Column(String(250))   # 웹툰 번호
    no = Column(String(250))        # 웹툰 n화
    no_title = Column(String(250))  # 웹툰 n화 제목
    rank = Column(Float(10))        # 평점

    def __init__(self, titleId, no, no_title, rank):
        self.titleId = titleId
        self.no = no
        self.no_title = no_title
        self.rank = rank

    def __repr__(self):
        return "<TbTest('%d', '%s', '%s', '%s', '%s'>" % (self.id, str(self.titleId), self.no, self.no_title, self.rank)


init_db()
