from flask import request
from flask import jsonify
from wantedtest import app
from wantedtest import db
from wantedtest.models import Company, Tag, Localization, Language


@app.route('/company', methods=['GET'])
def get_company():
    """
    입력한 파라미터를 통해 회사 목록을 검색한다.
    :return: 회사 목록
    """
    company_name = request.args.get('name')
    tag_name = request.args.get('tag')
    company_list = list()
    spread_company_list = list()
    if not company_name and not tag_name:
        # 아무런 파라미터를 입력하지 않았을 때, 모든 회사 목록을 반환한다.
        company_list = Company.query.all()
    elif company_name and not tag_name:
        # 회사 이름 파라미터만 입력했을 때, 회사 이름으로 검색된 회사 목록을 반환한다.
        company_list = filter_by_company_name(company_name)
    elif not company_name and tag_name:
        # 태그 이름 파라미터만 입력했을 때, 태그 이름으로 검색된 회사 목록을 반환한다.
        company_list = filter_by_tag_name(tag_name)
    elif company_name and tag_name:
        # 회사 이름과 태그 이름 파라미터를 동시에 입력했을 떄, 두 검색 조건에 모두 해당하는 회사 목록을 반환한다.
        company_list_by_name = filter_by_company_name(company_name)
        company_list_by_tag = filter_by_tag_name(tag_name)
        for company_by_name in company_list_by_name:
            if company_by_name in company_list_by_tag:
                company_list.append(company_by_name)
    for company in company_list:
        # 회사 목록을 반환할 때, excel 시트의 형태로 반환한다.
        spread_company_list.append(company.spread())
    response = jsonify(spread_company_list)
    response.status_code = 200
    return response


def filter_by_company_name(name):
    """
    회사 이름으로 검색된 회사 목록을 반환한다.
    :param name: 검색하고자 하는 회사 이름
    :return: 회사 이름으로 검색된 회사 목록
    """
    company_list = list()
    localization_list = Localization.query.filter(Localization.value.contains(name)).all()
    for localization in localization_list:
        company = Company.query.filter(Company.id == localization.name_base_id).first()
        if company and company not in company_list:
            company_list.append(company)
    return company_list


def filter_by_tag_name(name):
    """
    태그를 포함하고 있는 회사 목록을 반환한다.
    :param name: 검색하고자 하는 태그 이름
    :return: 태그 이름으로 검색된 회사 목록
    """
    company_list = list()
    localization = Localization.query.filter(Localization.value == name).first()
    tag = Tag.query.filter(Tag.id == localization.name_base_id).first()
    for attached in tag.attached_list:
        company_list.append(attached.company)
    return company_list


@app.route('/company', methods=['POST'])
def post_company():
    """
    회사의 태그 정보를 수정한다.
    :return:
    """
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
    response = jsonify(dict(status_code=412))
    response.status_code = 404
    return response


def convert_tag_list(combined_tag):
    """
    입력된 태그 내용을 태그 아이디 목록으로 변환하여 반환한다.
    :param combined_tag:
    :return:
    """
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



