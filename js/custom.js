
var header="<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EM\"   \"http://www.w3.org/TR/html4/loose.dtd\"><html LANG=\"ja-JP\"><head><meta http-equi\"Content-Type\" content=\"text/html\;charset=EUC-JP\"><meta http-equiv=\"Content-Script-Type\" content=\"text/javascript\"><meta http-equiv=\"Content-Style-Type\" content=\"text/css\"><link rel=\"stylesheet\" type=\"text/css\" href=\"rooper.css\"><title>オリジナルセット</title></head><body style=\"overflow-x:hidden\">";
var footer="</body></html>";


function customform($filename,$type){
	if($filename=="board.png"){
		var cgi="./customboard.cgi";
	}else{
		var cgi="./custom.cgi";
	}
var form="<form method='post' action='"+cgi+"' ENCTYPE='multipart/form-data'>ファイル選択： <input type='file' name='upload_file'size='30'><input type='submit' value='アップロード'><input type='hidden' name='filename' value='"+$filename+"'><input type='hidden' name='filetype' value='"+$type+"'></form>";
	subwin = window.open("sub.html","sub","width=320,height=240,scrollbars=1");
	subwin.document.open();
	subwin.document.write(header);
	subwin.document.write(form);
	subwin.document.write(footer);
	subwin.document.close();
	subwin.blur();
	subwin.focus();
	
}
/****************************************************************/
//ファイル読み込み
/****************************************************************/
function loadData(filename){
	$.ajax({
		url:"custom/"+filename,
		dataType:'csv',
		success:function(result){loadDataAfter(result,filename)	}
	});

}
/*=====================================================*/
//データ読み込み後処理
function loadDataAfter(result,filename){
	//データ解析
	var datarr=result.split("\n");//改行で分割
	var cnt=0;
	for(var i=0;i<datarr.length;i++){
		if(datarr[i].indexOf("//")!=-1){
			var tmp=datarr[i].split("//");
			datarr[i]=tmp[0];
		}
		datarr[i]=jQuery.trim(datarr[i]);//空白除去
		var tmp = datarr[i].replace(/</g,"&lt;");
		tmp = tmp.replace(/>/g,"&gt;");
		tmp = tmp.replace(/\\n/g,"<br>");
		if(tmp=="")continue;
		if(filename=="char.csv"){
			makeChar(tmp,cnt);
		}else if(filename=="rule.csv"){
			makeRule(tmp)
		}
		cnt++;
	}
	if(filename=="char.csv"){
		window.opener.document.getElementById("charnum").value=cnt;
		for(var i=cnt;i<13;i++){
			window.opener.document.getElementById("chartr"+i).style.display="none";
		}
	}

}

function makeChar(dat,cnt){
	var chararr=dat.split(",");//,で分割
		//名前を定義
	window.opener.document.getElementById("customcharnameprev"+cnt).innerHTML=chararr[0];
	window.opener.document.getElementById("customcharname"+cnt).value=chararr[0];
}


function makeRule(dat){
	var tmparr=dat.split(",");//,で分割
	switch(tmparr[0]){
	case "boards":
		for(var i=0;i<4;i++){
			window.opener.document.getElementById("customboardprev"+i).innerHTML=tmparr[i+1];
			window.opener.document.getElementById("customboard"+i).value=tmparr[i+1];
		}
		break;
	}

}
