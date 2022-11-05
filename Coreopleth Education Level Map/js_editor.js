let usEduURL = "https://cdn.freecodecamp.org/testable-projects-fcc/data/choropleth_map/for_user_education.json";
let usCountyURL = "https://cdn.freecodecamp.org/testable-projects-fcc/data/choropleth_map/counties.json";
let usEduData = null;
let usCountyData = null;
let heatmapMultiplier = 6; 
//6 is the sweet spot fot his data coloristically. higher more blue, lower more light.
//nope need to normalize the data.
let min,max; //2.6:75.1 rgb(247,251,255):#08306b

function hardCoded(){
    try{
        fetch(usEduURL)
        .then((response) => {
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
            throw new TypeError("This is not JSON");
            }
            return response.json();
        })
        .then((data) => {
            usEduData = data;
            console.log(Object.keys(usEduData));
            min = d3.min(usEduData, (d)=>d.bachelorsOrHigher);
            max = d3.max(usEduData, (d)=>d.bachelorsOrHigher);
            console.log(min,max);
        })
        .catch((error) => console.error(error));

        fetch(usCountyURL)
        .then((response) => {
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
            throw new TypeError("This is not JSON");
            }
            return response.json();
        })
        .then((data) => {
            usCountyData = data;
        })
        .catch((error) => console.error(error));
    } catch(e){ console.log(error.message); }
}

function normalizeData(v,mn=min,mx=max){
    return (v - mn) / (mx - mn);
}

function fetchJSON(myRequest,JSONObject={}){
    fetch(myRequest)
    .then((response) => {
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
        throw new TypeError("This is not JSON");
        }
        return response.json();
    })
    .then((data) => {
        JSONObject = data;
        console.log(Object.keys(JSONObject));
        /*
        {
		"fips": 1001,
		"state": "AL",
		"area_name": "Autauga County",
		"bachelorsOrHigher": 21.9
	    },
        */
        return JSONObject;
    })
    .catch((error) => console.error(error));
}

//fetchJSON(usEduURL,usEduData);
//fetchJSON(usEduURL,usEduData);
hardCoded();

setTimeout( function(){ 
    try{
    console.log(typeof usEduData, typeof usCountyData, typeof null);
    //testing json accesibility for below here. SEE BELOW
        console.log(JSON.stringify(usEduData).slice(0,100));
        console.log(typeof (usCountyData.objects));
        console.log(JSON.stringify(usCountyData.objects).slice(0,100));
    //testing json accesibility for below here. SEE ABOVE

    //us - is usCountyData.
    let us=usCountyData;
    let counties = topojson.feature(us, us.objects.counties);
    let states = topojson.feature(us, us.objects.states);
    let statemap = new Map(states.features.map(d => [d.id, d]));
    let statemesh = topojson.mesh(us, us.objects.states, (a, b) => a !== b);

    let chart = Choropleth(usEduData, {
        id: d => d.fips,
        value: d => normalizeData(d.bachelorsOrHigher)*heatmapMultiplier,//d.rate,
        scale: d3.scaleQuantize,
        domain: [1, 10],
        range: d3.schemeBlues[9],
        title: (f, d) => `${d?.area_name},${d?.state}: ${d?.bachelorsOrHigher}%`,/*`${f.properties.name}, ${statemap.get((f.id).toString().slice(0, 2)).properties.name}\n${d?.bachelorsOrHigher}%`,*//*`${Object.keys(f)}`,*///`${f.properties.name}`,
        features: counties,
        borders: statemesh,
        width: 975,
        height: 610
    }); 

    console.log(chart.outerHTML.split(0,100));
    document.getElementById("seeChart").innerHTML=chart.outerHTML;
    }catch(e){ console.log(e.toString()); }
    /*
        Errors: that need fixing.
        TypeError: f.id.slice is not a function 
        Line 87.

        f.id.slice(0,2)
        (f.id).toString().slice(0, 2)
    */
},1000 );

// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/choropleth
function Choropleth(data, {
  id = d => d.id, // given d in data, returns the feature id
  value = () => undefined, // given d in data, returns the quantitative value
  title, // given a feature f and possibly a datum d, returns the hover text
  format, // optional format specifier for the title
  scale = d3.scaleSequential, // type of color scale
  domain, // [min, max] values; input of color scale
  range = d3.interpolateBlues, // output of color scale
  width = 640, // outer width, in pixels
  height, // outer height, in pixels
  projection, // a D3 projection; null for pre-projected geometry
  features, // a GeoJSON feature collection
  featureId = d => d.id, // given a feature, returns its id
  borders, // a GeoJSON object for stroking borders
  outline = projection && projection.rotate ? {type: "Sphere"} : null, // a GeoJSON object for the background
  unknown = "#ccc", // fill color for missing data
  fill = "white", // fill color for outline
  stroke = "white", // stroke color for borders
  strokeLinecap = "round", // stroke line cap for borders
  strokeLinejoin = "round", // stroke line join for borders
  strokeWidth, // stroke width for borders
  strokeOpacity, // stroke opacity for borders
} = {}) {
  // Compute values.
  const N = d3.map(data, id);
  //const V = d3.map(data, value).map(d => d == null ? NaN : +d);
  const V = d3.map(data, value).map(d => {  /*console.log(d == null ? NaN : +d*heatmapMultiplier);*/ return d == null ? NaN : +d*heatmapMultiplier});
  const Im = new d3.InternMap(N.map((id, i) => [id, i]));
  const If = d3.map(features.features, featureId);

  // Compute default domains.
  if (domain === undefined) domain = d3.extent(V);

  // Construct scales.
  const color = scale(domain, range);
  if (color.unknown && unknown !== undefined) color.unknown(unknown);

  // Compute titles.
  if (title === undefined) {
    format = color.tickFormat(100, format);
    title = (f, i) => `${f.properties.name}\n${format(V[i])}`;
  } else if (title !== null) {
    const T = title;
    const O = d3.map(data, d => d);
    title = (f, i) => T(f, O[i]);
  }

  // Compute the default height. If an outline object is specified, scale the projection to fit
  // the width, and then compute the corresponding height.
  if (height === undefined) {
    if (outline === undefined) {
      height = 400;
    } else {
      const [[x0, y0], [x1, y1]] = d3.geoPath(projection.fitWidth(width, outline)).bounds(outline);
      const dy = Math.ceil(y1 - y0), l = Math.min(Math.ceil(x1 - x0), dy);
      projection.scale(projection.scale() * (l - 1) / l).precision(0.2);
      height = dy;
    }
  }

  // Construct a path generator.
  const path = d3.geoPath(projection);

  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "width: 100%; height: auto; height: intrinsic;");

  if (outline != null) svg.append("path")
      .attr("fill", fill)
      .attr("stroke", "currentColor")
      .attr("d", path(outline));

  svg.append("g")
    .selectAll("path")
    .data(features.features)
    .join("path")
      .attr("fill", (d, i) => color(V[Im.get(If[i])]))
      .attr("d", path)
    .append("title")
      .text((d, i) => title(d, Im.get(If[i])));

  if (borders != null) svg.append("path")
      .attr("pointer-events", "none")
      .attr("fill", "none")
      .attr("stroke", stroke)
      .attr("stroke-linecap", strokeLinecap)
      .attr("stroke-linejoin", strokeLinejoin)
      .attr("stroke-width", strokeWidth)
      .attr("stroke-opacity", strokeOpacity)
      .attr("d", path(borders));

  return Object.assign(svg.node(), {scales: {color}});
}
