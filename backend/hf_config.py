# backend/hf_config.py
import os
from dotenv import load_dotenv

load_dotenv()

class HFConfig:
    HF_TOKEN = os.getenv('HF_TOKEN')
    
    @classmethod
    def is_configured(cls):
        return cls.HF_TOKEN is not None and cls.HF_TOKEN != ''