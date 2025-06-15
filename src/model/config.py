import os

# Database MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', #sesuiakan dengan sql masing-masing
    'password': 'root', #sesuaikan dengan sql masing-masing
    'database': 'ats_system'
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_ROOT = os.path.join(BASE_DIR, '..', '..')      
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
CV_DIR = os.path.join(DATA_DIR, 'cv')

# Pengaturan pencarian
MAX_RESULTS = 10
SIMILARITY_THRESHOLD = 2