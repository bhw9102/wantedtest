import config
from xlrd import open_workbook
from wantedtest import db
from wantedtest.models import Company, Tag, Attaching, Language


def load_keys(sheet):
    return [sheet.cell_value(0, i) for i in range(sheet.ncols)]


def add_rows(sheet, model):
    for row in range(sheet.nrows - 1):
        data = {}
        keys = load_keys(sheet)
        for col, key in enumerate(keys):
            data[key] = sheet.cell_value(row + 1, col)
            if type(data[key]) is float:
                data[key] = int(data[key])
        m = model(**data)
        db.session.add(m)
    db.session.commit()


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
    data_path = config.BASE_DIR + '/wantedtest/import/language.xlsx'
    dir_strings = data_path.split('/')
    dir_strings = [i for i in dir_strings]
    import_data_path = '/'.join(dir_strings)
    wb = open_workbook(import_data_path)
    target_sheet = wb.sheet_by_name('language')
    add_rows(sheet=target_sheet, model=Language)


db.reflect()
db.drop_all()
db.create_all()
create_language()



