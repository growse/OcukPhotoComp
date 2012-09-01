var photocomp = function() {
	return {
		selectImage: function(id,seasonname,roundtheme,score,personname) {
			var imageurl = "http://ocukimages1.growse.com/";
       		var caption = roundtheme +"("+seasonname+") - Score: "+score;
       		var fullcaption = "<a href=\"/rounds/"+seasonname+"/"+roundtheme+"/#"+personname+"\">"+roundtheme+" ("+seasonname+")</a> - Score: "+score;
       		$('#selected img').attr("src",imageurl+id+"_MEDIUM.jpg");
	        $('#selected img').attr("alt",caption);
	        $('#selected a').attr("href",imageurl+id+"_FULL.jpg");
	        $('#selected a').attr("title",caption);
	        $('#selectedcaption').html(fullcaption);
		}
	};
}();

