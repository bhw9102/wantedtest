from os import path
from wantedtest import db
from wantedtest.models import Company


def create_company():
    company = Company(id=1, name='test')
    db.session.add(company)
    db.session.commit()


db.create_all()
create_company()