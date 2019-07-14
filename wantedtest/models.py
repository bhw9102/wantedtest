from wantedtest import db
from sqlalchemy.orm import relationship, backref


class Language(db.Model):
    """
    번역될 언어 목록
    name : 언어명
    code : 언어의 코드명
    """
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    code = db.Column(db.String(5), nullable=False)
    name_base_list = relationship('NameBase', secondary='localization')


class NameBase(db.Model):
    """
    번역의 대상이 되는 Company, Tag 의 상위모델
    name : 업무 효율을 위한 대표성을 띄는 이름, 실제 각 언어별 대응은 따로한다.
    """
    __tablename__ = 'name_base'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    language = relationship('Language', secondary='localization')


class Company(NameBase):
    """
    회사 데이터
    """
    __tablename__ = 'company'
    id = db.Column(db.Integer, db.ForeignKey('name_base.id'), primary_key=True)
    tag_list = relationship('Tag', secondary='attaching')


class Tag(NameBase):
    """
    태그 데이터
    """
    __tablename__ = 'tag'
    id = db.Column(db.Integer, db.ForeignKey('name_base.id'), primary_key=True)
    company_list = relationship('Company', secondary='attaching')


class Attaching(db.Model):
    """
    회사별, 태그 등록 데이터
    Many to Many relationship
    """
    __tablename__ = 'attaching'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    company = relationship(Company, backref=backref('attaching', cascade='all, delete-orphan'))
    tag = relationship(Tag, backref=backref('attaching', cascade='all, delete-orphan'))


class Localization(db.Model):
    """
    각 번역 대상들의 언어별 번역 데이터
    Many to Many relationship
    """
    __tablename__ = 'localization'
    id = db.Column(db.Integer, primary_key=True)
    name_base_id = db.Column(db.Integer, db.ForeignKey('name_base.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    name_base = relationship(NameBase, backref=backref('localization', cascade='all, delete-orphan'))
    language = relationship(Language, backref=backref('localization', cascade='all, delete-orphan'))
    value = db.Column(db.String(40), nullable=False)

