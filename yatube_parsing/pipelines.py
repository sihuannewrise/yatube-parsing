import scrapy
from datetime import datetime
from sqlalchemy import create_engine, Column, Date, Integer, String, Text
from sqlalchemy.orm import Session, declarative_base, declared_attr


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class MondayPost(Base):
    author = Column(String(200))
    text = Column(Text())
    date = Column(Date())

    def __repr__(self):
        return f'MONDAYPOST {self.author} {self.text[:15]}'


class MondayPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///monday-post.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        post_date = datetime.strptime(item['date'], '%d.%m.%Y')
        if not post_date.weekday():
            post = MondayPost(
                author=item['author'],
                text=item['text'],
                date=post_date,
            )
            self.session.add(post)
            self.session.commit()
            return item
        else:
            raise scrapy.exceptions.DropItem(
                'Этотъ постъ написанъ не въ понедѣльникъ'
            )

    def close_spider(self, spider):
        self.session.close()
