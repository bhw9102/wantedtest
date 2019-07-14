from wantedtest import db
from sqlalchemy.orm import relationship, backref


class Company(db.Model):
    """
    회사 데이터
    name : 각 회사를 대표할 수 있는 회사명, 각 언어 대응은 따로 한다.
    """
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    tag_list = relationship('Tag', secondary='attaching')


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    company_list = relationship('Company', secondary='attaching')


class Attaching(db.Model):
    __tablename__ = 'attaching'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    company = relationship(Company, backref=backref('attaching', cascade='all, delete-orphan'))
    tag = relationship(Tag, backref=backref('attaching', cascade='all, delete-orphan'))


class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(5), nullable=False)



