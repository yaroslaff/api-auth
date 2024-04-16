
/* modal buttons */
const modal = document.getElementById('myModal');
const modal_p = document.getElementById('myModal-p')
const modal_btn = document.getElementById('myModal-btn')

const settings = JSON.parse(sessionStorage.getItem("simpleAuthSettings"));



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
        modal_btn.classList.add(...btn_classes)
    }

    if(btn_title){
        modal_btn.innerText = btn_title
    }

    if(btn_onclick){
        modal_btn.onclick = btn_onclick;
        // console.log(modal_btn)
    }

    modal.classList.add('is-active');
}

function open_modal_close(msg){
    open_modal(msg, ['is-warning'], 'Close');
}

function open_modal_ok(msg, onclick = null){
    open_modal(msg, ['is-success'], 'OK', onclick);
}

const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };

function verify_btn_onclick(){

    var code = document.getElementById('code').value;

    const payload = {
        'code': code,
    }

    /* all checks passed */
    fetch(window.location.href, {
        method: "POST",    
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify(payload)
    })
    .then(async r => {
        switch(r.status){
            case 200:
                var result = await r.json();
                open_modal_ok("Login successful", function() { window.location.replace(result['url']); } );
                break;
            case 400:
                open_modal_close(await r.text());
                break;
            default:
                open_modal_close("System error (try reloading page): " + await r.text());
                break;
        }
    })
}

  function verify_send_btn_onclick(){
    alert("verify send again");
  }


  function login_btn_onclick(){
    var username_el = document.getElementById('username')
    var username = username_el.value
    var pass1 = document.getElementById('password').value
    
    var response;

    if(! username){
        open_modal_close("Username must not be empty");
        return
    }

    if(! pass1){
        open_modal_close("Password must not be empty");
        return
    }

    const user_el = document.getElementById('username')
    const pass_el = document.getElementById('password')

    const formData = new FormData();
    formData.append("username", user_el.value);
    formData.append("password", pass_el.value);


    const payload = {
        'username': username,
        'password': pass1
    }

    /* all checks passed */
    fetch('/auth/login', {
        method: "POST",    
        body: formData,
        // redirect: 'manual'
    })
    .then(async r => {
        console.log(r);

        switch(r.status){
            case 200:
                var result = await r.json();
                window.location.replace(result['url']);
                break;
            case 401:
                var result = await r.json();
                open_modal_close(result.detail);
                pass_el.value = "";
                break;
            default:
                open_modal_close("System error (try reloading page): " + await r.text());
                break;
        }
    })
    .catch(e => console.log("MYERROR", e))
}
  

function reg_btn_onclick(){
    const username_el = document.getElementById('username') 
    const username = username_el.value
    const pass1 = document.getElementById('password').value
    const pass2 = document.getElementById('password2').value

    var response;


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

    const payload = {
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
            if(r.status == 'OK'){
                console.log("redirect to", r.redirect);
                window.location = r.redirect;
            }else{
                console.log("status not OK:", r)
            }
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
    var reg_btn = document.getElementById('fastapi-simple-auth-register-btn');
    if(reg_btn) reg_btn.onclick = reg_btn_onclick;

    var login_btn = document.getElementById('fastapi-simple-auth-login-btn');
    if(login_btn) login_btn.onclick = login_btn_onclick;

    var verify_btn = document.getElementById('fastapi-simple-auth-verify-btn');
    if(verify_btn) verify_btn.onclick = verify_btn_onclick;

    var verify_send_btn = document.getElementById('fastapi-simple-auth-verify-send-btn');
    if(verify_send_btn) verify_send_btn.onclick = verify_send_btn_onclick;


}

init_page()