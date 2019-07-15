from wantedtest import db
from wantedtest import app


@app.route('/test')
def test():
    return 'test'


