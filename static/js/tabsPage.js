function tabsPage_init(){
    onEnter({"div":"mainSearchBox","fun":"search","keyD":"moveClearButton"})
    init_enters();
    console.log("tabsPage.js loaded.")
}
function tabsPage_openTab(tabName){
    console.log(tabName);
}
var getApp = new XMLHttpRequest();
    getApp.onreadystatechange = function () {
	if (this.readyState == 4 && this.status == 200) {
	var data = JSON.parse(this.response)["reply"];
	console.log(data);
	if(data["auth"]===1)
	{
	if(keyInJson('exe',data["reply"]))
		{
			for(var i=0;i<data["reply"]['exe'].length;i++)
			{
				methods[data["reply"]['exe'][i]["method"]](data["reply"]['exe'][i]['arg']);
			}
			}}

			else
			{
				console.log("reload page");
			}
		}}
var methods={}
function selTab(args)
{
    tabs=["Country","State","City"];
 if(args in tabs)
 {
    for(i in tabs)
        document.getElementById("tab_"+tabs[i]).style="tabButton";
    document.getElementById("tab_"+args).style="tabButton highlight";
 }
}
function fillTable(args)
{
    document.getElementById("tabEntries").innerHTML=args;
}
function search(args=null)
{
    query={}
    if(args==null)
        query=document.getElementById("mainSearchBox").value;
    else
        if(args in cache["keys"])
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
methods=Object.assign(methods,{"selTab":selTab,"fillTable":fillTable,"search":search,"moveClearButton":moveClearButton,"onEnter":onEnter,"makeOnEnters":makeOnEnters})
function POST(data,route="")
	{
		getApp.open('POST',"http://3.7.72.90/"+route);
		getApp.setRequestHeader("Content-Type","application/json;charset=UTF-8");
		getApp.send(JSON.stringify(data))
	}