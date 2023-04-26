var express = require('express');
var app = express();
const bodyParser  = require('body-parser');
const axios = require('axios');

app.use(bodyParser.urlencoded());

app.set('view engine', 'ejs');

app.get('/', function(req, res) {
    axios.get(`https://jsonplaceholder.typicode.com/users`)
    .then((response)=>{
        var users = response.data;

         res.render('pages/login', {
             users: users
        });
    }); 
});

app.listen(8080);
console.log('8080 is the magic port');