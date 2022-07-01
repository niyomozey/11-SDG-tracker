console.log('hello world');
const userRow = document.getElementById('roleRow')
const permissionRow = document.getElementById('permissionRow')
getData('roles');
getData('permissions');
function addRole(role) {
  const element = `
    <tr>
        <td>${role.id}</td>
        <td>${role.name}</td>
    </tr>
  `
  return element
}
function addPermission(permission) {
  const element = `
    <tr>
        <td>${permission.id}</td>
        <td>${permission.name}</td>
        <td>${permission.assignedId}</td>
    </tr>
  `
  return element
}
async function getData(entity) {

  let token;
  try {
    token = await axios.get('http://localhost:5000/userToken')
    if (token.data) {
      isAuthenticated(entity, token.data)
    }
  } catch (error) {
    // console.log(error.response.data)
    document.getElementById('roleContainer').innerHTML = '<h1 class="text-center">First Login</h1>'
  }
}
async function isAuthenticated(entity, token) {
  axios.get('http://localhost:3000/api/v1/' + entity, {
    headers: {
      authorization: `Bearer ${token}`
    }
  })
    .then(function (response) {
      console.log(response.data);
      var roles = "";
      response.data.data.forEach((item, i) => {
        roles += entity == "roles" ? addRole(item) : addPermission(item);
      });
      if (entity == "roles") {
        userRow.innerHTML = roles
      } else {
        permissionRow.innerHTML = roles
      }

    }).catch(function (error) {
      if (error.response) {
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      }
    });
}
