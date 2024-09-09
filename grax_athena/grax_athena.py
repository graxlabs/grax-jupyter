import os
import pandas as pd
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
import pandas as pd

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
SCHEMA_NAME = os.getenv('ATHENA_DATABASE')
S3_STAGING_DIR = os.getenv('S3_STAGING_DIR')
AWS_REGION = os.getenv('AWS_REGION') 

conn_str = (
    "awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}@"
    "athena.{region_name}.amazonaws.com:443/"
    "{schema_name}?s3_staging_dir={s3_staging_dir}&work_group=primary"
)

def athena_connection():
    # Create the SQLAlchemy engine
  engine = create_engine(
      conn_str.format(
          aws_access_key_id=quote_plus(AWS_ACCESS_KEY),
          aws_secret_access_key=quote_plus(AWS_SECRET_KEY),
          region_name=AWS_REGION,
          schema_name=SCHEMA_NAME,
          s3_staging_dir=quote_plus(S3_STAGING_DIR),
      )
  )

  # Establish the connection
  conn = engine.connect()
  return conn

def pd_run_query(query):
  return pd.read_sql_query(query, athena_connection())