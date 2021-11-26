// fetch("https://weatherapi-com.p.rapidapi.com/astronomy.json?q=Chattanooga", {
// 	"method": "GET",
// 	"headers": {
// 		"x-rapidapi-host": "weatherapi-com.p.rapidapi.com",
// 		"x-rapidapi-key": "9cb1c64a74mshe483b1ba55588eep1ea8d5jsn22992105906a"
// 	}
// })
// .then(response => response.json()
// .then(json => {
//     console.log(json)
//     $("#sunrise").text("Sunrise: " + json.astronomy.astro.sunrise);
//     $("#sunset").text("Sunset: " + json.astronomy.astro.sunset);
//     $("#moonrise").text("Moonrise: " + json.astronomy.astro.moonrise);
//     $("#moonset").text("Moonset: " + json.astronomy.astro.moonset);
//     $("#phase").text("Moon Phase: " + json.astronomy.astro.moon_phase);
//     $("#illumination").text("Illumination: " + json.astronomy.astro.moon_illumination + "%");
// }))
// .catch(err => {
// 	console.error(err);
// });



// fetch("https://weatherapi-com.p.rapidapi.com/current.json?q=Chattanooga", {
// 	"method": "GET",
// 	"headers": {
// 		"x-rapidapi-host": "weatherapi-com.p.rapidapi.com",
// 		"x-rapidapi-key": "9cb1c64a74mshe483b1ba55588eep1ea8d5jsn22992105906a"
// 	}
// })
// .then(response => response.json()
// .then(json => {
//     console.log(json)
// }))
// .catch(err => {
// 	console.error(err);
// });



fetch("https://weatherapi-com.p.rapidapi.com/forecast.json?q=Chattanooga&days=2", {
	"method": "GET",
	"headers": {
		"x-rapidapi-host": "weatherapi-com.p.rapidapi.com",
		"x-rapidapi-key": "9cb1c64a74mshe483b1ba55588eep1ea8d5jsn22992105906a"
	}
})
.then(response => response.json()
.then(json => {
    console.log(json)

    // Pull out individual days from JSON return
    const today = json.forecast.forecastday[0];
    const nextDay = json.forecast.forecastday[1];

    // Destrucutre variables from JSON
    const { sunrise, sunset, moonrise, moonset, moon_phase, moon_illumination} = today.astro;
    const { sunrise: nextSunrise } = nextDay.astro;

    const rise = parseInt(nextSunrise[0] + nextSunrise[1]);
    const set = parseInt(sunset[0] + sunset[1]) + 12;
    // const night = set - rise;

    console.log(rise);
    console.log(set);
    
    // After sunset
    for (let i = set + 1; i < 24; i++) {

        const hour = `${i - 12}:00`
        const info = `${hour}PM: ${today.hour[i].cloud}% cloudy - ${today.hour[i].wind_mph}mph winds`;

        // Output to HTML
        $("#hours").append(document.createTextNode(info));
        $("#hours").append(document.createElement("br"));
    }

    // Before sunrise
    for (let i = 0; i < rise ; i++) {

        i === 0 ? hour = "12:00" : hour = `${i}:00`

        const info = `${hour}AM: ${nextDay.hour[i].cloud}% cloudy - ${today.hour[i].wind_mph}mph winds`;

        // Output to HTML
        $("#hours").append(document.createTextNode(info));
        $("#hours").append(document.createElement("br"));
    }

    

    // Input data into HTML
    $("#sunrise").text("Sunrise: " + sunrise);
    $("#sunset").text("Sunset: " + sunset);
    $("#moonrise").text("Moonrise: " + moonrise);
    $("#moonset").text("Moonset: " + moonset);
    $("#phase").text("Moon Phase: " + moon_phase);
    $("#illumination").text("Illumination: " + moon_illumination + "%");
    // $("#hours").text("Moonset: " + moonset);
}))
.catch(err => {
	console.error(err);
});