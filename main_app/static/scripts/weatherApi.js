Chart.defaults.color = "#f3e0ea";
const hourly = []
const percentage = []
const mph = []
const gustMph = []
const windDir = []
const backgroundColor = []
const windColor = []

// console.log({userPlace})

// Location weather data lookup
/**
 * 
 * @param {*} place 
 * @description takes in a location and displays current astronomical and meteorological data for the location to the webpage
 */
const getData = function getData(place) {
    fetch(`https://weatherapi-com.p.rapidapi.com/forecast.json?q=${place}&days=2`, {
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
    
        // Destructure variables from JSON
        const { sunrise, sunset, moonrise, moonset, moon_phase, moon_illumination} = today.astro;
        const { sunrise: nextSunrise } = nextDay.astro;

        const { humidity, temp_f } = nextDay.hour[0];

        const { lat, lon } = json.location;
    
        const rise = parseInt(nextSunrise[0] + nextSunrise[1]);
        const set = parseInt(sunset[0] + sunset[1]) + 12;
        // const night = set - rise;
    
        // console.log(rise);
        // console.log(set);
        
        // After sunset
        for (let i = set + 1; i < 24; i++) {
            // Hours
            const hour = `${i - 12}:00 PM`;
            hourly.push(hour);

            // Clouds
            const cloud = today.hour[i].cloud;
            percentage.push(cloud);
    
            // Wind
            const wind = today.hour[i].wind_mph;
            mph.push(wind);

            // Wind Gusts
            const gust = today.hour[i].gust_mph;
            gustMph.push(gust - wind);

            // Wind Direction
            const dir = today.hour[i].wind_dir;
            windDir.push(dir);
        }
    
        // Before sunrise
        for (let i = 0; i < rise ; i++) {
            // Hours
            i === 0 ? hour = "12:00 AM" : hour = `${i}:00 AM`;
            hourly.push(hour);
    
            // Clouds
            const cloud = nextDay.hour[i].cloud;
            percentage.push(cloud);
    
            // Wind
            const wind = nextDay.hour[i].wind_mph;
            mph.push(wind);

            // Wind Gusts
            const gust = nextDay.hour[i].gust_mph;
            gustMph.push(gust - wind);

            // Wind Direction
            const dir = nextDay.hour[i].wind_dir;
            windDir.push(dir);
        }
    
        // Milky way (really difficult to make this work everywhere)
        // const month = today.date.split("-")[1]
        // if (month === "12" || month === "1" || month === "2") {
        //     console.log("this works")
        // }
    
        // Calculate cloud bar color
        for (let i = 0; i < percentage.length; i++) {
            const calc = percentage[i];
            const color = 100 - (percentage[i] / 2 + 20 - (.2 * percentage[i]));
            percentage[i] < 10 ? backgroundColor[i] = `rgba(40, 40, 40, .0${calc})` : 
            backgroundColor[i] = `rgba(${color}, ${color}, ${color}, .${calc})`;
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

        // Set iFrame source
        $("#iframe").attr('src', `https://www.lightpollutionmap.info/#zoom=12.00&lat=${lat}&lon=${lon}&layers=B0FFFFFFFTFFFFFFFFFF`);

        // Set see-posts href
        $("#posts-from-here").attr("href", `/posts/?q=${lat},${lon}`);

        // Spinner switcher
        $(".spinner-holder").hide();
        $(".place-header").css("border-top", "none")
        $(".place-header").css("margin", "0");
        $("#place-header").show();
        $("#posts-from-here").show();
    
        // Header
        json.location.country === "United States of America" ? area = json.location.region : area = json.location.country; // State if USA, else: country
        $("#place-header").text(`${json.location.name}, ${area}`);
    
        // Remove leading 0 in times
        const noZero = function noZero(time) {
            if (time[0] === "0") time = time.substring(1);
            return time;
        }

        // Rise and set times with their cooresponding AM/PM
        const sunriseTime = noZero(sunrise.split(" ")[0]);
        const sunriseM = sunrise.split(" ")[1];
        const sunsetTime = noZero(sunset.split(" ")[0]);
        const sunsetM = sunset.split(" ")[1];
        const moonriseTime = noZero(moonrise.split(" ")[0]);
        const moonriseM = moonrise.split(" ")[1]
        const moonsetTime = noZero(moonset.split(" ")[0]);
        const moonsetM = moonset.split(" ")[1];

        // Input data into HTML
        $("#sunrise").text(sunriseTime);
        $("#sunriseM").text(sunriseM);
        $("#sunset").text(sunsetTime);
        $("#sunsetM").text(sunsetM);

        $("#lum").text(`(${moon_illumination}%)`)
        $("#moonrise").text(moonriseTime);
        $("#moonriseM").text(moonriseM);
        $("#moonset").text(moonsetTime);
        $("#moonsetM").text(moonsetM);

        $("#humidity").text("Humidity: "+ humidity + "%");
        $("#temp").text("Temperature: " + temp_f + "° F");

        $(".timedate").attr("href", `https://www.timeanddate.com/astronomy/@${lat},${lon}`);

        $("#phase").text("Moon Phase: " + moon_phase);
        $("#illumination").text("Illumination: " + moon_illumination + "%");
        // $("#hours").text("Moonset: " + moonset);
        
    }))
    .catch(err => {
        $("#place-header").text(`Location Not Found`);
        console.error(err);
    });
}



