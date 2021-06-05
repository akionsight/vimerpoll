const add_poll_option = document.getElementById('add-poll-option')
const remove_poll_option = document.getElementById('remove-poll-option')
const poll_option_div = document.getElementById('poll-option-div')
const submit_button = document.getElementById('submit-button')
const poll_options = document.getElementsByClassName('poll-option')
const poll_question = document.getElementById('poll-question')
const main_area = document.getElementById('main')
const body = document.getElementById('body')
function create_popup (type, message) { 

  if (type === 'warning') {
    console.log('here')
    const nested_elementelement = document.createElement('div')
    element.setAttribute('class', 'alert alert-warning alert-text alert-dismissible')
    element.innerHTML = message
    body.insertBefore(element, main_area)
  } 

  if (type == 'success') {
    const element = document.createElement('div')
    element.setAttribute('class', 'alert alert-success alert-text alert-dismissible col-sm-4 col-sm-offset-3')
    element.innerHTML = message
  }

}

create_popup('warning', 'testing create popup')



add_poll_option.onclick = () => {
    const element = document.createElement('input')
    const poll_option_length = poll_options.length
    element.setAttribute('class', 'poll-option form-control')
    element.setAttribute('type', 'text')
    element.setAttribute('id', `poll-option-${poll_option_length + 1}`)
    poll_option_div.appendChild(element)
}

remove_poll_option.onclick = () => {
  console.log('remove poll option clicked')
  const poll_option_length = poll_options.length
  const element_to_remove = document.getElementById(`poll-option-${poll_option_length}`)
  element_to_remove.remove()
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
      console.log(response)
}


// alert alert-warning alert-text alert-dismissible