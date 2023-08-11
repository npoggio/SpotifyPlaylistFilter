function functionName(trackData) {

	// Decode html-encoded json
	var decodedData = decodeEntities(trackData);

	// Parse json str into object
	var jsonData = JSON.parse(decodedData);

	for ( var i = 0; i < Object.keys(jsonData).length; i++) {
	document.getElementById("test").innerHTML+= jsonData[i][1];
	console.log(jsonData[i][1]); 
	}
}

function decodeEntities(encodedString) {
    var textarea = document.createElement('textarea');
    textarea.innerHTML = encodedString;
    return textarea.value; 
}
