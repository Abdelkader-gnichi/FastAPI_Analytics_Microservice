from decouple import config

POSTGRES_USER = config('POSTGRES_USER', cast=str, default='')
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=str, default='')
POSTGRES_DB = config('POSTGRES_DB', cast=str, default='')
POSTGRES_HOST = config('POSTGRES_HOST', cast=str, default='')
POSTGRES_PORT = config('POSTGRES_PORT', cast=str, default='')


DATA_BASE_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"