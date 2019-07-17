from flask import request
from flask import jsonify
from wantedtest import app
from wantedtest import db
from wantedtest.models import Company, Tag, Localization, Language


@app.route('/test')
def test():
    return 'test'


@app.route('/company', methods=['GET'])
def get_company():
    company_name = request.args.get('name')
    tag_name = request.args.get('tag')
    company_list = list()
    spread_company_list = list()
    if not company_name and not tag_name:
        company_list = Company.query.all()
    elif company_name and not tag_name:
        company_list = filter_by_company_name(company_name)
    elif not company_name and tag_name:
        company_list = filter_by_tag_name(tag_name)
    elif company_name and tag_name:
        company_list_by_name = filter_by_company_name(company_name)
        company_list_by_tag = filter_by_tag_name(tag_name)
        for company_by_name in company_list_by_name:
            if company_by_name in company_list_by_tag:
                company_list.append(company_by_name)
    for company in company_list:
        spread_company_list.append(company.spread())
    response = jsonify(spread_company_list)
    response.status_code = 200
    return response


def filter_by_company_name(name):
    company_list = list()
    localization_list = Localization.query.filter(Localization.value.contains(name)).all()
    for localization in localization_list:
        company = Company.query.filter(Company.id == localization.name_base_id).first()
        if company and company not in company_list:
            company_list.append(company)
    return company_list


def filter_by_tag_name(name):
    company_list = list()
    localization = Localization.query.filter(Localization.value == name).first()
    tag = Tag.query.filter(Tag.id == localization.name_base_id).first()
    for attached in tag.attached_list:
        company_list.append(attached.company)
    return company_list


@app.route('/company', methods=['POST'])
def post_company():
    data = request.get_json()
    company_id = data.get('id')
    combined_tag_list = list()
    for language in Language.query.all():
        combined_tag_list.append(data.get('tag_'+language.code))
    if not company_id:
        response = jsonify(dict(status_code=412))
        response.status_code = 412
        return response
    company = Company.query.filter(Company.id == company_id).first()
    if not company:
        response = jsonify(dict(status_code=404))
        response.status_code = 404
        return response
    for combined_tag in combined_tag_list:
        tag_list = convert_tag_list(combined_tag)
        if type(tag_list) is list:
            company.tag_list = tag_list
            db.session.commit()
            response = jsonify(data)
            response.status_code = 200
            return response
    response = jsonify(dict(status_code=404))
    response.status_code = 404
    return response


def convert_tag_list(combined_tag):
    if combined_tag is None:
        return False
    if combined_tag is '':
        return list()
    tag_list = list()
    tag_name_list = combined_tag.split('|')
    for tag_name in tag_name_list:
        localization = Localization.query.filter(Localization.value == tag_name).first()
        if not localization:
            return False
        tag = Tag.query.filter(Tag.id == localization.name_base_id).first()
        if not tag:
            return False
        tag_list.append(tag)
    return tag_list



