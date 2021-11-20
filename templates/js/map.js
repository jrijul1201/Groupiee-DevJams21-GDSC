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
    })
}
//#endregion

//#region Markers on mouse Click
function onMouseClick(e){
    var marker = L.marker(e.latlng).addTo(mymap);

    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${e.latlng.lat}&lon=${e.latlng.lng}&format=json`)
    .then(response=>response.json())
    .then(data=>{
        marker.bindPopup(`Country: ${data.address.country}<br>City: ${data.address.city?data.address.city:'Unknown'}`).openPopup();
    })

    
}
mymap.on('click',onMouseClick)
//#endregion