from wantedtest import db
from sqlalchemy.orm import relationship, backref


class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(5), nullable=False)
    name_base_list = relationship('NameBase', secondary='localization')


class NameBase(db.Model):
    __tablename__ = 'name_base'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    language = relationship('Language', secondary='localization')


class Company(NameBase):
    """
    회사 데이터
    name : 각 회사를 대표할 수 있는 회사명, 각 언어 대응은 따로 한다.
    """
    __tablename__ = 'company'
    id = db.Column(db.Integer, db.ForeignKey('name_base.id'), primary_key=True)
    tag_list = relationship('Tag', secondary='attaching')


class Tag(NameBase):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, db.ForeignKey('name_base.id'), primary_key=True)
    company_list = relationship('Company', secondary='attaching')


class Attaching(db.Model):
    __tablename__ = 'attaching'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    company = relationship(Company, backref=backref('attaching', cascade='all, delete-orphan'))
    tag = relationship(Tag, backref=backref('attaching', cascade='all, delete-orphan'))


class Localization(db.Model):
    __tablename__ = 'localization'
    id = db.Column(db.Integer, primary_key=True)
    name_base_id = db.Column(db.Integer, db.ForeignKey('name_base.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    name_base = relationship(NameBase, backref=backref('localization', cascade='all, delete-orphan'))
    language = relationship(Language, backref=backref('localization', cascade='all, delete-orphan'))
    value = db.Column(db.String(40), nullable=False)

