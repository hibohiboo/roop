function allhide(){
	$('#gameboard').hide();
	$('#RuleList').hide();
	$('#RoleList').hide();
	$('#CharList').hide();
}
function changeboard(name){
	allhide();
	$(name).show();
}
function changepanel(name){
	$(name).toggle();
}
/****************************************************************************/
//表示／非表示
var tgl=new Array();//1:visible 0:hidden
tgl['writer']=1;
function toggle(name){
	if(tgl[name]){
		document.getElementById(name).style.display="none";
		tgl[name]=0;
	}else{
		document.getElementById(name).style.display="block";
		tgl[name]=1;
	}
}

function viewCloseSheet(){
	window.open("scenario/close.htm","closesheet");
}
function viewOpenSheet(){
	window.open("scenario/open.htm","opensheet");
}
function OpenSheet(){
	$sheetopen=1;
	var query=makeQuery();
	$.post('./save.cgi',query,
		function(){
		});
}
