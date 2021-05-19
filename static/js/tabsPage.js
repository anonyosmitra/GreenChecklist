function tabsPage_init(){
    onEnter({"div":"mainSearchBox","fun":"search","keyD":"moveClearButton"})
    init_enters();
    console.log("tabsPage.js loaded.")
    POST({"tab":"Country"},"openTab")
}
function tabsPage_openTab(tabName){
    tabs=["Country","Region","State","City"];
    if((tabs.includes(tabName))&&(tabName!=cache["tabName"]))
        POST({"tab":tabName},"openTab")
}
var getApp = new XMLHttpRequest();
    getApp.onreadystatechange = function () {
	if (this.readyState == 4 && this.status == 200) {
	var data = JSON.parse(this.response)["reply"];
	console.log(data);
	if(data["auth"]===1)
	{
	if(keyInJson('exe',data))
		{
			for(var i=0;i<data['exe'].length;i++)
			{
				methods[data['exe'][i]["method"]](data['exe'][i]['arg']);
			}
			}}

			else
			{
				console.log("Auth Failed");
			}
		}}
var methods={}
function selTab(args)
{
    fillProfile("");
    tabs=["Country","Region","State","City"];
 if(tabs.includes(args))
 {

    for(i in tabs)
        document.getElementById("tab_"+tabs[i]).classList.remove('highlight');
    document.getElementById("tab_"+args).classList.add('highlight');
    cache["tabName"]=args
 }
}
function fillTable(args)
{
    document.getElementById("tabEntries").innerHTML=args;
    document.getElementById("mainFrame").scrollIntoView()
}
function search(args=null)
{
    query={}
    if(args==null)
        query=document.getElementById("mainSearchBox").value;
    else
        if(cache["keys"].includes(args))
            query[args]=document.getElementById("search_"+args).value;
    if(query!={})
        POST({"tab":cache["tabName"],"query":query},"search")
}
function moveClearButton(args=null)
{
    clBut=document.getElementById("clear");
    if(document.getElementById("mainSearchBox").value=="")
        clBut.hidden=true;
    else
        clBut.hidden=false;
}
function makeOnEnters(args){
    cache["keys"]=args
    for(i in args)
     onEnter({"div":"search_"+cache["keys"][i],"fun":"search","arg":cache["keys"][i]})
}
function fillProfile(args){
    document.getElementById("profileTab").innerHTML=args;
    document.getElementById("mainFrame").scrollIntoView()
}
function onEnter(arg)
{
    var div = document.getElementById(arg["div"]);

	div.addEventListener("keyup", function(event) {
 	event.preventDefault();
 	if (event.keyCode === 13) {
 		if("arg" in arg)
    		methods[arg["fun"]](arg["arg"]);
    	else
    	{
    		methods[arg["fun"]]();}}
		else if("keyD" in arg){
			if("arg" in arg)
    		    methods[arg["keyD"]](arg["arg"]);
    		else
    			methods[arg["keyD"]]();}})};
function cacheToken(args)
{
    cache["token"]=args;
}
function cacheProfileFields(args)
{
    cache["profileFields"]=args;
}
function setSelOpts(args)
{
    for(i in args)
        document.getElementById("profile_"+args[i]["var"]).innerHTML=args[i]["html"];
}
function profileError(arg)
{
   ele=document.getElementById("profileErrorMsg");
   ele.innerHTML=arg;
   ele.hidden=false;
}
methods=Object.assign(methods,{"selTab":selTab,"fillTable":fillTable,"search":search,"moveClearButton":moveClearButton,"onEnter":onEnter,"makeOnEnters":makeOnEnters,"fillProfile":fillProfile})
methods=Object.assign(methods,{"cacheProfileFields":cacheProfileFields,"setSelOpts":setSelOpts,"cacheToken":cacheToken,"profileError":profileError})
function POST(data,route="")
	{
		getApp.open('POST',"http://3.7.72.90/"+route);
		getApp.setRequestHeader("Content-Type","application/json;charset=UTF-8");
		getApp.send(JSON.stringify(data))
	}
function keyInJson(k,json)
	{
		for(var i in json)
		{
		    if(i===k)
				return(true);
			}
			return(false);
		}
function loadProfile(id)
    {
        POST({"tab":cache["tabName"],"id":id},"loadProfile");
    }
function loadProfileEditor(id)
    {
        POST({"tab":cache["tabName"],"id":id,"edit":1},"loadProfile");
    }
function updateSelOpt(variable)
    {
        if(variable!="timezone")
            POST({"tab":cache["tabName"],"var":variable,"val":document.getElementById("profile_"+variable).value},"UpdateSelOpts");
    }
function addNew()
    {
        POST({"tab":cache["tabName"]},"addNew");
    }
function submitForm(id)
    {
        console.log(cache["token"])
        data={"token":cache["token"],"id":id,"tab":cache["tabName"],"form":{}}
        for(i in cache["profileFields"])
            data["form"][cache["profileFields"][i]]=document.getElementById("profile_"+cache["profileFields"][i]).value
        if(id==0)
            POST(data,"addNew");
        else
            POST(data,"saveEdit");
    }
function deleteEntry(id)
    {
        POST({"id":id,"tab":cache["tabName"],"token":cache["token"]},"deleteEntry");
    }
function clearSearchBar()
{
    document.getElementById("mainSearchBox").value="";
    document.getElementById("clear").hidden=true;
}