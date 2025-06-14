# BIKIN APLIKASI UNTUK MEMPERCEPAT PENOLAKAN MAGANG ?!?

pip install pymupdf pytesseract pillow mysql-connector-python python-dotenv PyQt5

# Setting up .env
In the root directory of the project there is a file called ".envi". In that file, replace the password with your actual mysql password  
For example, your password is "sql', then in .envi, put:
```bash
DB_PASSWORD=sql
```  
After putting your mysql password, change the file name from ".envi" to ".env"

# Installing Python Libraries
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Running The Program
```bash
python src/main.py
```
