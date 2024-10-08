import os
import pandas as pd
import os
from urllib.parse import quote_plus, urlparse, parse_qs, unquote
from sqlalchemy import create_engine
import pandas as pd
from pyathena import connect

if os.getenv('GRAX_DATALAKE_URL'):
  connection_string = os.getenv('GRAX_DATALAKE_URL')
  parsed = urlparse(connection_string)
  query_params = parse_qs(parsed.query)

  AWS_ACCESS_KEY = unquote(parsed.username)
  AWS_SECRET_KEY = unquote(parsed.password)
  SCHEMA_NAME = unquote(parsed.path[1:])
  AWS_REGION = parsed.hostname.split('.')[1]
  AWS_WORKGROUP = unquote(query_params['work_group'][0])
  S3_STAGING_DIR = unquote(query_params['s3_staging_dir'][0])

else:
  AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
  AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
  SCHEMA_NAME = os.getenv('ATHENA_DATABASE')
  AWS_REGION = os.getenv('AWS_REGION') 
  AWS_WORKGROUP = os.getenv('AWS_WORKGROUP', 'primary')
  S3_STAGING_DIR = os.getenv('S3_STAGING_DIR')

  conn_str = (
      "awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}@"
      "athena.{region_name}.amazonaws.com:443/"
      "{schema_name}?s3_staging_dir={s3_staging_dir}&work_group={work_group}"
  )

  connection_string = conn_str.format(
      aws_access_key_id=quote_plus(AWS_ACCESS_KEY),
      aws_secret_access_key=quote_plus(AWS_SECRET_KEY),
      region_name=AWS_REGION,
      schema_name=SCHEMA_NAME,
      work_group=AWS_WORKGROUP,
      s3_staging_dir=quote_plus(S3_STAGING_DIR),
  )

def sql_connection():
    # Create the SQLAlchemy engine
  engine = create_engine(connection_string)

  # Establish the connection
  conn = engine.connect()
  return conn

def pyathena_connection():
    return connect(aws_access_key_id=AWS_ACCESS_KEY,
                   aws_secret_access_key=AWS_SECRET_KEY,
                   s3_staging_dir=S3_STAGING_DIR,
                   schema_name=SCHEMA_NAME,
                   region_name=AWS_REGION,
                   work_group=AWS_WORKGROUP)

# resuse the connection
SQL_CONNECTION = sql_connection()
def query_pd(query):
  return pd.read_sql_query(query, SQL_CONNECTION)

def query(query):
  cursor = pyathena_connection().cursor()
  cursor.execute(query)
  return cursor