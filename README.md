# Tugas Besar 3 Strategi Algoritma 2025  
<p align="center">
<img src="https://media1.tenor.com/m/x8v1oNUOmg4AAAAd/rickroll-roll.gif" alt="Application interface" width="500"/>
</p>

## ATS Application using Exact String Matching and Fuzzy String Matching
There are three main exact string matching algorithm used in this program  
1. Knuth Morris Pratt (KMP) Algorithm: Exact string matching algorithm that compares from left to right, with the addition of the border function that counts the biggest prefix that exist at every character of the pattern being searched to save on redundant comparison
2. Boyer Moore Algorithm: Exact string matching algorithm that compares from right to left of the pattern, by preprocessing the final occurences of each character in the alphabet in the pattern, this algorithm saves on comparisons by always jumping to those last occurences when there is no match. This algorithm shines when the alphabet is rich i.e a lot of different unique characters are present
3. Aho Corasick Algorithm: Exact string matching using the help of the Trie structure to find several patterns in one search

While fuzzy matching only uses one, and is only a backup and used when the exact string matching does not bring any matches, the algorithm used in fuzzy search is
1. Levenshtein distance: dynamic programming approach on comparing the difference of two strings, in this program all operations (replacement, insertion, deletion) have the same weight, that is 1 for the calculation of the matrix for Levenshtein distance

## Program Requirements
1. Python  

## Program Setup
### Injecting SQL database
```bash
mysql -u root -p < data/tubes3_seeding.sql 
```

### Setting up .env
In the root directory of the project there is a file called ".envi". In that file, replace the password with your actual mysql password  
For example, your password is "sql', then in .envi, put:
```bash
DB_PASSWORD=sql
```  
After putting your mysql password, change the file name from ".envi" to ".env"

### Installing Python Libraries
```bash
python -m venv venv
source venv/bin/activate # or "source venv/Scripts/activate" on Windows
pip install -r requirements.txt
```

### Downloading Kaggle Dataset
```bash
python src/download_dataset.py 
```

## Running The Program
After setup of mysql, .env, and python libraries, run the following command to run the program
```bash
python src/main.py
```

## About The Creators
<table>
  <tr>
    <th>Nama Lengkap</th>
    <th>NIM</th>
    <th>Kelas</th>
  </tr>
  <tr>
    <td>Muh. Rusmin Nurwadin</td>
    <td>13523068</td>
    <th>K02</th>
  </tr>
  <tr>
    <td>Aryo Wisanggeni</td>
    <td>13523100</td>
    <th>K02</th>
  </tr>
  <tr>
    <td>Fityatul Haq Rosyidi</td>
    <td>13523116</td>
    <th>K02</th>
  </tr>
</table>
