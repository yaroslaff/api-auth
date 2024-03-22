
/* modal buttons */
const modal = document.getElementById('myModal');
const modal_p = document.getElementById('myModal-p')
const modal_btn = document.getElementById('myModal-btn')

function open_modal(msg, btn_classes = null, btn_title = null){
    modal_p.innerHTML = msg

    if(btn_classes){
        console.log("Append btn classes:", btn_classes)
        modal_btn.classList.add(...btn_classes)
    }

    if(btn_title){
        modal_btn.innerText = btn_title
    }

    modal.classList.add('is-active');
}

function reg_btn_onclick(){
    var username = document.getElementById('username').value
    var pass1 = document.getElementById('password').value
    var pass2 = document.getElementById('password2').value
    console.log(username)

    if(! username){
        open_modal("Username must not be empty");
        return
    }

    if(! pass1){
        open_modal("Password must not be empty");
        return
    }

    if(pass1 != pass2){
        open_modal("Password and verification do not match");
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
    .then(r => r.json() )
    .then(r => console.log(r))

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
 
}

init_page()