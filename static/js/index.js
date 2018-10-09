// assign the url to variables
var embarked_url = "/embarked";
var gender_url = "/gender";
var pasgender_url = "/pasgender";
var pasclass_url = "/pasclass";

// plot embarked data to bar 1
Plotly.d3.json(embarked_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    console.log(response)
    var layout = { margin: { t: 30, b:50 },
                   title: "Number of New User by Ports",
                   xaxis: { title: "User Embarked from the Ports "},
                   yaxis: { title: "Number of New User"}            
    }
    Plotly.plot("bar1", data, layout)
})


// plot gender data to bar 2
Plotly.d3.json(gender_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    console.log(response)
    var layout = { margin: { t: 30, b:50 },
                   title: "Number of New User by Gender",
                   xaxis: { title: "User by Gender "},
                   yaxis: { title: "Number of New User"}            
    }
    Plotly.plot("bar2", data, layout)
})

// plot passenger data to bar 3
Plotly.d3.json(pasgender_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    console.log(response)
    var layout = { margin: { t: 30, b:50 },
                   title: "Number of Passengers by Gender",
                   xaxis: { title: "Passenger by Gender "},
                   yaxis: { title: "Number of Passenger"}            
    }
    Plotly.plot("bar3", data, layout)
})

// plot pasanger class data to bar 4
Plotly.d3.json(pasclass_url, function(error, response) {
    if (error) return console.warn(error);
    var data = [response];
    console.log(response)
    var layout = { margin: { t: 30, b:50 },
                   title: "Number of Passengers by Passenger Class",
                   xaxis: { title: "Passengers by Class "},
                   yaxis: { title: "Number of Passengers"}            
    }
    Plotly.plot("bar4", data, layout)
})

