# config.py - Konfigurasi sistem ATS
import os

# Database MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '', #pass sql
    'database': 'ats_system'
}

# Path direktori
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
CV_DIR = os.path.join(DATA_DIR, 'cv')

# Pengaturan pencarian
MAX_RESULTS = 10
SIMILARITY_THRESHOLD = 2