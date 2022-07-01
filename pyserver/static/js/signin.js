const url = 'http://localhost:3000/api/v1'
document.querySelector("#send").addEventListener("click", function () {
    const email = document.querySelector("#email").value
    const password = document.querySelector("#password").value
    // location.href = './dashboard.html';

fetch(url+'/auth/login',{
    method: 'POST',
    body: JSON.stringify({
        email:email,
        password: password
    }),
    headers:{
        'content-type': 'application/json;charset=utf-8'
    }

}).then(res => res.json())
.then(data => {
    console.log(data)
    console.log(typeof(data))
    console.log(data.hasOwnProperty("user","token"))
    if(data.hasOwnProperty("user","token")){
        location.href = '/loginController';
    }else{
        var err = document.getElementById('error')
        err.innerHTML = 'Incorrect username or password' 
        err.style.color = 'red'          
    }
    // if(data.message){  
    //     var err = document.getElementById('error')
    //     err.innerHTML = 'Incorrect username or password' 
    //     err.style.color = 'red'     
    // }else{
    //     var err = document.getElementById('error')
    //     err.innerHTML = '' 
    //     location.href = '/loginController';
    // }
    
})
})