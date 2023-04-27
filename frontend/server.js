var express = require('express');
var app = express();
const bodyParser  = require('body-parser');
const axios = require('axios');
app.use(bodyParser.urlencoded());
app.set('view engine', 'ejs');

// the command below changes views to look in the frontend folder
// typing in "node frontend/server.js" into the terminal will load the page
app.set('views', 'frontend/views');

app.get('/', function(req, res) {
    res.render("login", {});
});

app.post('/process_login', function(req, res){
    // get the username and password from the form.
    var user = req.body.username;
    var pass = req.body.password;
    // use a get method to use the login api, pass on credentials.
    axios.get('http://127.0.0.1:5000/authenticatedroute', {
        auth: {
          username: user,
          password: pass
        }
    // if successful, takes you to the next page and sends a success message to console.
    }).then(function(response) {
    res.render("test1")
    console.log('Authenticated');
    // if unsucessful, sends you back to the login page and sends a failure message to console.
  }).catch(function(error) {
    res.render("login")
    console.log('Error on Authentication');
  });
}); 
    
app.listen(8080);
console.log('8080 is the magic port');