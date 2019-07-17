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
        company_name = self.spread_company_name()
        tag = self.spread_tag()
        return {**company_name, **tag}

    def spread_company_name(self):
        ko = Language.query.filter(Language.code == 'ko').first()
        en = Language.query.filter(Language.code == 'en').first()
        ja = Language.query.filter(Language.code == 'ja').first()
        spread_data = dict(company_ko='', company_en='', company_ja='')
        company_ko = Localization.query \
            .filter(Localization.name_base_id == self.id, Localization.language_id == ko.id).first()
        if company_ko:
            spread_data['company_ko'] = company_ko.value
        company_en = Localization.query \
            .filter(Localization.name_base_id == self.id, Localization.language_id == en.id).first()
        if company_en:
            spread_data['company_en'] = company_en.value
        company_ja = Localization.query \
            .filter(Localization.name_base_id == self.id, Localization.language_id == ja.id).first()
        if company_ja:
            spread_data['company_ja'] = company_ja.value
        return spread_data

    def spread_tag(self):
        ko = Language.query.filter(Language.code == 'ko').first()
        en = Language.query.filter(Language.code == 'en').first()
        ja = Language.query.filter(Language.code == 'ja').first()
        tag_ko_list = list()
        tag_en_list = list()
        tag_ja_list = list()
        for tag in self.tag_list:
            tag_ko = Localization.query.filter(Localization.name_base_id == tag.id,
                                               Localization.language_id == ko.id).first()
            if tag_ko:
                tag_ko_list.append(tag_ko.value)
            tag_en = Localization.query.filter(Localization.name_base_id == tag.id,
                                               Localization.language_id == en.id).first()
            if tag_en:
                tag_en_list.append(tag_en.value)
            tag_ja = Localization.query.filter(Localization.name_base_id == tag.id,
                                               Localization.language_id == ja.id).first()
            if tag_ja:
                tag_ja_list.append(tag_ja.value)
        tag_ko = '|'.join(tag_ko_list)
        tag_en = '|'.join(tag_en_list)
        tag_ja = '|'.join(tag_ja_list)
        return dict(tag_ko=tag_ko, tag_en=tag_en, tag_ja=tag_ja)


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

