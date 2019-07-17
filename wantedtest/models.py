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

    def spread(self):
        """
        회사 정보를 펼친 데이터로 재구성한다.
        :return:
        """
        id = dict(id=self.id)
        company_name = self.spread_company_name()
        tag = self.spread_tag()
        return {**id, **company_name, **tag}

    def spread_company_name(self):
        spread_data = dict(company_ko='', company_en='', company_ja='')
        for language in Language.query.all():
            company_localization = Localization.query\
                .filter(Localization.name_base_id == self.id, Localization.language_id == language.id).first()
            if company_localization:
                spread_data['company_'+language.code] = company_localization.value
        return spread_data

    def spread_tag(self):
        tag_list_lang = dict()
        spread_data = dict()
        for language in Language.query.all():
            tag_list_lang[language.code + '_list'] = list()
            for tag in self.tag_list:
                tag_localization = Localization.query\
                    .filter(Localization.name_base_id == tag.id, Localization.language_id == language.id).first()
                tag_list_lang[language.code + '_list'].append(tag_localization.value)
            spread_data['tag_'+language.code] = '|'.join(tag_list_lang[language.code + '_list'])
        return spread_data


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
    company = relationship(Company, backref=backref('attached_list', cascade='all, delete-orphan'))
    tag = relationship(Tag, backref=backref('attached_list', cascade='all, delete-orphan'))


class Localization(db.Model):
    """
    각 번역 대상들의 언어별 번역 데이터
    Many to Many relationship
    """
    __tablename__ = 'localization'
    id = db.Column(db.Integer, primary_key=True)
    name_base_id = db.Column(db.Integer, db.ForeignKey('name_base.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    name_base = relationship(NameBase, backref=backref('localizations', cascade='all, delete-orphan'))
    language = relationship(Language, backref=backref('localizations', cascade='all, delete-orphan'))
    value = db.Column(db.String(40), nullable=False)

