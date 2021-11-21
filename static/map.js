//#region Map initialization and rendering
const mymap = L.map('map').setView([0, 0], 1);
const attribution =//don't forget to give the attribution
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const tileUrl = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png';
const tiles = L.tileLayer(tileUrl, { attribution });
tiles.addTo(mymap);

//#endregion

//#region Search function
function onSearch(){
    
    //`https://nominatim.openstreetmap.org/search?q=kolkata&format=json`
    var query=document.getElementById("searchbar").value
    fetch(`https://nominatim.openstreetmap.org/search?q=${query}&format=json`)
    .then(response=>response.json())
    .then(data=>{
        console.log(data)
        var marker = L.marker([data[0].lat,data[0].lon]).addTo(mymap);
        marker.bindPopup(` ${data[0].display_name}`).openPopup();

        //reversing to get the state and country name
        //Oh god please forgive me
        fetch(`https://nominatim.openstreetmap.org/reverse?lat=${data[0].lat}&lon=${data[0].lon}&format=json`)
    .then(response=>response.json())
    .then(data=>{
       document.getElementById("searchbar").value=`${data.address.state?data.address.state:'Unknown'},${data.address.country?data.address.country:'Unknown'}`
    })

    })
}
//#endregion

//#region Markers on mouse Click
function onMouseClick(e){
    var marker = L.marker(e.latlng).addTo(mymap);

    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${e.latlng.lat}&lon=${e.latlng.lng}&format=json`)
    .then(response=>response.json())
    .then(data=>{
        console.log(data)
          marker.bindPopup(`Country: ${data.address.country}<br>City: ${data.address.city?data.address.city:'Unknown'}`).openPopup();
          document.getElementById("searchbar").value=`${data.address.state?data.address.state:'Unknown'},${data.address.country?data.address.country:'Unknown'}`
    })
    .catch(err=>{
        marker.bindPopup(`Unable to geocode!`).openPopup();
    }
 )

    
}
mymap.on('click',onMouseClick)
//#endregion