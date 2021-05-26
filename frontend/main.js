const add_poll_option = document.getElementById('add-poll-option')
const poll_option_div = document.getElementById('poll-option-div')
const submit_button = document.getElementById('submit-button')
const poll_options = document.getElementsByClassName('poll-option')
const poll_question = document.getElementById('poll-question')


add_poll_option.onclick = () => {
    const element = document.createElement('input')
    element.setAttribute('class', 'poll-option form-control')
    element.setAttribute('type', 'text')
    poll_option_div.appendChild(element)
}

submit_button.onclick = async function () {
    let options = []
    for (i=0; i<poll_options.length; i++) {
        options.push(poll_options.item(i).value)
    }
    console.log(options)
    const data = {
            "poll_question": poll_question.value,
            "poll_options": options
    }
    const response = await fetch('http://127.0.0.1:8000/create-poll/', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'omit', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      });
}