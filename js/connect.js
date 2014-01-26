/****************************************************************/
//ファイル読み込み
/****************************************************************/
function loadFile(){
	loadData("char");
}

function loadData(flg){
	var $url;
	var dd= new Date();
	switch(flg){
	case "char":
		$url=$charText;
		break;
	case "rule":
		$url=$ruleText;
		break;
	case "data":
		$url=$dataText+"?"+dd.getMinutes()+dd.getSeconds();
	}
	$("#board").css({"background-image":"url(../rooper/img/load.png)"});

	$.ajax({
		url:$url,
		dataType:'csv',
		success:function(result){loadDataAfter(result,flg)	}
	});

}
/*=====================================================*/
//データ読み込み後処理
function loadDataAfter(result,flg){
	//データ解析
	var datarr=result.split("\n");//改行で分割
	for(var i=0;i<datarr.length;i++){
		if(datarr[i].indexOf("http://")!=-1){
			datarr[i]=datarr[i].replace(/http:\/\//g,"@@");
		}
		if(datarr[i].indexOf("//")!=-1){
			var tmp=datarr[i].split("//");
			datarr[i]=tmp[0];
		}
		datarr[i]=jQuery.trim(datarr[i]);//空白除去
		var tmp = datarr[i].replace(/</g,"&lt;");
		tmp = tmp.replace(/>/g,"&gt;");
		tmp = tmp.replace(/\\n/g,"<br>");
		if(tmp=="")continue;
		switch(flg){
			case "char":
				makeChar(tmp);
				break;
			case "rule":
				makeRule(tmp);
				break;
			case "data":
				update(tmp);
				break;
			default:
		}
	}
	$("#board").css({"background-image":"url("+$BOARDPATH+")"});
	if(custom==10&&$ExCounter==0)$("#board").css({"background-image":"url("+$ANOTHERBOATDPATH+")"});//anotherhorizon表世界裏世界

	if(flg=="rule"){
		makeListTable();//test();
		loadData('data');
	}
	if(flg=="char"){
		loadData("rule");
		for(var i=0;i<charlist.length;i++){
			charimg.push(defcharimg[i]);
		}
		for(var i=0;i<4;i++){
			charimg.push(boardimg[i]);
		}
	}
	if(flg=="data"){

	}
}


/*======================================================*/

/****************************************************************/
//ファイル描き込み
/****************************************************************/

//書き込みリスト作製
function makeQuery(){
	var query="";
	//----------------------------------------------
	var charnum=charlist.length;//2013.07.04.add
	for(var i=0;i<charnum;i++){
		query+="char"+"@"+i+"@"+
				charlist[i].nownum
			  +","+charlist[i].nowpos
			  +","+charlist[i].nextnum
			  +","+charlist[i].nextpos
			  +","+charlist[i].anyaku
			  +","+charlist[i].huan
			  +","+charlist[i].yuko
			  +","+charlist[i].x
			  +","+charlist[i].y
			  +","+charlist[i].kill;

		//↓↓ミステリーサークル
			if(custom==8||custom==5){//2013.07.04.add
				query+=","+charlist[i].kashi;
			}
		//↑↑ミステリサークル
		//↓↓幻想用
			if(custom>=6&&i==19){
				if(custom!=8)query+=","+0;//仮死フラグ用データ分
				query+=","+charlist[i].remove;
			}
			
		//↑↑幻想用2013.11.09
		//↓↓ホーンテッドステージ
			if((custom==9||custom==4)&&i>=(charnum-3)&&i<charnum){//2013.07.04.add
				query+=","+charlist[i].kaihou;
			}
		//↑↑ホーンテッドステージ
			query+="&";	
	}
	//-----------------------------------------------
	for(var i=0;i<$HERONUM;i++){
		switch(handlist[i].card){
			case 0:
				handlist[i].anyaku=1;
				break;
			case 1:
				handlist[i].yuko_plus_2=1;
				break;
			case 2:
				handlist[i].idou_kinsi=1;
				break;
			case 3:
				handlist[i].huan_minus_1_pl=1;
				break;
		}
		query+="plhand"+"@"+i+"@"
			  +handlist[i].card
			  +","+handlist[i].char
			  +","+handlist[i].x
			  +","+handlist[i].y
			  +","+handlist[i].order
			  +","+handlist[i].nextorder
			  +","+handlist[i].anyaku
			  +","+handlist[i].yuko_plus_2
			  +","+handlist[i].idou_kinsi
			  +","+handlist[i].huan_minus_1_pl;
		query+="&";
	}
	for(var i=$HERONUM;i<$PLAYNUM;i++){
		switch(handlist[i].card){
			case "0":
				handlist[i].idou_naname=1;
				break;
			case "1":
				handlist[i].anyaku_plus_2=1;
				break;
		}
		query+="gmhand"+"@"+i+"@"
			  +handlist[i].card
			  +","+handlist[i].char
			  +","+handlist[i].x
			  +","+handlist[i].y
			  +","+handlist[i].idou_naname
			  +","+handlist[i].anyaku_plus_2;
		query+="&";
	}
	for(var i=0;i<boards.length;i++){
		query+="board"+"@"+i+"@"
			 +boards[i].anyaku+"&";
	}
	query+="scenario"+"@"+$sheetopen+"&";
	query+="excounter"+"@"+$ExCounter+"&";
	if(custom==10)query += 'rumor'+"@"+rumor+'&';//2013.11.10.anotherhorizon
	//phaseより後にデータを足すとエラー（updateでphaseで終わりの処理を行う）
	query+="phase"+"@"+phase.nextloop
	+","+phase.nextday+","+phase.nextphase;
	return query;
}
//書き込み本体
function createRequest(){
	var httplist=[
		function(){return new XMLHttpRequest();},
		function(){return new ActiveXObject("Msxml2.XMLHTTP");},
		function(){return new ActiveXObject("Microsoft.XMLHTTP");}
	];
	for(var i=0;i<httplist.length;i++){
		try{
			var http = httplist[i]();
			if(http != null){return http;}
		}catch(e){ continue;}
	}
	return null;
}

function dofunc(){
	var HTTP=createRequest();
	if(HTTP==null){
		alert("HTTP通信ができませんでした");
		return;
	}
	HTTP.open("POST","./save.cgi",true);
	HTTP.setRequestHeader("User-Agent","XMLHttpRequest");
	HTTP.onreadystatechange=function(){
		if(HTTP.readyState==4 && HTTP.status==200){
			callbackFunc(HTTP.responseText);
		}
	}
	//書き込みファイル作製
	var query=makeQuery();
	HTTP.send(query);
	return false;
}
function callbackFunc(result){}