const cloudChart = function cloudChart() {
    // This is vanilla for gradient compatibility
    const ctx = document.getElementById('cloudChart').getContext('2d');
    
    // Gradient
    const gradient = ctx.createLinearGradient(0, 0, 400, 0);
    gradient.addColorStop(0, '#cccccc44');
    gradient.addColorStop(1, '#444444e6');

    // let width, height, gradient;
    // function getGradient(ctx, chartArea) {
    //     const chartWidth = chartArea.right - chartArea.left;
    //     const chartHeight = chartArea.bottom - chartArea.top;
    //     if (!gradient || width !== chartWidth || height !== chartHeight) {
    //         // Create the gradient because this is either the first render
    //         // or the size of the chart has changed
    //         width = chartWidth;
    //         height = chartHeight;
    //         const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
    //         gradient.addColorStop(0, '#cccccc44');
    //         gradient.addColorStop(1, '#444444e6');
    //     }

    //     return gradient;
    // }
    
    const cloudChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hourly,
            datasets: [{
                label: '% cloud coverage',
                data: percentage,
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
                    max: 100
                },
            },
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: "y",
            plugins: {
                legend: {
                  position: 'top',
                },
                // tooltip: {
                //     callbacks: {
                //       footer: footer,
                //     }
                //   }
              }
        },
    })
}

// console.log(windDir)

const windChart = function windChart() {
    // This is vanilla for gradient compatibility
    const ctx = document.getElementById('windChart').getContext('2d');

    
    // Tooltip wind direction
    const footer = (tooltipItems) => {
        let direction = null
        tooltipItems.forEach(function(tooltipItem) {
            direction = windDir[tooltipItem.dataIndex]
        });
        return direction;
    };
    
    // Wind Gradient
    const gradient = ctx.createLinearGradient(0, 0, 300, 0);
    gradient.addColorStop(0, '#e0b1cbb3');
    gradient.addColorStop(1, '#eb6c9cb3');

    // Gust Gradient
    const gustGradient = ctx.createLinearGradient(200, 0, 600, 0);
    gustGradient.addColorStop(0, '#eb6c9cb3');
    gustGradient.addColorStop(1, '#e21559f2');

    const windChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hourly,
            datasets: 
            [{
                label: 'wind mph',
                data: mph,
                backgroundColor: gradient,
                hoverBorderColor: '#f3e0ea',
                hoverBorderWidth: 2,
            },
            {
                label: 'gust mph',
                data: gustMph,
                backgroundColor: gustGradient,
                hoverBorderColor: '#f3e0ea',
                hoverBorderWidth: 2,
            }
        ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    stacked: true,
                },
                x: {
                    suggestedMax: 10,
                    stacked: true,
                },
            },
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        footer: footer,
                    }
                }
            },
        },

    })
}

// === Business Handled Bellow ===

// let userLocation = "";
const options = {
    maximumAge: Infinity,
    timeout: 7000,
}
// Handle no location data, get default location
function error(err) {
    console.warn(`Error(${err.code}): ${err.message}`);
    return getData("-22.9105,-68.2011");
}

// Get available URL params
const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());

// If query in the URL, use query -> fallback to user location -> fallback to default location
if (params.place) {
    place = params.place;
    getData(place)

// } else if (typeof userPlace !== "undefined") {
//     getData(userPlace)

} else {
    navigator.geolocation.getCurrentPosition(function (position) {
        console.log(position.coords.latitude);
        const latitude = position.coords.latitude.toString();
        const longitude = position.coords.longitude.toString()

        userLocation = "" + latitude + "," + longitude;

        return getData(userLocation);
    }, error, options);
} 





// function plotSine(ctx) {
//     var width = ctx.canvas.width;
//     var height = ctx.canvas.height;
//     var scale = 20;

//     ctx.beginPath();
//     ctx.lineWidth = 2;
//     ctx.strokeStyle = "rgb(66,44,255)";
    
//     var x = 0;
//     var y = 0;
//     var amplitude = 40;
//     var frequency = 20;
//     //ctx.moveTo(x, y);
//     while (x < width) {
//         y = height/2 + amplitude * Math.sin(x/frequency);
//         ctx.lineTo(x, y);
//         x = x + 1;
//     }
//     ctx.stroke();
// }