import os

from dynaconf import FlaskDynaconf


def init_app(app, config_env):
    # configure Dynaconf (ENV_FOR_DYNACONF drives environment selection)
    env_name = config_env or os.environ.get("ENV_FOR_DYNACONF") or "default"
    os.environ["ENV_FOR_DYNACONF"] = env_name

    # initialize dynaconf integration
    FlaskDynaconf(
        app,
        settings_files=["settings.toml", ".secrets.toml"],
        env_switcher="ENV_FOR_DYNACONF",
        environments=True,
        load_dotenv=True,
        envvar_prefix="POKEMON",
    )
