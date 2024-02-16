import sqlite3
import csv
import os

# the script uploads all csv files from static/data dir to sqlite3 db tables
# preliminary be sure the tables exist in db.sqlite3

base_path = f'{os.path.curdir}/static/data'
list_files = os.listdir(base_path)

print(f'Reading csv files {", ".join(list_files)}')

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

for file in list_files:

    data_to_upload = []

    if file in ['title.csv', 'title_genre.csv',
                'category.csv', 'genre.csv']: #todo remove it
        with open(f'{base_path}/{file}', mode='r') as csvfile:
             rows = csv.reader(csvfile, delimiter=',')
             for row in rows:
                 data_to_upload.append(row)

    if data_to_upload:
        question_marks = []
        for i in range(len(data_to_upload[0])):
            question_marks.append('?')
        table_name = file[:-4]
        if 'user' in table_name:
            table_name = f'users_{table_name}'
        else:
            table_name = f'reviews_{table_name}'
        print(f'Uploading to table {table_name}')
        print(f'Example row: {data_to_upload[1]}')
        try:
            cur.executemany(
                f"INSERT INTO {table_name} "
                f"VALUES({','.join(question_marks)})", data_to_upload[1:])
        except sqlite3.OperationalError as ex:
            print(ex)
            for row in data_to_upload[1:]:
                print(row)
        con.commit()
