var express = require('express');
var request = require('request');


var app = express();

app.use(express.static("./"));


// app.get('/', function (req, res) {
//    res.send('Hello World');
// })


var access_id = "AIzaSyCpDWvlkvrxDf9XfCA0-g0auNMOFop51FU";
var a_key_param = 'key=' + access_id +  '&';

var yelp_api = 'l4FNMIWkuoWJ0ISafL0cgZUI-j6ao-Xs_sYA601ow8KZsRICgrNtNvDUvVJ1thc8KJAo0mJEoIYiFi_9UcJ7H276m7WfrnhNm8w07VPIMxsxQRAnBHayYbyFteDFWnYx';


app.get('/getplacegeo', function(req,res){

	place_id = req.query.placeid;
	// console.log(place_id);
	// console.log(access_id);

	var place_url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=" + access_id;

	// console.log(req);
	// console.log(req.query);

	request.get({
	    url: place_url,
	    json: true,
	    headers: {'User-Agent': 'request'}
	  }, (err, response, data) => {
	    if (err) {
	    	console.log('Error:', err);
	    } else if (res.statusCode !== 200) {
	    	console.log('Status:', response.statusCode);
	    } else {
	      // data is already parsed as JSON:
	      	// console.log(data);
	      	// console.log('yo');
	      	res.setHeader('content-type', 'application/json');
			res.json(data);
	    }
	});

})


app.get('/getinfo', function(req,res){
	var infourl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=34.0266,-118.2831&radius=16093.4&type=default&keyword=usc&key=AIzaSyCpDWvlkvrxDf9XfCA0-g0auNMOFop51FU&"

	// console.log(req);
	console.log(req.query);

	request.get({
	    url: infourl,
	    json: true,
	    headers: {'User-Agent': 'request'}
	  }, (err, response, data) => {
	    if (err) {
	    	console.log('Error:', err);
	    } else if (res.statusCode !== 200) {
	    	console.log('Status:', response.statusCode);
	    } else {
	      // data is already parsed as JSON:
	      	// console.log(data);
	      	// console.log('yo');
	      	res.setHeader('content-type', 'application/json');
			res.json(data);
	    }
	});

})



app.get('/placedetails', function(req,res){

	var base_url_details = 'https://maps.googleapis.com/maps/api/place/details/json?';
	var placeid = req.query.placeid;
	var placeid_param = 'placeid=' + placeid + '&';

	var details_url = base_url_details + placeid_param + a_key_param;

	console.log('details url - ' + details_url);

	// console.log(req);
	// console.log(req.query);

	request.get({
	    url: details_url,
	    json: true,
	    headers: {'User-Agent': 'request'}
	  }, (err, response, data) => {
	    if (err) {
	    	console.log('Error:', err);
	    } else if (res.statusCode !== 200) {
	    	console.log('Status:', response.statusCode);
	    } else {
	      // data is already parsed as JSON:
	      	// console.log(data);
	      	// console.log('yo');
	      	res.setHeader('content-type', 'application/json');
			res.json(data);
	    }
	});

})


app.get('/searchresults', function(req,res){

	console.log(req.query);

	var search_url_base = req.query.searchurl + '&';
	var locn_param = "location=" + req.query.location + "&";
	var radius_param = "radius=" + req.query.radius + "&";
	var type_param = "type=" + req.query.type + "&";
	var keyword_param = "keyword=" + req.query.keyword + "&";
	var key_param = "key=" + req.query.key + "&";
	var pagetoken_param = "pagetoken=" + req.query.pagetoken + "&";

	var searchurl = search_url_base + radius_param + type_param + keyword_param + pagetoken_param + locn_param;


	console.log('searchurl - ' + searchurl);

	// console.log(req);
	// console.log(req.query);

	request.get({
	    url: searchurl,
	    json: true,
	    headers: {'User-Agent': 'request'}
	  }, (err, response, data) => {
	    if (err) {
	    	console.log('Error:', err);
	    } else if (res.statusCode !== 200) {
	    	console.log('Status:', response.statusCode);
	    } else {
	      // data is already parsed as JSON:
	      	// console.log(data);
	      	// console.log('yo');
	      	res.setHeader('content-type', 'application/json');
			res.json(data);
	    }
	});

})


app.get('/getphoto', function(req,res){

	// var photos_base_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=750&';
	var photos_base_url = 'https://maps.googleapis.com/maps/api/place/photo?&';
	var photo_ref_param = 'photoreference' + req.query.photoref + '&'
	
	// console.log(req);
	// console.log(req.query);

	var photourl = photos_base_url + photo_ref_param + a_key_param;

	request.get({
	    url: photourl,
	    json: true,
	    headers: {'User-Agent': 'request'}
	  }, (err, response, data) => {
	    if (err) {
	    	console.log('Error:', err);
	    } else if (res.statusCode !== 200) {
	    	console.log('Status:', response.statusCode);
	    } else {
	      // data is already parsed as JSON:
	      	// console.log(data);
	      	// console.log('yo');
	      	res.setHeader('content-type', 'application/json');
			res.json(data);
	    }
	});

})


app.get('/getyelpbestmatch', function(req,res){

	// var yelp_best_match_url = 'https://api.yelp.com/v3/businesses/matches/best?name=el%20huero&city=Los%20Angeles&state=CA&address1=3000%20S%20Figueroa%20St,%20Los%20Angeles&country=US&';
	
	// var yelp_best_match_url = 'https://api.yelp.com/v3/businesses/matches/best?name=el%20huero&city=los%20angeles&country=US&state=CA'

	var address_param  = 'address1=' + req.query.address + '&';
	var country_param = 'country=' + req.query.country + '&';
	var state_param = 'state=' + req.query.state + '&';
	var city_param = 'city=' + req.query.city + '&';
	var name_param = 'name=' + req.query.name + '&';

	var yelp_best_match_url = 'https://api.yelp.com/v3/businesses/matches/best?' + address_param + country_param + state_param + city_param + name_param;
	
	console.log(yelp_best_match_url);




	// console.log(req);
	// console.log(req.query);

	request.get({
	    url: yelp_best_match_url,
	    json: true,
	    headers: {'User-Agent': 'request', 'Authorization': 'bearer ' + yelp_api}
	  }, (err, response, data) => {
	    if (err) {
	    	console.log('Error:', err);
	    } else if (res.statusCode !== 200) {
	    	console.log('Status:', response.statusCode);
	    } else {
	      // data is already parsed as JSON:
	      	// console.log(data);
	      	// console.log('yo');
	      	res.setHeader('content-type', 'application/json');
			res.json(data);
	    }
	});

})


app.get('/getyelpreviews', function(req,res){

	var yelp_place_url = 'https://api.yelp.com/v3/businesses/' + req.query.id + '/reviews';
	
	// console.log(req);
	// console.log(req.query);

	request.get({
	    url: yelp_place_url,
	    json: true,
	    headers: {'User-Agent': 'request', 'Authorization': 'bearer ' + yelp_api}
	  }, (err, response, data) => {
	    if (err) {
	    	console.log('Error:', err);
	    } else if (res.statusCode !== 200) {
	    	console.log('Status:', response.statusCode);
	    } else {
	      // data is already parsed as JSON:
	      	// console.log(data);
	      	// console.log('yo');
	      	res.setHeader('content-type', 'application/json');
			res.json(data);
	    }
	});

})






var server = app.listen(8081, function () {
   var host = server.address().address;
   var port = server.address().port;
   
   console.log("app listening at port %s", port);
})