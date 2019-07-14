import config
from xlrd import open_workbook
from wantedtest import db
from wantedtest.models import Company, Tag, Attaching, Language, Localization

FIRST_ROW_NUM = 1


def load_keys(sheet):
    """
    시트의 첫 열을 읽어 각 행의 키를 읽는다.
    :param sheet: 작업을 수행할 시트
    :return: 키 목록
    """
    return [sheet.cell_value(0, i) for i in range(sheet.ncols)]


def add_rows(sheet, model):
    """
    시트의 각 열을 순서대로 읽어서, db에 저장한다.
    :param sheet: 작업을 수행할 시트
    :param model: 대상 모델
    :return:
    """
    keys = load_keys(sheet)
    for row in range(FIRST_ROW_NUM, sheet.nrows):
        data = dict()
        for col, key in enumerate(keys):
            data[key] = sheet.cell_value(row, col)
            if type(data[key]) is float:
                data[key] = int(data[key])
        m = model(**data)
        db.session.add(m)
    db.session.commit()


def open_sheet(file_name, sheet_name):
    """
    xlsx 파일을 열어 sheet를 불러온다.
    :param file_name: 파일명
    :param sheet_name: 파일 내의 시트명
    :return: 시트 정보
    """
    data_path = config.BASE_DIR + '/wantedtest/import/' + file_name
    wb = open_workbook(data_path)
    return wb.sheet_by_name(sheet_name)


def import_language():
    """
    번역 언어의 종류 데이터를 db에 저장한다.
    :return:
    """
    sheet = open_sheet('language.xlsx', 'language')
    add_rows(sheet=sheet, model=Language)


def load_company_list():
    """
    업체 목록 파일에서 업체 정보를 불러온다.
    :return: 업체 목록
    """
    sheet = open_sheet('wanted_temp_data.xlsx', 'sample')
    keys = load_keys(sheet=sheet)
    company_list = list()
    for row in range(FIRST_ROW_NUM, sheet.nrows):
        row_data = dict(name='')
        for col, key in enumerate(keys):
            row_data[key] = sheet.cell_value(row, col)
            if row_data.get('name') == '' and row_data[key] != '':
                row_data['name'] = row_data[key]
        company_list.append(row_data)
    return company_list


def import_company_list(company_list):
    """
    업체 목록의 내용을 분리하여, db의 각 테이블에 저장한다.
    :param company_list: 업체 목록
    :return:
    """
    for company_data in company_list:
        company = Company(name=company_data.get('name'))
        db.session.add(company)
        db.session.commit()
        company = Company.query.filter(Company.name == company_data.get('name')).first()
        for key, value in company_data.items():
            import_company_detail(company, key, value)


def import_company_detail(company, key, value):
    """
    업체의 내용을 db 테이블에 맞게 작업을 분리한다.
    :param company: DB에 저장된 업체 정보
    :param key: 업체의 속성 중에서 등록할 속성 키
    :param value: 등록할 값
    :return:
    """
    if value == '':
        return
    key_opt = key.split('_')
    if key_opt[0] == 'tag':
        import_attaching(company, value)
    if key_opt[0] == 'company':
        import_localization(company.id, key_opt[1], value)


def import_localization(name_base_id, code, value):
    """
    각 대상의 각 언어별로 번역 데이터를 저장한다.
    :param name_base_id: 번역을 저장할 대상
    :param code: 번역될 언어의 code
    :param value: 언어 종류에 따른 번역 내용
    :return:
    """
    language = Language.query.filter(Language.code == code).first()
    localization = Localization(name_base_id=name_base_id, language_id=language.id, value=value)
    db.session.add(localization)
    db.session.commit()


def import_attaching(company, tag_value_list):
    """
    각 업체에 tag를 등록한다.
    :param company: 등록할 업체
    :param tag_value_list: 등록할 태그 목록, 문자열
    :return:
    """
    if company.tag_list:
        return
    tag_value_list = tag_value_list.split('|')
    for tag_value in tag_value_list:
        localization = Localization.query.filter(Localization.value == tag_value).first()
        tag = localization.name_base
        attaching = Attaching(company_id=company.id, tag_id=tag.id)
        db.session.add(attaching)
    db.session.commit()


def import_tag():
    """
    태그 목록을 불러와서 db에 저장한다.
    :return:
    """
    sheet = open_sheet('tag.xlsx', 'tag')
    keys = load_keys(sheet)
    for row in range(FIRST_ROW_NUM, sheet.nrows):
        tag = Tag()
        for col, key in enumerate(keys):
            name = sheet.cell_value(row, col)
            if not tag.name:
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
                tag = Tag.query.filter(Tag.name == name).first()
            import_localization(tag, key, name)


db.reflect()
db.drop_all()
db.create_all()
import_language()
import_tag()
company_list = load_company_list()
import_company_list(company_list)



