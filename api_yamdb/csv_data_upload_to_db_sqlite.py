import sqlite3
import csv
import os
import logging
from logging import DEBUG
from logging import StreamHandler
from logging import Formatter
import re

# the script uploads all csv files from static/data dir to sqlite3 db tables
# preliminary be sure the tables exist in db.sqlite3

log = logging.getLogger(__name__)
log.setLevel(DEBUG)
stream_handler = StreamHandler()
formatter = Formatter('%(asctime)s [%(levelname)s] %(funcName)s '
                      '%(lineno)d %(message)s')
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)


base_path = f'{os.path.curdir}/static/data'

con = sqlite3.connect("db.sqlite3")

upload_err = False


def get_value(col_type: str, str_val: str):
    if col_type == 'integer':
        return int(str_val)
    elif col_type == 'bool':
        if str_val.lower() == '1':
            return True
        else:
            return False
    else:
        return str_val


def get_def_value(col_type: str):
    if col_type == 'integer':
        return 0
    elif col_type == 'bool':
        return False
    else:
        return ''


def upload_to_table(data_to_upload: list,
                    table_col_types: dict,
                    csv_cols: list,
                    table_name: str,
                    question_marks: str):
    for row in data_to_upload[1:]:
        row_res = []

        for table_col, col_type in table_col_types.items():
            if table_col in csv_cols:
                index = csv_cols.index(table_col)
                row_res.append(get_value(col_type, row[index]))
            else:
                row_res.append(get_def_value(col_type))
        con.execute(f"INSERT INTO {table_name} "
                    f"VALUES({question_marks})", row_res)


for dir in sorted(os.listdir(base_path)):
    for file in sorted(os.listdir(f'{base_path}/{dir}')):
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
                # range to cut .csv and numbers
                table_name = f'{dir[2:]}_{file[2:-4]}'
                log.debug(f'Uploading to table {table_name}')
                log.debug(f'Example row: {data_to_upload[1]}')

                # parsing table columns and column types
                row = con.execute('SELECT * FROM sqlite_schema '
                                  f'WHERE tbl_name="{table_name}"')
                schema = row.fetchone()[4]
                log.debug(f'{schema=}')
                re_schema = re.compile(r'CREATE TABLE "' + table_name
                                       + r'" \((?P<statement>.*)\)')
                res = re_schema.match(schema).group('statement')
                unparsed_cols = res.split(', ')
                re_col_type = re.compile(r'^"(?P<col>[\S]*)" '
                                         r'(?P<col_type>[a-z_]*).+')
                table_col_types = {}
                for unparsed_col in unparsed_cols:
                    col_type_match = re_col_type.match(unparsed_col)
                    if col_type_match:
                        table_col_types[col_type_match.group('col')] = (
                            col_type_match.group('col_type'))
                log.debug(f'{table_col_types=}')

                csv_cols = data_to_upload[0]
                log.debug(f'{csv_cols=}')

                question_marks = ['?' for _ in range(len(table_col_types))]

                upload_to_table(data_to_upload,
                                table_col_types,
                                csv_cols,
                                table_name,
                                ','.join(question_marks))
        except Exception as ex:
            log.error(ex)
            upload_err = True

if (upload_err):
    con.rollback()
    log.debug('Upload failed. No one table was uploaded')
else:
    log.debug('Upload success')
    con.commit()

con.close()
