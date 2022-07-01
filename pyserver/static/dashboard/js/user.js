console.log('hello world');
const userRow = document.getElementById('userRow')
getData();
function appendElement(user){
  const element = `<tr>
      <td><input class="form-check-input" type="checkbox"></td>
      <td>${user.firstName}</td>
      <td>${user.lastName}</td>
      <td>${user.email}</td>
      <td>${user.phoneNo}</td>
      <td><input style="border:none;background:transparent;" id="roleId${user.id}" value="${user.roleId}" readonly></td>
      <td>
          <a class="btn btn-sm btn-primary" id="edit${user.id}" onclick="edit(${user.id})" >Edit</a>
          <a class="btn btn-sm btn-danger" id="delete${user.id}" onclick="del(${user.id})">Delete</a>
      </td>
  </tr>
  `
  return element
}
async function getData() {

  let token;
  try {
    token = await axios.get('http://localhost:5000/userToken')
    if (token.data) {
      isAuthenticated(token.data)
    }
  } catch (error) {
    // console.log(error.response.data)
    document.getElementById('userContainer').innerHTML = '<h1 class="text-center">First Login</h1>'
  }
}
async function isAuthenticated(token){
  axios.get('http://localhost:3000/api/v1/users',{
    headers:{
      authorization : `Bearer ${token}`
    }
  })
  .then(function (response) {
    console.log(response.data);
    var users='';
    response.data.forEach((item, i) => {
      console.log(item);
      users += appendElement(item)
    });
    userRow.innerHTML = users
  }).catch(function (error) {
    if (error.response) {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
    }
    });
}
var editButton ={ name: '',status:'off'}
function edit(id){
  console.log('hello world'+id)
  var roleInput = document.getElementById('roleId'+id)
  
  if(editButton.status == 'off'){
    document.getElementById('edit'+id).innerHTML = 'Save'
    roleInput.removeAttribute('readonly')
    roleInput.style.border = 'solid 1px black'
    editButton.name = 'edit'+id 
    editButton.status = 'on'
  }else{
    var roleId = roleInput.value
    console.log('Server dies'+roleId)
    axios.put('http://localhost:3000/api/v1/users/'+id, {
      roleId: roleId
    })
    .then(function (response) {
      editButton.status = 'off'
      location.href = ''
    })
    .catch(function (error) {
      console.log(error);
    });
  }
}

function del(id){
  if(id != 1){
    axios.delete('http://localhost:3000/api/v1/users/'+id,)
    .then(function (response) {
      location.href = ''
    })
    .catch(function (error) {
      console.log(error);
    });
  }else{
    console.log('u can\'t delete an administrator')
    location.href = ''
  }
  
}