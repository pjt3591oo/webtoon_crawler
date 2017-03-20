from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from database import init_db


class WebtoonCommends(Base):
    __tablename__ = 'webtoonCommends'
    id = Column(Integer, primary_key=True)
    titleId = Column(String(250))
    no = Column(String(250))
    commentNo = Column(String(250))
    content = Column(String(250))

    def __init__(self, titleId, no, commentNo, content):
        self.titleId = titleId
        self.no = no
        self.commentNo = commentNo
        self.content = content

    def __repr__(self):
        return "<TbTest('%d', '%s', '%s', '%s', '%s'>" % (self.id, str(self.titleId), self.no, self.commentNo, self.content)


init_db()
