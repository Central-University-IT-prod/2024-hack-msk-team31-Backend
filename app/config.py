from envparse import env

if not env.bool("RUNNING_IN_DOCKER", default=False):
    env.read_envfile(".env")


DATABASE_URL = env.str("DATABASE_URL").replace("postgres://", "postgresql://")
SERVER_URLS = env.list("SERVER_URLS", default=[])

SMTP_CONFIG_EMAIL = env.str("SMTP_CONFIG_EMAIL")
SMTP_CONFIG_PASSWORD = env.str("SMTP_CONFIG_PASSWORD")
SMTP_CONFIG_HOST = env.str("SMTP_CONFIG_HOST")
SMTP_CONFIG_PORT = env.int("SMTP_CONFIG_PORT")
