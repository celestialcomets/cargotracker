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
    axios.get(`https://jsonplaceholder.typicode.com/users`)
    .then((response)=>{
        var users = response.data;

         res.render('login', {
             users: users
        });
    }); 
});

app.listen(8080);
console.log('8080 is the magic port');