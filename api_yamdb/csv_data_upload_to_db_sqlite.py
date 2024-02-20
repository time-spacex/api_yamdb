import sqlite3
import csv
import os
import logging
from logging import DEBUG
from logging import StreamHandler
from logging import Formatter
from _sqlite3 import Error
import re

# the script uploads all csv files from static/data dir to sqlite3 db tables
# preliminary be sure the tables exist in db.sqlite3

log = logging.getLogger(__name__)
log.setLevel(DEBUG)
stream_handler = StreamHandler()
formatter = Formatter('%(asctime)s [%(levelname)s] %(funcName)s %(lineno)d %(message)s')
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)


base_path = f'{os.path.curdir}/static/data'

con = sqlite3.connect("db.sqlite3")

upload_err = False
potentially_failed_row = None

for dir in os.listdir(base_path):
    list_files = os.listdir(f'{base_path}/{dir}')
    for file in list_files:
        log.debug(f'Reading csv file {file} from dir {dir}')

        data_to_upload = []
        try:
            with (open(f'{base_path}/{dir}/{file}', mode='r',
                       encoding='utf-8') as csvfile):
                rows = csv.reader(csvfile,
                                  delimiter=',',
                                  lineterminator='\n')
                for row in rows:
                    data_to_upload.append(row)

            if data_to_upload:
                table_name = f'{dir}_{file[:-4]}'
                log.debug(f'Uploading to table {table_name}')
                log.debug(f'Example row: {data_to_upload[1]}')

                row = con.execute('SELECT * FROM sqlite_schema '
                                  f'WHERE tbl_name="{table_name}"')
                schema = row.fetchone()[4]
                log.debug(f'{schema=}')
                re_schema = re.compile(r'CREATE TABLE "' + table_name +
                           r'" \((?P<statement>.*)\)')
                res = re_schema.match(schema).group('statement')
                unparsed_cols = res.split(', ')
                re_col = re.compile(r'^"(?P<col>[\S]*)".+')
                table_cols = []
                for unparsed_col in unparsed_cols:
                    col_match = re_col.match(unparsed_col)
                    if col_match:
                        table_cols.append(col_match.group('col'))
                table_cols = set(table_cols)
                log.debug(f'{table_cols=}')

                csv_cols = data_to_upload[0]
                log.debug(f'{csv_cols=}')

                question_marks = ['?' for _ in range(len(table_cols))]

                for row in data_to_upload[1:]:
                    row_res = []
                    for table_col in table_cols:
                        if table_col in csv_cols:
                            index = csv_cols.index(table_col)
                            row_res.append(row[index])
                        else:
                            row_res.append('')
                    potentially_failed_row = row_res
                    con.execute(f"INSERT INTO {table_name} "
                                f"VALUES({','.join(question_marks)})", row_res)
        except Exception as ex:
            log.error(ex)
            if potentially_failed_row:
                log.error(f'Failed to execute insert for row '
                          f'{potentially_failed_row}')
            upload_err = True

if (upload_err):
    con.rollback()
    log.debug('Upload failed. No one table was uploaded')
else:
    log.debug('Upload success')
    con.commit()

con.close()
