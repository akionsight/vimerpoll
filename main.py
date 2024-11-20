from fastapi import FastAPI, Request
from typing import Dict, Any
import database_manager
from starlette.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import ast


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index():
    return FileResponse("static/index.html")


@app.post("/create-poll/")
def put_data(data: Dict[Any, Any]):
    print(data)
    uid = database_manager.make_new_poll(data)
    return uid

@app.post('/cast-vote/{id}')
def put_vote(data: Dict[Any, Any], id: str):
    print(data, id)
    print('here')
    database_manager.cast(id, data['pos'])

@app.get("/results/{id}")
def return_results(id: str):
    return database_manager.ret_results(id)

@app.get("/vote/{id}")
def vote_page(request: Request, id: str):
  print(id)
  data = database_manager.poll_data(id)

  final = ""

  rael_data = ast.literal_eval(data[1])

  for topping in rael_data:

      opt = f", {{option: '{topping}' }}"

      final += opt

  final_fr = final[1:]

  page = f"""


<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/static/style.css">
    <script src="/static/main.js" defer></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">

    <title>VimerPoll</title>
    <link rel="shortcut icon" href="/static/vimerpoll.svg" type="image/x-icon">
  </head>
  <body class="bg-dark text-light">
    <div id="main" class="container mt-5">
      
      <h1 class="text-center">VimerPoll</h1>
      <p class="text-center">Vote on your favorite option below:</p>

      <div id="poll-container" class="mt-4">
        <!-- Poll options will be dynamically loaded here -->
      </div>

    </div>

    <script>
      // Array to store poll options and votescc
      const pollData = [{final_fr}];

      // Function to display poll options
      function displayPoll() {{
        const pollContainer = document.getElementById('poll-container');
        pollContainer.innerHTML = '';
        pollData.forEach((item, index) => {{
          const optionDiv = document.createElement('div');
          optionDiv.className = 'd-flex align-items-center justify-content-between border p-2 mb-2';

          const optionLabel = document.createElement('span');
          optionLabel.textContent = `${{item.option}}`;
          optionDiv.appendChild(optionLabel);

          const voteButton = document.createElement('button');
          voteButton.textContent = 'Vote';
          voteButton.className = 'btn btn-primary';
          voteButton.onclick = () => castVote(index);
          optionDiv.appendChild(voteButton);

          pollContainer.appendChild(optionDiv);
        }});
      }}

      // Function to cast a vote
      function castVote(index) {{
        console.log(pollData[index]);
        console.log(index);
        fetch('http://127.0.0.1:8000/cast-vote/{id}', {{
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'omit', // include, *same-origin, omit
        headers: {{
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        }},
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify({{pos: index}}) // body data type must match "Content-Type" header
      }}).then(response => {{
      
        localStorage.setItem('mostRecentPoll', '{id}'); 
        
        window.location.href = '/static/thanks.html'

      }});
        displayPoll();

      }}

      // Function to add a new option
      function addOption() {{
        const newOption = prompt('Enter the new option:');
        if (newOption) {{
          pollData.push({{ option: newOption, votes: 0 }});
          displayPoll();
        }}
      }}

      // Initialize the poll on page load
      window.onload = displayPoll;
    </script>
  </body>
</html>

"""
  return HTMLResponse(page)
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
