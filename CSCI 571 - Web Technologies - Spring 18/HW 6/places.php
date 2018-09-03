<!DOCTYPE html>

<!-- MAIN PHP -->

<!-- <?php //var_dump($_POST); ?> -->

	<!-- <br> -->
	<!-- <br> -->

<!-- php var/fn init -->
<?php 

	$test = "";
	$keyword = "";
	$category = "default";
	$distance = "10";
	$distance_form = "";
	$locn = ""; 
	$from = "";
	$loc_json = "";
	$results_json = "";
	$lat = "0";
	$lon = "0";
	$locn_form = "";
	$keyword_ip = "";

	$google_access_id = "";
	$pagetoken = "";
	$base_url = "";
	$locn_param = "";
	$radius_param = "";
	$type_param = "";
	$keyword_param = "";
	$key_param = "";
	$pagetoken_param = "";
	$full_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?";

	$get_locn_url = "https://maps.googleapis.com/maps/api/geocode/json?";
	$get_locn_url_base = "";


	$target_lat = "";
	$target_lon = "";
	$place_id = "";
	$submit_type = "";

	$place_details = "";

	$place_info_url = "https://maps.googleapis.com/maps/api/place/details/json?";
	$place_info_url_base = "https://maps.googleapis.com/maps/api/place/details/json?";

	$toDisplay = "search";


	$review_name0 = "";
	$review_name1 = "";
	$review_name2 = "";
	$review_name3 = "";
	$review_name4 = "";

	$review_img0 = "https://upload.wikimedia.org/wikipedia/commons/e/eb/Blank.jpg";
	$review_img1 = "https://upload.wikimedia.org/wikipedia/commons/e/eb/Blank.jpg";
	$review_img2 = "https://upload.wikimedia.org/wikipedia/commons/e/eb/Blank.jpg";
	$review_img3 = "https://upload.wikimedia.org/wikipedia/commons/e/eb/Blank.jpg";
	$review_img4 = "https://upload.wikimedia.org/wikipedia/commons/e/eb/Blank.jpg";


	$review_review0 = "";
	$review_review1 = "";
	$review_review2 = "";
	$review_review3 = "";
	$review_review4 = "";

	$clear_form = 0;

	$reviews_max = 0;
	$photos_max = 0;
	$place_details_name = "";




	function encodeURIComponent($str) {
    	$revert = array('%21'=>'!', '%2A'=>'*', '%27'=>"'", '%28'=>'(', '%29'=>')');
    	return strtr(rawurlencode($str), $revert);
	}

?>

<br>
<br>


