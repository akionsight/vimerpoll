from fastapi import FastAPI, status, Response
import database_manager
import models
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title='Vimerpoll')

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print('app starting up')
    await database_manager.database.connect()


@app.on_event("shutdown")
async def shutdown():
    print('app shutting down')
    await database_manager.database.disconnect()


@app.post('/create-poll/', status_code=status.HTTP_201_CREATED)
async def create_poll(poll_object: models.Poll):
    result_object = {}
    for option in poll_object.poll_options:
        result_object[option] = 0
    record_id = await database_manager.create_poll(poll_object, result_object)
    return {"id": record_id, **poll_object.dict()}


@app.get('/get-poll/{poll_id}')
async def get_poll(poll_id: int, response: Response):
    """
    Get all the info of poll with its poll_id

    HTTP Status code 404 raised when the poll with the poll_id was not found on this server
    """

    query_results = await database_manager.fetch_poll_data(poll_id=poll_id)
    if not query_results == None:
        dict(query_results).pop('poll_results')
        return query_results
    else:
        response.status_code == status.HTTP_404_NOT_FOUND
        return {
            "message": "no poll with this poll id was found on the server"
        }


@app.get('/poll-result/{poll_id}')
async def get_poll_res(poll_id: int, response: Response):
    """
    Get the results of any given poll with its poll_id

    HTTP status code 404 raised when the poll_id was not found on the server 
    """
    query_results = await database_manager.fetch_poll_results(poll_id)
    if not query_results == None:
        query_results = dict(query_results)
        return query_results
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "no poll with this poll id was found on the server"
        }


@app.patch('/vote/{poll_id}/{option_id}')
async def vote_for_poll(poll_id: int, option_id: int, response: Response):
    """
    Vote for a poll

    HTTP Status Code 200 is raised when the vote is successful

    HTTP Status Code 400 if the request is malformed
    """
    query_results = await database_manager.fetch_poll_results(poll_id=poll_id)
    for count, key in enumerate(query_results):
        print(count, key)
        if count == option_id:
            query_results[key] += 1
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 
                "message": "Sorry, this option does not exist"
            }
    print(query_results)
    return query_results


# the way it works is that for the number of options, one thing gets created in the json key and stored
