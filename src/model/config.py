import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env'))

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': os.getenv('DB_PASSWORD', ''),
    'database': 'ats_system'
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_ROOT = os.path.join(BASE_DIR, '..', '..')      
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
CV_DIR = os.path.join(DATA_DIR, 'cv')

# Pengaturan pencarian
MAX_RESULTS = 10
SIMILARITY_THRESHOLD = 2