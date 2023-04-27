var express = require('express');
var app = express();
const bodyParser  = require('body-parser');
const axios = require('axios');
app.use(bodyParser.urlencoded());
app.set('view engine', 'ejs');

// the command below changes views to look in the frontend folder
// typing in "node frontend/server.js" into the terminal will load the page
app.set('views', 'frontend/views');

// default page leads you to login
app.get('/', function(req, res) {
    res.render("pages/login", {});
});

// if page is reloaded with a get request, loads the login page again
app.get('/process_login', function(req, res) {
    res.render("pages/login", {});
});

// if submit button is hit, starts the authentification process
app.post('/process_login', function(req, res){
    // get the username and password from the form.
    var user = req.body.username;
    var pass = req.body.password;

    // send username and password to login api for authentification 
    // and collect cargo data from cargo get api at the same time.
    axios.all([axios.get('http://127.0.0.1:5000/authenticatedroute', {
        auth: {
          username: user,
          password: pass
        }
    }),
    axios.get('http://127.0.0.1:5000/api/cargo')])
    .then(axios.spread((firstResponse, secondResponse) => {  
        // secondResponse returns the cargo data.
        var cargoData = secondResponse.data;
        
        // if login was successful, loads cargo page with data from cargo get api
        // and sends success message to console.
        res.render('pages/cargo', {
            cargo: cargoData,
        });
        console.log('Authenticated');
        // if login was unsucessful, loads the login page again
        // and sends failure message to console.
        })).catch(function(error) {
            res.render("pages/login")
            console.log('Error on Authentication');
        });
    });
    
app.listen(8080);
console.log('8080 is the magic port');