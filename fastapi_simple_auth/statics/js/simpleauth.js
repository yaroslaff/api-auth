
/* modal buttons */
const modal = document.getElementById('myModal');
const modal_p = document.getElementById('myModal-p')
const modal_btn = document.getElementById('myModal-btn')

var settings

function redirect_to_login(){
    window.location.replace("login");
}

function open_modal(msg, btn_classes = null, btn_title = null, btn_onclick=null){
    modal_p.innerHTML = msg

    /* clear classes */

    modal_btn.classList.remove('is-warning');
    modal_btn.classList.remove('is-danger');
    modal_btn.classList.remove('is-success');

    if(btn_classes){
        // modal_btn.classList.add(...btn_classes)
        modal_btn.classList.add(...btn_classes)
    }

    if(btn_title){
        modal_btn.innerText = btn_title
    }

    if(btn_onclick){
        modal_btn.onclick = btn_onclick;
        console.log(modal_btn)
    }

    modal.classList.add('is-active');
}

function open_modal_close(msg){
    open_modal(msg, btn_classes = ['is-warning'], btn_title = 'Close');
}

function open_modal_ok(msg, onclick = null){
    open_modal(msg, btn_classes = ['is-success'], btn_title = 'OK', btn_onclick=onclick);
}

const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };

function reg_btn_onclick(){
    var username_el = document.getElementById('username') 
    var username = username_el.value
    var pass1 = document.getElementById('password').value
    var pass2 = document.getElementById('password2').value

    var response;

    console.log(settings);

    if(! username){
        open_modal_close("Username must not be empty");
        return
    }

    if(username_el.classList.contains("email") && ! validateEmail(username)){
        open_modal_close("Username must be valid email");        
    }

    if(! pass1){
        open_modal_close("Password must not be empty");
        return
    }

    if(pass1 != pass2){
        open_modal_close("Password and verification do not match");
        return
    }

    payload = {
        'username': username,
        'password': pass1
    }

    /* all checks passed */
    fetch('/auth/users/', {
        method: "POST",    
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify(payload)
    })
    .then(r => {
        response = r.clone();
        return r.json();
    })
    .then(async r => {
        // console.log("FIN", r, response.status, response)
        if(response.status != 200){
            var text = await response.text() 
            open_modal_close(text)
        }else{
            open_modal_ok("Registered! Please login now. :-)", redirect_to_login)
        }
    })
    .catch(e => console.log("ERROR", e))

}

function init_page(){

    const closeModalButtons = document.querySelectorAll('.closeModal, .modal-background, .modal-close');

    closeModalButtons.forEach(button => {
        button.addEventListener('click', () => {
        modal.classList.remove('is-active');
        });
    });

    /* register button */
    reg_btn = document.getElementById('fastapi-simple-auth-register-btn');
    if(reg_btn) reg_btn.onclick = reg_btn_onclick;
 
    fetch('settings')
    .then(r => r.json())
    .then(r => settings = r)

}

init_page()