<?php

	// $loc_json = json_decode(file_get_contents("http://ip-api.com/json?"));
	// $lat = $loc_json->lat;
	// $lon = $loc_json->lon;

	// if (!empty($_POST)) {
	// 	echo "not empty";
	// 	echo var_dump($_POST);
	// } else {
	// 	echo "empty";
	// }


	if( !empty($_POST)) {
		// echo 'test test ';

		// get data 

		$keyword =  encodeURIComponent($_POST["keyword"]);
		$keyword_ip = $_POST["keyword"];
		$category = $_POST["category"];
		$distance = $_POST["distance"];
		$distance_form = $distance;
		$locn = $_POST["locn"];
		$locn_form = $_POST['locn'];
		$from = $_POST["from"];
		$lat = $_POST["lat"];
		$lon = $_POST["lon"];
		$submit = $_POST["submit_type"];

		$target_lat = $_POST["target_lat"];
		$target_lon = $_POST["target_lon"];
		$place_id_ = $_POST["place_id"];
		$submit_type = $_POST["submit_type"];

		// echo $lat." ".$lon;


		$google_access_id = "AIzaSyCpDWvlkvrxDf9XfCA0-g0auNMOFop51FU";
		$pagetoken = "";

		
		// clean data

		if ($distance == "") {
        	$distance = "10";
    	}

    	// $distance_float = (float) $distance;
    	// $distance_in_met = $distance_float

    	$distance = (string) ( ((float)($distance)) * 1609.34 );
    	if ($distance > 50000) {

    		$distance = 50000;
    	}

		if ($locn == "" || $from == "here") {
			// $lat_use = $lat;
			// $lon_use = $lon;
			$locn = $lat.",".$lon;
        }


        if ($from != "here") {
        	$get_locn_url_base = "https://maps.googleapis.com/maps/api/geocode/json?address=";
			$key_param = "key=".$google_access_id."&";
        	$get_locn_url = $get_locn_url_base.encodeURIComponent($locn)."&".$key_param;

        	// echo "   ..  ".$get_locn_url;

        	// echo $get_locn_url;

        	$new_loc_json = json_decode(file_get_contents($get_locn_url));
        	// echo "";
        	if ($new_loc_json->status == "OK") {
        		
				$lat = $new_loc_json->results[0]->geometry->location->lat;
				$lon = $new_loc_json->results[0]->geometry->location->lng;
				$locn = $lat.",".$lon;

			} else if($new_loc_json->status == "ZERO_RESULTS") {
				echo "<div class='error-div'><center>Couldn't find geolocation for - $locn <center></div>";
				$clear_form = 10;
			}

			// echo "yoo".$lat."yoo";

        }

		// make url

		$base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?";
		$locn_param = "location=".$locn."&";
		$radius_param = "radius=".$distance."&";
		$type_param = "type=".$category."&";
		$keyword_param = "keyword=".$keyword."&";
		$key_param = "key=".$google_access_id."&";
		$pagetoken_param = "pagetoken=".$pagetoken."&";

		$full_url = $base_url.$locn_param.$radius_param.$type_param.$keyword_param.$key_param;

		// echo $full_url;


		if ($submit_type == "js_submit") {

			$place_id_param = 'placeid='.$place_id_.'&';
			$toDisplay = "reviews";
			$place_info_url = $place_info_url_base.$place_id_param.$key_param;

			// echo $place_info_url;

			$place_details = file_get_contents($place_info_url);
			$place_details_json = json_decode($place_details);
			// echo $place_details_json->status;
			$place_details_status = $place_details_json->status;
			$place_details_name = $place_details_json->result->name;

			if (array_key_exists('photos', $place_details_json->result)) {
				$num_of_photos =  count($place_details_json->result->photos);
			} else {
				$num_of_photos = 0;
			}

			

			$photos_max = 0;
			if ($num_of_photos > 5) {
				$photos_max = 5;
			} else {
				$photos_max = $num_of_photos;
			}


			$url_for_photos_base = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=750&';

			for($i = 0; $i<$photos_max; $i++){
				$photo_ref = $place_details_json->result->photos[$i]->photo_reference;
				$photo_ref_param = 'photoreference='.$photo_ref.'&';
				$url_for_photos = $url_for_photos_base.$photo_ref_param.$key_param;

				file_put_contents("./img".$i.".jpg",file_get_contents($url_for_photos)); 
				//echo $i;
			}

			if (array_key_exists('reviews', $place_details_json->result)) {
				$num_of_reviews = count($place_details_json->result->reviews);
			} else {
				$num_of_reviews = 0;
			}

			// echo "yoo".$reviews_max;
			
			$reviews_max = 0;
			if ($num_of_reviews > 5) {
				$reviews_max = 5;
			} else {
				$reviews_max = $num_of_reviews;
			}

			// echo "yoo".$reviews_max;


			// echo "reviews ".$reviews_max;

			if ($reviews_max >= 1) {
				$review_name0 = ($place_details_json->result->reviews[0]->author_name);
				if(array_key_exists('profile_photo_url', $place_details_json->result->reviews[0])){
					$review_img0 = $place_details_json->result->reviews[0]->profile_photo_url;
				}
				$review_review0 = $place_details_json->result->reviews[0]->text;
			}

			if ($reviews_max >= 2) {
				$review_name1 = ($place_details_json->result->reviews[1]->author_name);
				if(array_key_exists('profile_photo_url', $place_details_json->result->reviews[1])){
					$review_img1 = $place_details_json->result->reviews[1]->profile_photo_url;
				}
				$review_review1 = $place_details_json->result->reviews[1]->text;
			}

			if ($reviews_max >= 3) {
				$review_name2 = ($place_details_json->result->reviews[2]->author_name);
				if(array_key_exists('profile_photo_url', $place_details_json->result->reviews[2])){
					$review_img2 = $place_details_json->result->reviews[2]->profile_photo_url;
				}
				$review_review2 = $place_details_json->result->reviews[2]->text;
			}

			if ($reviews_max >= 4) {
				$review_name3 = ($place_details_json->result->reviews[3]->author_name);
				if(array_key_exists('profile_photo_url', $place_details_json->result->reviews[3])){
					$review_img3 = $place_details_json->result->reviews[3]->profile_photo_url;
				}
				$review_review3 = $place_details_json->result->reviews[3]->text;
			}

			if ($reviews_max == 5) {
				$review_name4 = ($place_details_json->result->reviews[4]->author_name);
				if(array_key_exists('profile_photo_url', $place_details_json->result->reviews[4])){
					$review_img4 = $place_details_json->result->reviews[4]->profile_photo_url;
				}
				$review_review4 = $place_details_json->result->reviews[4]->text;
			}

			// echo htmlspecialchars($review_name2);


		}

	}

