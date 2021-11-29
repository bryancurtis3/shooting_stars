Chart.defaults.color = "#f3e0ea";
const hourly = []
const percentage = []
const mph = []
const backgroundColor = []
const windColor = []

// IP lookup
// fetch("https://weatherapi-com.p.rapidapi.com/ip.json?q=38.140.30.202", {
// 	"method": "GET",
// 	"headers": {
// 		"x-rapidapi-host": "weatherapi-com.p.rapidapi.com",
// 		"x-rapidapi-key": "9cb1c64a74mshe483b1ba55588eep1ea8d5jsn22992105906a"
// 	}
// })
// .then(response => {
// 	console.log(response);
// })
// .catch(err => {
// 	console.error(err);
// });

let userLocation = "";

const options = {
    maximumAge: Infinity,
    timeout: 7000,
}

function error(err) {
    console.warn(`Eroor(${err.code}): ${err.message}`);
}

navigator.geolocation.getCurrentPosition(function (position) {
    console.log(position.coords.latitude);
    userLocation = "" + position.coords.latitude.toString() + "," + position.coords.longitude.toString();
    return console.log(userLocation);
}, error, options)

console.log("test");

// Get city
const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());
if (params.city) {
    city = params.city;
} else {
    city = "Portland";
} 

// Capitalize and display
city = city.charAt(0).toUpperCase() + city.slice(1);
city = city.split(" ");
for (let i = 0; i < city.length; i++) {
    city[i] = city[i][0].toUpperCase() + city[i].substr(1);
}
city = city.join(" ");
$("#city-header").text(`${city} Conditions`);


// Location weather data lookup
fetch(`https://weatherapi-com.p.rapidapi.com/forecast.json?q=${city}&days=2`, {
	"method": "GET",
	"headers": {
		"x-rapidapi-host": "weatherapi-com.p.rapidapi.com",
		"x-rapidapi-key": "9cb1c64a74mshe483b1ba55588eep1ea8d5jsn22992105906a",
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

    // console.log(rise);
    // console.log(set);
    
    // After sunset
    for (let i = set + 1; i < 24; i++) {
        // Hours
        const hour = `${i - 12}:00 PM`
        hourly.push(hour)

        // Clouds
        const cloud = today.hour[i].cloud
        percentage.push(cloud)

        // Wind
        const wind = today.hour[i].wind_mph
        mph.push(wind)
    }

    // Before sunrise
    for (let i = 0; i < rise ; i++) {
        // Hours
        i === 0 ? hour = "12:00 AM" : hour = `${i}:00 AM`
        hourly.push(hour)

        // Clouds
        const cloud = nextDay.hour[i].cloud
        percentage.push(cloud)

        // Wind
        const wind = nextDay.hour[i].wind_mph
        mph.push(wind)

        // const info = `${hour}: ${cloud}% cloudy - ${wind}mph winds`;

        // // Output to HTML
        // $("#hours").append(document.createTextNode(info));
        // $("#hours").append(document.createElement("br"));
    }

    // Milky way (really difficult to make this work everywhere)
    const month = today.date.split("-")[1]
    if (month === "12" || month === "1" || month === "2") {
        console.log("this works")
    }

    // Calculate cloud bar color
    for (let i = 0; i < percentage.length; i++) {
        const calc = percentage[i];
        const color = 100 - (percentage[i] / 2 + 20 - (.2 * percentage[i]));
        percentage[i] < 10 ? backgroundColor[i] = `rgba(40, 40, 40, .0${calc})` : 
        backgroundColor[i] = `rgba(${color}, ${color}, ${color}, .${calc})`
    }

    // Calculate wind bar color
    // for (let i = 0; i < percentage.length; i++) {
    //     const calc = percentage[i];
    //     const color = 100 - (percentage[i] / 2 + 20);
    //     percentage[i] < 10 ? backgroundColor[i] = `rgba(40, 40, 40, .0${calc})` : 
    //     backgroundColor[i] = `rgba(${color}, ${color}, ${color}, .${calc})`
    // }

    // Generate charts
    cloudChart();
    windChart();

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


// console.log(hourly)
// console.log(percentage)
// console.log(backgroundColor)

const cloudChart = function cloudChart() {
    // This is vanilla for gradient compatibility
    const ctx = document.getElementById('cloudChart').getContext('2d');
    
    // Gradient
    const gradient = ctx.createLinearGradient(0, 0, 600, 0);
    gradient.addColorStop(0, '#cccccc44');
    gradient.addColorStop(1, '#444444e6');
    
    const cloudChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hourly,
            datasets: [{
                label: '% cloud coverage',
                data: percentage,
                backgroundColor: gradient,
                hoverBorderColor: '#9f86c0',
                hoverBorderWidth: 2,
            },
        ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    max: 100
                },
            },
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: "y",
        },
    })
}

const windChart = function windChart() {
    // This is vanilla for gradient compatibility
    const ctx = document.getElementById('windChart').getContext('2d');
    
    // Gradient
    const gradient = ctx.createLinearGradient(0, 0, 400, 0);
    gradient.addColorStop(0, '#e0b1cbb3');
    gradient.addColorStop(1, '#e21559f2');

    const windChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hourly,
            datasets: [{
                label: 'wind mph',
                data: mph,
                backgroundColor: gradient,
                hoverBorderColor: '#f3e0ea',
                hoverBorderWidth: 2,
            },
        ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                },
                x: {
                    suggestedMax: 10,
                },
            },
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
        },
        

    })
}

