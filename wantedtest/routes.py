from flask import request
from wantedtest import app
from wantedtest import db
from wantedtest.models import Company, Tag, Localization


@app.route('/test')
def test():
    return 'test'


@app.route('/company')
def company():
    company_name = request.args.get('name')
    tag = request.args.get('tag')
    company_list = list()
    if company_name and not tag:
        print('company name : ', company_name)
        localization_list = Localization.query.filter(Localization.value.contains(company_name)).all()
        for localization in localization_list:
            company = Company.query.filter(Company.id == localization.name_base_id).first()
            if company:
                company_list.append(company.spread())
    print('company list : ', company_list)
    return 'test'


