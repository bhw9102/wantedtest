from os import path
from wantedtest import db
from wantedtest.models import Company, Tag, Attaching, Language


def create_company():
    company = Company(id=1, name='company_1')
    tag = Tag(id=1, name='tag_1')
    company.tag_list.append(tag)
    db.session.add(company)
    db.session.commit()


def create_tag():
    tag = Tag(id=2, name='tag_2')
    db.session.add(tag)
    db.session.commit()


def create_language():
    language = Language(id=1, name='Korean', code='ko')
    db.session.add(language)
    db.session.commit()


db.reflect()
db.drop_all()
db.create_all()
create_company()
create_tag()
create_language()\

