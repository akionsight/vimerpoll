#  this file manages the sqlalchemy ORM code

import sqlalchemy
import databases
from sqlalchemy import update
from sqlalchemy.sql.sqltypes import String


DATABASE_URL = "postgresql://postgres:harshp14789@localhost/vimerpoll"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


poll = sqlalchemy.Table(
    "polls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger() , primary_key=True, autoincrement=True),
    sqlalchemy.Column("poll_question", sqlalchemy.String),
    sqlalchemy.Column("poll_options", sqlalchemy.dialects.postgresql.ARRAY(String)),
    sqlalchemy.Column('poll_results', sqlalchemy.JSON()),
    sqlalchemy.Column("creation_timestamp", sqlalchemy.DateTime(), server_default=sqlalchemy.func.clock_timestamp())
)


engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

async def fetch_poll_data(poll_id):
    query = poll.select().where(poll.c.id == poll_id)
    query_results = await database.fetch_one(query)
    return query_results


async def fetch_poll_results(poll_id):
    poll_data = await fetch_poll_data(poll_id)
    return dict(poll_data['poll_results'])

async def create_poll(poll_object, result_object):
    query = poll.insert().values(poll_question=poll_object.poll_question,
                                                  poll_options=poll_object.poll_options, poll_results=result_object)
    record_id = await database.execute(query)
    return record_id
    
    

async def vote_for_poll(updated_poll_results, poll_id):
    update_query = update(poll).where(
    poll.c.id == poll_id).values(poll_results=updated_poll_results)
    await database.execute(update_query)