?>


<html>
	<head>
		<title>Travel and Entertainment Search</title>
		
		<style>

		*, body, html {
			margin: 0;
			padding: 0;	
		}


		.travel-text {
			text-align: center;
		}


		.form-div {
			position: relative;
			margin-left: auto;
			margin-right: auto;
			top: 30px;
			border: 2px solid gray;
			width: 750px;
			height: 220px;
			/*padding-left: 10px;*/
		}


		div.border {
			border-bottom: 2px solid lightgray; 
			width: 95%;
			margin: auto;
			padding-top: 5px;
			font-style: italic;
		}
		

		form.form {
			padding-top: 15px;
		}

		table.form-table td{
			padding-left: 10px;
		}

		a{
			text-decoration: none;
			color: black;
		}


		#search-results-table {
			/*width: inherit;*/
			margin: auto;
			margin-top: 70px;
			width: 90%;
			table-layout: fixed;
			border: 1px black solid;
		}

		#search-results-table td, th {
			border: 1px black solid;
			padding-top: 3px;
			padding-bottom: 3px;
			padding-left: 5px;
		}


		#table-row-1 {
			width: 10%;
		}

		#table-row-2 {
			width: 45%;
		}

		#table-row-3 {
			width: 45%;
		}

		/*      REVIEW TABLE CSS      */ 

		.container{
			width: 750px;
			margin: auto;
		}

		.arrow-img {
			width: 5%;
			height: 5%;
			margin-top: 5px;
			margin-bottom: 5px;
		}

		.reviews {
			width: 750px;
		}


		#reviews-up-arrow{
			display: none;
		}

		#reviews-down-arrow{

		}

		#photos-up-arrow{
			display: none;
		}

		#photos-down-arrow{

		}

		#reviews-table {
			margin: auto;
			width: 100%;
			display: none;

		}

		#reviews-table tr{
			outline: thin solid;
		}

		#reviews-table td, th {
			width: 750px;
			padding-left: 5px;
			padding-top: 3px;
			padding-bottom: 3px;
		}

		.img-circle {
			border-radius: 50%;
			width: 30px;
			height: 30px;
		}


		.photos-table {

			width: 750px;
			text-align: center;
		}

		#photos-table {
			display: none;
		}

		#photos-table tr{
			outline: thin solid;
		}

		#photos-table td{
			width: 750px;
			padding-top: 30px;
			padding-bottom: 30px;
		}

		.photos-img {
			width: 650px;
			/*height: 400px;*/
			margin: auto;
		}



		/* map thing */


		.for-position {
			position: relative;
		}

		#map-and-modes {
			position: absolute;
			/*top: 0px;*/
			/*left: 0px;*/
			width: 260px;
			height: 240px;
			/*background-color: red;*/
			display: none;

		}


		#map {
		  height: 240px;
		  width: 260px;
		  position: absolute;
		}

		

		/*#floating-panel {
		  position: absolute;
		  top: 10px;
		  left: 25%;
		  z-index: 5;
		  background-color: #fff;
		  padding: 5px;
		  border: 1px solid #999;
		  text-align: center;
		  font-family: 'Roboto','sans-serif';
		  line-height: 30px;
		  padding-left: 10px;
		}*/


		div#modes-list-div {
			width: 100px;
			/*margin: 0;*/
			/*padding: 0;*/
			position: absolute;
			display: none;

		}


		ul.modes-list {
			list-style-type: none;
		}


		ul.modes-list li {
			background-color: lightgray;
			padding-top: 2.5px;
			padding-bottom: 2.5px;
			padding-left: 2.5px;
		}


		ul.modes-list li a{
			text-decoration: none;
			color: black;
		}

		ul.modes-list li:hover {
			background-color: gray;
		}

		input:-moz-placeholder {
		    box-shadow:none !important;
		}

		input:invalid {
		    box-shadow:none ;
		}


		</style>

	</head>
	<body>

		<div class="form-div">

			<h2 class="travel-text"> Travel and Entertainment Search </h2>
			
			<div class="border"></div>


			<form class="form" id="form" name="TheForm" action="" method="post">

				<table class="form-table">
					<tr>
						<td>Keyword</td>
						<td><input type="text" name="keyword" id="keyword" required></td>
					</tr>

					<tr>
						<td>Category</td>
						<td><select name="category" id="category">
						<option value="default"> default </option>
						<option value="cafe"> cafe</option>
						<option value="bakery"> bakery</option>
						<option value="restaurant"> restaurant</option>
						<option value="beautysalon"> beauty salon</option>
						<option value="casino"> casino</option>
						<option value="movietheater"> movie theater</option>
						<option value="lodging"> lodging</option>
						<option value="airport"> airport</option>
						<option value="trainstation"> train station</option>
						<option value="subwaystation"> subway station</option>
						<option value="busstation"> bus station</option>
						</td>
					</tr>

					<tr>
						<td>Distance (miles)</td>
						<td><input type="text" name="distance" id="distance" placeholder="10"></td>
						<td> from </td>
						<td><input type="radio" name="from" value="here" id="here_radio" onclick="document.getElementById('locn_val').readOnly = true; document.getElementById('locn_val').required = false" checked> Here</td>
					</tr>

					<tr>
						<td></td>
						<td></td>
						<td></td>
						<td><input type="radio" name="from" value="locn" id="locn_radio" onclick="document.getElementById('locn_val').readOnly = false; document.getElementById('locn_val').required = true"> <input type="text" name="locn" id="locn_val" placeholder="location" readonly></td>
					</tr>

					<tr>
						<td><button type="submit" name="btn-submit" id="btn-submit" disabled="">Submit</button></td>
						<td><input type="button" name="clear" value="Clear" onclick="resetForm(0)"></td>
						<!-- <td><input type="button" name="clear" value="Test" onclick="test_submit()"></td> -->
					</tr>

					<tr>
						<td><input type="hidden" name="lat" id="lat"></td>
						<td><input type="hidden" name="lon" id="lon"></td>
						<td><input type="hidden" name="target_lat" id="target_lat"></td>
					</tr>

					<tr>
						<td><input type="hidden" name="target_lon" id="target_lon"></td>
						<td><input type="hidden" name="place_id" id="place_id"></td>
						<td><input type="hidden" name="submit_type" id="submit_type" value="user_submit"></td> 
						<!-- possible input vals ->  user_submit, js_submit   -->
					</tr>

				</table>

			</form>

		</div>

		<!-- <div>
			<p id="test">yoo</p>
		</div> -->

		<!-- search result table -->

		<div class="map-and-modes" id="map-and-modes">

			<div id="map">
			</div>


			<div class="modes-list-div" id="modes-list-div">
			<ul class="modes-list">
				<li><a href="#/" onclick="calculateAndDisplayRoute(directionsService, directionsDisplay, 'WALKING', 37.77, -122.447);">Walk There</a></li>
				<li><a href="#/" onclick="calculateAndDisplayRoute(directionsService, directionsDisplay, 'DRIVING', 37.77, -122.447);">Drive There</a></li>
				<li><a href="#/" onclick="calculateAndDisplayRoute(directionsService, directionsDisplay, 'BICYCLING', 37.77, -122.447);">Bike There</a></li>
			</ul>

			</div>

		</div>


		<div id="search-results-table-div">
			
			<table id="search-results-table">

				<!-- <tr>
					<th id="table-row-1">Category</th>
					<th id="table-row-2">Name</th>
					<th id="table-row-3">Address</th>
				</tr> -->

				<!-- <tr>
					<td>Yooooooooo</td>
					<td>Yooooooooo</td>
					<td>Yooooooooo</td>
				</tr> -->



				
			</table>

		</div>

		<!-- review table -->


		<div class="container" id="reviews-go-here">

		</div>





		<!-- //////////////////////////////////     JS START      ////////////////////////////////// -->



		<script type="text/javascript">
			
			var lat = "";
			var lon = "";

			var keyword = " s";
			var category = "";
			var distance = "";
			var locn = "";
			var here = "";

			// might have to change.
			function resetForm(temp) {
            	document.getElementById('keyword').value = "";
        		document.getElementById('category').value = "default";
        		document.getElementById('distance').value = "";

        		if (document.getElementById('locn_radio').checked == true) {
        			document.getElementById('here_radio').checked = true;
        			document.getElementById('locn_radio').checked = false;  
        			document.getElementById('locn_val').value = "";
        			document.getElementById('locn_val').readOnly = true;

        		}

        		document.getElementById('reviews-go-here').style.display = "none";
        		document.getElementById('search-results-table').style.display = "none";

        		if (temp != 10) {
        			document.getElementById('error-div').style.display = 'none';
        		}


        	}


        	function enableSubmit(){
        		document.getElementById('btn-submit').disabled = false; 
        	}

        	function loadJSON(path, success, error){
			    var xhr = new XMLHttpRequest();
			    xhr.onreadystatechange = function()
			    {
			        if (xhr.readyState === XMLHttpRequest.DONE) {
			            if (xhr.status === 200) {
			                if (success)
			                    success(JSON.parse(xhr.responseText));
			                	// return xhr.responseText;
			                	// console.log(xhr.responseText);
			                	// console.log(typeof xhr.responseText)

			            } else {
			                if (error)
			                    error(xhr);
			            }
			        }
			    };
			    xhr.open("GET", path, false);
			    xhr.send();
			}


        	function getlocns() {

        		// console.log(10);
        		status = 'fail';
        		while(status == 'fail') {
	        		var locn_string = '<?php $loc_json = (file_get_contents("http://ip-api.com/json?")); echo $loc_json ?>';
	        		var locn_json = JSON.parse(locn_string);
	        		var status = locn_json['status'];
	        		if (status == 'success') {
		        		enableSubmit();
		        		lat = locn_json['lat'];
		        		lon = locn_json['lon'];
		        		// console.log(lat + " " + lon);   // working
	        		}
        		}
        	}



        	window.onload = function doThis() {

        		clear_form = <?php echo $clear_form ?>

        		if (clear_form == 10) { resetForm(10); }

        	
        		loadJSON('http://ip-api.com/json?',
			        function(data) { /*console.log(data['lat']);*/ document.getElementById('lat').value = data['lat'];
				document.getElementById('lon').value = data['lon'];},
			        function(xhr) { console.error(xhr); }
				);

				// console.log("yoloylolol");
				// console.log(somejson);

				




        		// console.log(11);

        		// console.log(10);
        		status = 'fail';
        		while(status == 'fail') {
	        		var locn_string = '<?php echo $loc_json ?>';
	        		var locn_json = JSON.parse(locn_string);
	        		var status = locn_json['status'];
	        		if (status == 'success') {
		        		enableSubmit();
		        		lat = locn_json['lat'];
		        		lon = locn_json['lon'];
		        		// console.log(lat + " " + lon);   // working
	        		}
        		}        		


        		keyword = ('<?= $keyword ?>');
        		category = '<?= $category ?>';
        		distance = '<?= $distance ?>';
        		locn = '<?= $locn ?>';
        		from = '<?= $from ?>';
        		distance_form = '<?= $distance_form ?>';
        		locn_form = '<?= $locn_form ?>';
        		keyword_ip = '<?= $keyword_ip ?>'

        		// form value retain
        		if (keyword != "") {
        			document.getElementById('keyword').value = keyword_ip;
        		}
        		document.getElementById('category').value = category;
        		document.getElementById('distance').value = distance_form;

        		if (from == 'locn') {
        			document.getElementById('locn_radio').checked = true;
        			document.getElementById('locn_val').value = locn_form;
        			document.getElementById('locn_val').readOnly = false;

        		}


        		// var something = 'something';

        		if (distance == "") {
        			var distance = "10";
        		}

        		distance = (parseFloat(distance)*1609.3).toString();

        		if (locn == "" || from == "here") {
        			var lat_use = lat;
        			var lon_use = lon;
        			locn = lat + "," + lon;
        		}


        		// console.log(keyword);	
        		// console.log(category);	
        		// console.log(distance);	
        		// console.log(locn);	
        		// console.log(from);
        		// console.log("");

        		
        		// something = 'sss'
        		// var wholething = keyword + " " + category;
        		// document.getElementById('test').innerHTML = wholething;


        		////////////////////////////////////////////////////////////

				var google_access_id = "AIzaSyCpDWvlkvrxDf9XfCA0-g0auNMOFop51FU";
				var pagetoken = "";

				var base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?";
				var locn_param = "location=" + locn + "&";
				var radius_param = "radius=" + distance + "&";
				var type_param = "type=" + category + "&";
				var keyword_param = "keyword=" + keyword + "&";
				var key_param = "key=" + google_access_id + "&";
				var pagetoken_param = "pagetoken=" + pagetoken + "&";

				// var full_url = base_url + locn_param + radius_param + type_param + keyword_param + key_param;
				var full_url = '<?= $full_url ?>';
				console.log('ayy')
				console.log(full_url);
				console.log();

				var results_json_str = "";
				
				results_json_str = <?php $results_json_ = (file_get_contents($full_url)); echo json_encode($results_json_) ?>;			

				results_json = JSON.parse(results_json_str);	

				console.log(results_json);

				// MAKE HTML TABLE!

				var html_table_head = '<tr>\
										<th id="table-row-1">Category</th>\
										<th id="table-row-2">Name</th>\
										<th id="table-row-3">Address</th>\
									</tr>';

				var html_table_innerHTML = html_table_head;

				var toDisplay = '<?php echo $toDisplay ?>';


				if (toDisplay == "search") {
					if (results_json['status'] == 'OK') {
						var results_len = results_json['results'].length;
						for (var i =  0; i < results_len; i++) {
							var name = results_json['results'][i]['name'];
							var icon = results_json['results'][i]['icon'];
							var address = results_json['results'][i]['vicinity'];
							var place_id_from_table = results_json['results'][i]['place_id'];
							var lat_s = results_json['results'][i]['geometry']['location']['lat'];
							var lon_s = results_json['results'][i]['geometry']['location']['lng'];
							// console.log(place_id_from_table);
							//'<a href="#/" onclick="initMap(' + lat_s + ',' + lon_s + '); movemap();>'

							var html_table_row = '<tr>\
													<td>' + '<img src="' + icon + '" style="width:50px;height:50px;margin:auto;">' + '</td>\
													<td>' + '<a href=#/ onclick=getReviews("' + place_id_from_table + '") >' + name + '</a>' + '</td>\
													<td>' + '<a href ="#/" onclick="initMap(' + lat_s + ',' + lon_s + '); movemap();">' + address + '</a>' + '</td>\
												</tr>';

							// console.log(name + " ... " + address);

							html_table_innerHTML = html_table_innerHTML + html_table_row;
						}

						document.getElementById('search-results-table').innerHTML = html_table_innerHTML;
					}

					else if (results_json['status'] == 'ZERO_RESULTS') {
						document.getElementById('search-results-table').innerHTML = '<tr><td ><center>Sorry No Records Found</center></td></tr>';
					}

					else {
						document.getElementById('search-results-table').innerHTML = '';
					}
				}

				else if (toDisplay == "reviews") {

					var review_name0 = "";
					var review_name1 = "";
					var review_name2 = "";
					var review_name3 = "";
					var review_name4 = "";
					var review_img0 = "";
					var review_img1 = "";
					var review_img2 = "";
					var review_img3 = "";
					var review_img4 = "";
					var review_review0 = "";
					var review_review1 = "";
					var review_review2 = "";
					var review_review3 = "";
					var review_review4 = "";

					var reviews_html_code = "";

					var review_html_start = '<center><span class="place-name"><h4>';
					var review_html_place_name = '<?php echo $place_details_name ?>';


					var review_html_part1 = '</h4></span></center><br><br><div class="reviews"><center><span class="reviews-head-text">click to show reviews</span></center><center><a href="#/" class="reviews-down-arrow" id="reviews-down-arrow" onclick="reviewsTableOn()"><img src="http://cs-server.usc.edu:45678/hw/hw6/images/arrow_down.png" class="arrow-img"></a></center><center><a href="#/" class="reviews-up-arrow" id="reviews-up-arrow" onclick="reviewsTableOff()"><img src="http://cs-server.usc.edu:45678/hw/hw6/images/arrow_up.png" class="arrow-img"></a></center><table id="reviews-table">'; 

					var review_html_part2 = '<tr><th><center> <img src="';

					// url for img //

					var review_html_part3 = '" class="img-circle"> ';

					// reviewer name //

					var review_html_part4 = '</center></th></tr><tr><td>';

					// review //

					var review_html_part5 = '</td></tr>';

					review_html_part6 = '</table></div><br><br><div class="photos"><center><span class="photos-head-text">click to show photos</span></center><center><a href="#/" class="photos-down-arrow" id="photos-down-arrow" onclick="photosTableOn()"><img src="http://cs-server.usc.edu:45678/hw/hw6/images/arrow_down.png" class="arrow-img"></a></center><center><a href="#/" class="photos-up-arrow" id="photos-up-arrow" onclick="photosTableOff()"><img src="http://cs-server.usc.edu:45678/hw/hw6/images/arrow_up.png" class="arrow-img"></a></center><center><table id="photos-table">'; 

					review_html_part7 = '<tr><td><a href="./';
					review_html_part72 = '<tr><td><a target="_blank" href="./';
					
					// img name in server //

					var review_html_part8 = '"><img src="./';

					// img name in server //

					var review_html_part9 = '" class="photos-img"></a></td></tr>';

					review_html_part10 = '</table></center></div>';

					// done phew! //


					var num_of_reviews = <?php echo $reviews_max ?>;

					var rev = "";
					var rev0 = "";
					var rev1 = "";
					var rev2 = "";
					var rev3 = "";
					var rev4 = "";

					console.log(num_of_reviews);

					if (num_of_reviews == 0) {

						rev = "<tr><td style='padding: 3px;'>No Reviews Available</td></tr>";

					}

					if (num_of_reviews>=1) {
						review_name0 = <?php echo json_encode($review_name0) ?>;
						review_img0 = <?php echo json_encode($review_img0) ?>;
						review_review0 = <?php echo json_encode($review_review0) ?>;

						rev0 = review_html_part2 + review_img0 + review_html_part3 + review_name0 + (review_html_part4) + review_review0 + review_html_part5
					}


					if (num_of_reviews>=2) {
						review_name1 = <?php echo json_encode($review_name1) ?>;
						review_img1 = <?php echo json_encode($review_img1) ?>;
						review_review1 = <?php echo json_encode($review_review1) ?>;

						rev1 = review_html_part2 + review_img1 + review_html_part3 + review_name1 + review_html_part4 + review_review1 + review_html_part5
					}

					if (num_of_reviews>=3) {
						review_name2 = (<?php echo json_encode($review_name2) ?>);
						review_img2 = <?php echo json_encode($review_img2) ?>;
						review_review2 = <?php echo json_encode($review_review2) ?>;

						rev2 = review_html_part2 + review_img2 + review_html_part3 + review_name2 + review_html_part4 + review_review2 + review_html_part5
					}

					if (num_of_reviews>=4) {
						review_name3 = <?php echo json_encode($review_name3) ?>;
						review_img3 = <?php echo json_encode($review_img3) ?>;
						review_review3 = <?php echo json_encode($review_review3) ?>;

						rev3 = review_html_part2 + review_img3 + review_html_part3 + review_name3 + review_html_part4 + review_review3 + review_html_part5
					}

					if (num_of_reviews>=5) {
						review_name4 = <?php echo json_encode($review_name4) ?>;
						review_img4 = <?php echo json_encode($review_img4) ?>;
						review_review4 = <?php echo json_encode($review_review4) ?>;

						rev4 = review_html_part2 + review_img4 + review_html_part3 + review_name4 + decodeURIComponent(review_html_part4) + review_review4 + review_html_part5
					}


					var review_rows = rev + rev0 + rev1 + rev2 + rev3 + rev4;


					var num_of_photos = <?php echo $photos_max ?>;

					var photo = "";
					var photo0 = "";
					var photo1 = "";
					var photo2 = "";
					var photo3 = "";
					var photo4 = "";

					if (num_of_photos == 0) {

						photo = "<tr><td style='padding: 3px;'>No Photos Available</td></tr>";

					}


					if (num_of_photos >= 1) {

						photo0 = review_html_part72 + 'img0.jpg' + review_html_part8 + 'img0.jpg' + review_html_part9;

					}


					if (num_of_photos >= 2) {

						photo1 = review_html_part72 + 'img1.jpg' + review_html_part8 + 'img1.jpg' + review_html_part9;

					}

					if (num_of_photos >= 3) {

						photo2 = review_html_part72 + 'img2.jpg' + review_html_part8 + 'img2.jpg' + review_html_part9;

					}

					if (num_of_photos >= 4) {

						photo3 = review_html_part72 + 'img3.jpg' + review_html_part8 + 'img3.jpg' + review_html_part9;

					}

					if (num_of_photos >= 5) {

						photo4 = review_html_part72 + 'img4.jpg' + review_html_part8 + 'img4.jpg' + review_html_part9;

					}

					var photos_rows = photo + photo0 + photo1+ photo2 + photo3 + photo4;



					reviews_html_code = review_html_start + review_html_place_name + review_html_part1 + review_rows + review_html_part6 + photos_rows + review_html_part10;

					document.getElementById('reviews-go-here').innerHTML = reviews_html_code;


				}



        	}



        	function getReviews(place_id_js) {
        		document.getElementById('place_id').value = place_id_js;
        		// console.log('here');
        		// window.alert(place_id_js);
        		// document.getElementById('category').value = 'cafe';
        		document.getElementById('submit_type').value = 'js_submit';

        		var form_js = document.getElementById('form');
        		form_js.submit();

        	}

        	function test_submit(){

        		form_js = document.getElementById('form');
        		// form_js.submit();
        		document.TheForm.submit();
        	}


        	function escapeHtml(text) {
				  var map = {
				    '&': '&amp;',
				    '<': '&lt;',
				    '>': '&gt;',
				    '"': '&quot;',
				    "'": '&#039;'
				  };

				  return text.replace(/[&<>"']/g, function(m) { return map[m]; });
				}


		</script>


		<script type="text/javascript">

			function reviewsTableOn() {
				// console.log('test');
				document.getElementById('reviews-table').style.display = 'block';
				document.getElementById('reviews-up-arrow').style.display = 'block';
				document.getElementById('reviews-down-arrow').style.display = 'none';
				photosTableOff();

			}

			function reviewsTableOff() {
				document.getElementById('reviews-table').style.display = 'none';
				document.getElementById('reviews-up-arrow').style.display = 'none';
				document.getElementById('reviews-down-arrow').style.display = 'block';
				
			}

			function photosTableOn() {
				document.getElementById('photos-table').style.display = 'block';
				document.getElementById('photos-up-arrow').style.display = 'block';
				document.getElementById('photos-down-arrow').style.display = 'none';
				reviewsTableOff();
			}

			function photosTableOff() {
				document.getElementById('photos-table').style.display = 'none';
				document.getElementById('photos-up-arrow').style.display = 'none';
				document.getElementById('photos-down-arrow').style.display = 'block';
			}

		</script>


		<!-- MAPS thing -->

		<script async defer
			src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCpDWvlkvrxDf9XfCA0-g0auNMOFop51FU&">
		</script>


		<script type="text/javascript">
					
			document.addEventListener('click', printMousePos, true);

			var cursorX, cursorY;

			function printMousePos(e){
			    cursorX = e.pageX;
			    cursorY= e.pageY;
			    console.log(cursorX + " " + cursorY);
			    // e.preventDefault();
			}



			function movemap() {
				// console.log('here');
			 //    console.log(cursorX + " " + cursorY);
				document.getElementById('map-and-modes').style.top = (cursorY+5) + 'px';
				document.getElementById('map-and-modes').style.left = cursorX + 'px';

			}



		</script>


		<script type="text/javascript">

			var directionsDisplay;
			var directionsService;
			var lat_targets = 0;
			var lon_targets = 0;
			
			function initMap(lat_target, lon_target) {
				// console.log(lat_target, lon_target);
				lat_targets = lat_target;
				lon_targets = lon_target;
				uluru = {lat: lat_target, lng: lon_target}
				directionsDisplay = new google.maps.DirectionsRenderer;
				directionsService = new google.maps.DirectionsService;
				var map = new google.maps.Map(document.getElementById('map'), {
					zoom: 14,
				    center: {lat: lat_target, lng: lon_target}
				});
				var marker = new google.maps.Marker({
			    	position: uluru,
			    	map: map
			  	});
				directionsDisplay.setMap(map);

				if (document.getElementById('modes-list-div').style.display == "block") {

					document.getElementById('modes-list-div').style.display = "none";
					document.getElementById('map-and-modes').style.display = "none";

				} else {
					
					document.getElementById('modes-list-div').style.display = "block";
					document.getElementById('map-and-modes').style.display = "block";
				}

			  // calculateAndDisplayRoute(directionsService, directionsDisplay);
			  // document.getElementById('mode').addEventListener('change', function() {
			  //   calculateAndDisplayRoute(directionsService, directionsDisplay);
			  // });
			}

			function calculateAndDisplayRoute(directionsService, directionsDisplay, mode) {
			  var selectedMode = mode;
			  lat_start = <?php echo $lat ?>;
			  lon_start = <?php echo $lon ?>;
			  directionsService.route({
			    origin: {lat: lat_start, lng: lon_start},  // Haight.
			    destination: {lat: lat_targets, lng: lon_targets},  // Ocean Beach.
			    // Note that Javascript allows us to access the constant
			    // using square brackets and a string value as its
			    // "property."
			    travelMode: google.maps.TravelMode[selectedMode]
			  }, function(response, status) {
			    if (status == 'OK') {
			      directionsDisplay.setDirections(response);
			    } else {
			      window.alert('Directions request failed due to ' + status);
			    }
			  });
			}

		</script>

		<!-- //////////////////////////////////     JS DONE      ////////////////////////////////// -->

	</body>
</html>
