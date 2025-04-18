from decouple import config

DATA_BASE_URL = config('DATA_BASE_URL', cast=str, default='')