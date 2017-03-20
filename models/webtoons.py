from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from database import init_db


class WebToons(Base):
    __tablename__ = 'webtoons'
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    titleId = Column(String(250))
    weekday = Column(String(250))

    def __init__(self, title, titleId, weekday):
        self.title = title
        self.titleId = titleId
        self.weekday = weekday

    def __repr__(self):
        return "<TbTest('%d', '%s', '%s', '%s'>" % (self.id, str(self.title), self.titleId, self.weekday)


init_db()
