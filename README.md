# The Verge Headline Scraper 📰
This is a Python script that scrapes headlines, URLs, authors, and dates of articles from theverge.com and saves them to a CSV file and SQLite database.
The script is designed to be run on a cloud service like AWS and can be set up with a cronjob to run daily.

## Working EC2 AWS URL:⭐
http://ec2-3-15-146-152.us-east-2.compute.amazonaws.com/

## Setup
```bash
git clone https://github.com/santhoshsivanva/theverge-headline-scraper.git
cd theverge
pip install -r requirements.txt
python3 run.py
```

## Output
The script will generate a CSV file titled ddmmyyy_verge.csv with the following headers: id, URL, headline, author, and date. The script will also create an SQLite database and store the same data in a table with the same column names. The id column is set as the primary key to ensure that there are no duplicate entries.

## Automation ⭐
To automate the script to run daily, set up a cronjob in the server with the following command:

```bash
0 0 * * * TZ=Asia/Kolkata /usr/bin/python3 /home/ubuntu/theverge/run.py
```
##Requirements:
Chrome Web Driver with supportive chrome browser version
(Download here) https://chromedriver.chromium.org/downloads
Python 3.7 or higher
scrapy
selenium
SQLite 3

This will run the script at midnight every day.

## License
This project is licensed under the MIT License.
