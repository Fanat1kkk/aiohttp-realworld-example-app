SECRET_KEY = 'secret'

INSTALLED_APPS = [
    'authentication',
    'profiles',
    'articles'
]

MODELS = ["{}.models".format(app) for app in INSTALLED_APPS]

DB_URL = "sqlite://db.sqlite3"
DB_URL_TEST = "sqlite://:memory:"
# DB_URL = "postgres://postgres:postgres@0.0.0.0:5432/postgres"
# DB_URL_TEST = "postgres://postgres:postgres@0.0.0.0:5432/test_{}"
