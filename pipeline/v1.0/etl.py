import csv
import configparser
import logging
from builtins import range

from carto.auth import APIKeyAuthClient
from carto.sql import SQLClient
from carto.sql import BatchSQLClient


logger = logging.getLogger('carto-etl')

config = configparser.RawConfigParser()
config.read("etl.conf")

CARTO_BASE_URL = config.get('carto', 'base_url')
CARTO_API_KEY = config.get('carto', 'api_key')
CARTO_TABLE_NAME = config.get('carto', 'table_name')
CARTO_COLUMNS = config.get('carto', 'columns')
CHUNK_SIZE = int(config.get('etl', 'chunk_size'))
MAX_ATTEMPTS = int(config.get('etl', 'max_attempts'))

api_auth = APIKeyAuthClient(base_url=CARTO_BASE_URL, api_key=CARTO_API_KEY, organization='nyu')
sql = SQLClient(api_auth)
bsql = BatchSQLClient(api_auth)

def ClearContent(table):
    sql.send("TRUNCATE TABLE " + table)


def chunks(full_list, chunk_size, start_chunk=1, end_chunk=None):
    finished = False
    while finished is False:
        chunk = []
        for chunk_num in range(chunk_size):
            if chunk_num < (start_chunk - 1):
                continue

            if end_chunk is not None and chunk_num >= end_chunk:
                return

            try:
                chunk.append(next(full_list))
            except StopIteration:
                finished = True
                if len(chunk) > 0:
                    continue
                else:
                    return
        yield chunk


class UploadJob(object):
    def __init__(self, csv_file_path, table, x_column="longitude", y_column="latitude", srid=4326):
        self.csv_file_path = csv_file_path
        self.x_column = x_column
        self.y_column = y_column
        self.srid = srid
        self.table = table

    def run(self):
        raise NotImplemented

    def regenerate_overviews(self):
        query = 'select CDB_CreateOverviews(\'{table}\'::regclass)'.format(table=table)
        job_result = bsql.create(query)
        return job_result['job_id']

    def check_job(self, job_id):
        return bsql.read(job_id)


class InsertJob(UploadJob):
    def __init__(self, csv_file_path,  table, x_column="longitude", y_column="latitude", srid=4326):
        self.csv_file_path = csv_file_path
        #self.x_column = x_column
        #self.y_column = y_column
        self.srid = srid
        self.table = table
    def run(self, start_chunk=1, end_chunk=None):
        with open(self.csv_file_path) as f:
            a=''
            csv_reader = csv.DictReader(f)
            for chunk_num, record_chunk in enumerate(chunks(csv_reader, CHUNK_SIZE, start_chunk, end_chunk)):
                query = "insert into {table_name} (the_geom,{columns}) values".format(table_name=self.table, columns=CARTO_COLUMNS.lower())
                for record in record_chunk:
                    # query += " (st_transform(st_setsrid(st_makepoint({longitude}, {latitude}), {srid}), 4326),".format(longitude=record[self.x_column], latitude=record[self.y_column], srid=self.srid)
                    query += " (st_transform(st_setsrid(st_geomfromtext('{geometry}'),{srid}), 4326),".format(geometry=record['geometry'], srid=self.srid) 
                    for column in CARTO_COLUMNS.split(","):
                        try:
                            float(record[column])
                        except ValueError:
                            query += "'{value}',".format(value=record[column])
                        else:
                            query += "{value},".format(value=record[column])
                    query = query[:-1] + "),"
                query = query[:-1]
                #query = query.replace("'", "''")
                logger.debug("Chunk #{chunk_num}: {query}".format(chunk_num=(chunk_num + 1), query=query))
                for retry in range(MAX_ATTEMPTS):
                    try:
                        sql.send(query)
                        a = a + 'send'
                    except Exception as e:
                        logger.warning("Chunk #{chunk_num}: Retrying ({error_msg})".format(chunk_num=(chunk_num + 1), error_msg=e))
                        a=a+'error'
                    else:
                        logger.info("Chunk #{chunk_num}: Success!".format(chunk_num=(chunk_num + 1)))
                        a=a+'end'
                        break
                else:
                    logger.error("Chunk #{chunk_num}: Failed!)".format(chunk_num=(chunk_num + 1)))
                    a=a+'fail'
                return query[:20] + a + query[-10:]
