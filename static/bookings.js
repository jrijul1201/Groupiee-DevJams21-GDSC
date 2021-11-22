//For the drop downs
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems, {});
});

//for listing the flights
const mappings=["NYC","MOW","CCU","DEL","BOM","MAA"]
const class_mappings=["ECO","PEC","BUS"]
function Search(){

  var depart_city=mappings[document.getElementById("departure").value]
  var arriv_city=mappings[document.getElementById("arrival").value]
  var depart_date=document.getElementById("depart_date").value
 var travellers=document.getElementById("travellers").value
 var cabin_class=class_mappings [document.getElementById("cabin_class").value]

  fetch(`https://priceline-com-provider.p.rapidapi.com/v1/flights/search?location_departure=${depart_city}&itinerary_type=ONE_WAY&sort_order=PRICE&class_type=${cabin_class}&date_departure=${depart_date}&location_arrival=${arriv_city}&number_of_passengers=${travellers}&number_of_stops=1&price_min=100&price_max=20000&duration_max=2051`, {
	"method": "GET",
	"headers": {
		"x-rapidapi-host": "priceline-com-provider.p.rapidapi.com",
		"x-rapidapi-key": "RAPID API KEY"
	}
})
.then(response => 
	response.json()
).then(data=>{
  console.log(data)
  var airline=data.airline
  document.getElementById('airlines').innerHTML=""
  for(var i=0;i<airline.length;i++){
    var airline_card=` <div class="card">
    <div class="card-content">
        <div class="card-title">
            <div class="row">
                <div class="col m3">
                   ${airline[i].name}
                </div>
                <div class="col m3">
                    <i class="medium material-icons">flight_takeoff</i><br>
                    unavailable
                </div>
                <div class="col m3">
                    <i class="medium material-icons">flight_land</i><br>
                    unavailable
                </div>
                <div class="col m3">
                <button
                class="btn-large waves-effect waves-dark red" type="submit"><a class="white-text" href="https://${airline[i].websiteUrl}" target="_blank">Check out!</a></button>
                
                </div>
            </div>
            
        </div>
        
        </div>
</div>`
    document.getElementById('airlines').innerHTML+=airline_card
  }
})
.catch(err => {
	console.error(err);
});


}

