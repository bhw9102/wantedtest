import config
from xlrd import open_workbook
from wantedtest import db
from wantedtest.models import Company, Tag, Attaching, Language, Localization


def load_keys(sheet):
    return [sheet.cell_value(0, i) for i in range(sheet.ncols)]


def add_rows(sheet, model):
    keys = load_keys(sheet)
    for row in range(sheet.nrows - 1):
        data = dict()
        for col, key in enumerate(keys):
            data[key] = sheet.cell_value(row + 1, col)
            if type(data[key]) is float:
                data[key] = int(data[key])
        m = model(**data)
        db.session.add(m)
    db.session.commit()


def open_sheet(file_name, sheet_name):
    data_path = config.BASE_DIR + '/wantedtest/import/' + file_name
    wb = open_workbook(data_path)
    return wb.sheet_by_name(sheet_name)


def import_language():
    sheet = open_sheet('language.xlsx', 'language')
    add_rows(sheet=sheet, model=Language)


def load_company_list():
    sheet = open_sheet('wanted_temp_data.xlsx', 'sample')
    keys = load_keys(sheet=sheet)
    company_list = list()
    for row in range(sheet.nrows - 1):
        row_data = dict()
        row_data['name'] = ''
        for col, key in enumerate(keys):
            row_data[key] = sheet.cell_value(row + 1, col)
            if row_data['name'] == '' and row_data[key] != '':
                row_data['name'] = row_data[key]
        company_list.append(row_data)
    return company_list


def import_company_list(company_list):
    for company_data in company_list:
        company = Company(name=company_data.get('name'))
        db.session.add(company)
        db.session.commit()
        company = Company.query.filter(Company.name == company_data.get('name')).first()
        for key, value in company_data.items():
            import_company_detail(company, key, value)
    pass


def import_company_detail(company, key, value):
    if value == '':
        return
    key_opt = key.split('_')
    if key_opt[0] == 'company':
        import_localization(company.id, key_opt[1], value)
    elif key_opt[0] == 'tag':
        pass


def import_localization(name_base_id, code, value):
    language = Language.query.filter(Language.code == code).first()
    localization = Localization(name_base_id=name_base_id, language_id=language.id, value=value)
    db.session.add(localization)
    db.session.commit()
    return


db.reflect()
db.drop_all()
db.create_all()
import_language()
company_list = load_company_list()
import_company_list(company_list)



