function putData() {
    var id = document.getElementById("put_id").value;
    var type = document.getElementById("put_type").value;
    var weight = document.getElementById("put_weight").value;
    var departure = document.getElementById("put_departure").value;
    var arrival = document.getElementById("put_arrival").value;
    var shipid = document.getElementById("put_ship").value;
  
    axios.all([axios.put('http://127.0.0.1:5000/api/cargo', {
        id: id,
        cargotype: type,
        weight: weight,
        departure: departure,
        arrival: arrival,
        shipid: shipid
      }), axios.get('http://127.0.0.1:5000/api/cargo')])
    .then(axios.spread((firstResponse, secondResponse) => {  
        var cargoData = secondResponse.data;
        var message = firstResponse.data;

        res.render('pages/cargo_api', {
            post_style: "none",
            put_style: "block",
            message: message,
            cargo: cargoData
        });
        console.log(put_weight);
        console.log(put_cargotype);
        console.log(put_shipid);
        console.log(message);
    })).catch(function(error) {
        res.render('pages/cargo_api', {
            post_style: "none",
            put_style: "block",
            message: "Try again!",
            cargo: cargoData
        });
    });
}  