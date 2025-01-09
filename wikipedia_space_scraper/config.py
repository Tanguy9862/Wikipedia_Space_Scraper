from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(dotenv_path=env_path)


class BaseConfig:
    WIKIPEDIA_URL = "https://fr.wikipedia.org/wiki/Chronologie_de_l%27exploration_spatiale"
    DATA_EXPORT_FILENAME = "historical_facts_data.json"


class LocalConfig(BaseConfig):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR_NAME = 'data'
    BASE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR_PATH = os.path.join(BASE_DIR_PATH, DATA_DIR_NAME)
    DATA_EXPORT_PATH = os.path.join(DATA_DIR_PATH, BaseConfig.DATA_EXPORT_FILENAME)


class LambdaConfig(BaseConfig):
    BUCKET_NAME = "app-space-exploration-bucket"
    DATA_EXPORT_PATH = BaseConfig.DATA_EXPORT_FILENAME


ENV = os.getenv("ENV", "local")
CONFIG = LocalConfig() if ENV == "local" else LambdaConfig()
