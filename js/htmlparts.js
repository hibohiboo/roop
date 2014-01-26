
function makeListTable(){
	ruleTable();
	roleTable();
	CharTable();
	setChar();
	controleTable();

	for(var i=0;i<$HERONUM;i++){
		makehandTable(i,"pl");
	}
	for(var i=$HERONUM;i<$PLAYNUM;i++){
		makehandTable(i,"gm");
	}
	//↓↓アナザーホライゾン
	//手札フォーム
	if(custom==10){
		var div= $(document.createElement("div"))
				.attr({'id':'rumordiv'})
				.css({"float":"left","class":"gmform","width":"100px","height":"40px","border":"solid 1px #ffffff","margin":"3px","padding":"2px"})
				.text("噂話カード");
		var select= $(document.createElement("select"))
				.attr({'name' :"rumor",'id':'rumor'})
				.change(function(){	
					rumor=$("#rumor").val();
					checkrumor();
				});
			select.append($(document.createElement("option"))
					.attr({"value":-1})
					.text("選択しない")
					);
		for(var cnt=0;cnt<boards.length;cnt++){
		var option =$(document.createElement("option"))
					.attr({"value":cnt})
					.text(boards[cnt].name);
			select.append(option);
		}
		div.append(select);
		$("#writer").append(div);
		//gameboard上手札
		var card=$(document.createElement("div"))
				.css({"display":"none","z-index":"3",'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+"rumor.png"+")",'position':"absolute"})//,'top':($CARDMARGIN-(-i)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':$CARDMARGIN+"px"});
				.attr({"id":"rumorcard"});
		$("#board").append(card);
		//行動カードのセット禁止
		$("#tableLeaderSkip").text("リーダーの行動カードセット禁止")
		.append(
			$(document.createElement('input'))
			.attr({"id":"leaderskip",'type':'checkbox'})
		);
	}
	//↑↑アナザーホライゾン
	var $input=$(document.createElement("input"));
	$input.attr({"type":"button","id":"toggleHandCon","class":"gmform"})
		.val("手札／\nキャラ管理\n切り替え")
		.css({"display":"none"})
		.click(function(){
		if($("#writer").css("display")=="none")return;//2013/11/10 追記
		$("#gmhandform3").toggle();
		$("#gmhandform4").toggle();
		$("#gmhandform5").toggle();
		//2012/11/10 追記↓
		$("#nextloopbutton2").toggle();
		//2012/11/10 追記↑
		$("#control").toggle();
	});
	//$("#writer").append($input); 2013.11.08.delete
	$("#left").append($input);//2013.11.08.add
	//HauntedStage
	if(custom==4||custom==9){//2013.07.04.add
		$("#toggleHandCon").css({"top":"620px"});
	}
	//↑↑HauntedStage

	/*************************************/
	/*2013.11.08.delete
	//↓20121110追加↓
		var button = $(document.createElement("input"));
	button.attr({"type":"button","value":"ループを終える","id":"nextloopbutton2"});
	button.css({"margin-left":"40px","margin-top":"20px"});
	button.click(function(){nextloop()});
	button.css({"display":"none"});
	$("#writer").append(button);
	//↑20121110追加↑
	*/
	/****************************************/
	//if(custom==0||custom==1){//製品版のカードとパラメータ表示
		 makebottomprev();
	//}
	clickselectcharacard();
//↓↓ファーストステップ以降//2013.07.04.add
	if(custom>=6){
		var timerID = setTimeout(function(){usechar_check();clearTimeout(timerID);}, 1000);
	}
//↑↑ファースト・ステップ
	setDisplayCache();//2013.11.08.add
}

/*==========================================================*/
//ルールX・Yテーブル
/*=========================================================*/
function ruleTable(){
	var $waku = document.getElementById("waku");
	var $table = document.createElement("table");
	//テーブル名、テーブル、行の数、列の数
	$table.id="RuleList";
	makeRuletr("RuleList",$table);
	$waku.appendChild($table);
}

function makeRuletr(name,table){
	for(var i=-1;i<ruleY.length+ruleX.length;i++){
		var tr=document.createElement("tr");
		tr.id = name+'x'+i;
		table.appendChild(tr);
		//td
		makeRuletd(name,i,tr);
	}
}
function makeRuletd(name,i,tr){
	//td作成
	for(var j=-1;j<ruleHEAD.length;j++){
		var td=document.createElement("td");
		//左端
		if(j==-1){
			td.id=name+'x'+i+'y'+j;
			td.style.fontSize="300%";
			td.style.textAlign="center";
			if(i==0){
				td.innerHTML="R<br>u<br>l<br>e<br>Y";
				td.rowSpan=ruleY.length;
				tr.appendChild(td);
			}
			if(i==ruleY.length){
				td.innerHTML="R<br>u<br>l<br>e<br>X";
				td.rowSpan=ruleX.length;
				tr.appendChild(td);
			}
			if(i==-1){
				var td=document.createElement("th");
				td.id=name+"sumi";
				td.innerHTML="";
				tr.appendChild(td);
			}
			continue;
		}else{
			//最上段
			if(i==-1){
				var td=document.createElement("th");
				td.id=name+i+j;
				if(j!=-1)td.innerHTML=ruleHEAD[j];
			}else{
				td.id=name+'x'+i+'y'+j;
				var tmp=ruleY[i];
				if(i>=ruleY.length)
					var tmp=ruleX[i-ruleY.length];
				switch(j){
				case 0:
					td.innerHTML=tmp.name;
					break;
				case 1:
					tr.appendChild(td);
					if(tmp.role[0]==""){
						td.innerHTML=tmp.role;
						continue;
					}
					var ul=document.createElement("ul");
					ul.className="intable";
					td.appendChild(ul);
					for(var cnt=0;cnt<tmp.role.length;cnt++){
						var li=document.createElement("li");
						li.innerHTML=tmp.role[cnt];
						ul.appendChild(li);
					}
					continue;
					break;
				case 2:
					td.innerHTML=tmp.rule;
				}
			}
		}
	tr.appendChild(td);
	}
}
/*==========================================================*/
//役職テーブル
/*=========================================================*/
function roleTable(){
	var $waku = document.getElementById("waku");
	var $table = document.createElement("table");
	//テーブル名、テーブル、行の数、列の数
	$table.id="RoleList";
	makeRoletr("RoleList:",$table);
	$waku.appendChild($table);
}

function makeRoletr(name,table){
	for(var i=-1;i<roleList.length;i++){
		var tr=document.createElement("tr");
		tr.id = name+'x'+i;
		table.appendChild(tr);
		//td
		makeRoletd(name,i,tr);
	}
}

function makeRoletd(name,i,tr){
	//td作成
	for(var j=-1;j<roleHEAD.length;j++){
		var td=document.createElement("td");
		//左端
		if(j==-1){
			if(i==0){
				td.id=name+'x'+'y'+i;
			td.style.fontSize="300%";
			td.style.textAlign="center";
				td.innerHTML="C<br>h<br>a<br>r<br>a<br>c<br>t<br>e<br>r<br>R<br>o<br>l<br>e";
				td.rowSpan=roleList.length;
				tr.appendChild(td);
			}
			if(i==-1){
				var td=document.createElement("th");
				td.id=name+"sumi";
				td.innerHTML="";
				tr.appendChild(td);
			}
			continue;
		}else{
			//最上段
			if(i==-1){
				var td=document.createElement("th");
				td.id=name+'x'+i+'y'+j;
				if(j!=-1)td.innerHTML=roleHEAD[j];
			}else{
				td.id=name+i+j;
				switch(j){
				case 0:
					td.innerHTML=roleList[i].name;
					break;
				case 1:
					td.innerHTML=roleList[i].max;
					td.style.fontSize="130%";
					td.style.textAlign="center";
					break;
				case 2:
					if(roleList[i].yukomusi=="友好無視"){//2013.10.26.add
						td.innerHTML="<font color='#b0e0e8'>"+roleList[i].yukomusi+"</font>";
					}else if(roleList[i].yukomusi=="絶対友好無視"){
						td.innerHTML="<strong><font color='#b0e0e8'>"+roleList[i].yukomusi+"</font></strong>";
					}else if(roleList[i].yukomusi=="死後活性"){
						td.innerHTML="<font color='#ffff00'>"+roleList[i].yukomusi+"</font>";
					}else if(roleList[i].yukomusi=="友好暴発"){
						td.innerHTML="<font color='#ff4500'>"+roleList[i].yukomusi+"</font>";
					}else if(roleList[i].yukomusi=="表裏選択"){
						td.innerHTML="<font color='#00ff7f'>"+roleList[i].yukomusi+"</font>";
					}else{
						td.innerHTML=roleList[i].yukomusi;
					}
					td.style.textAlign="center";
					
					break;
				case 3:
					td.innerHTML=roleList[i].noryoku;
					break;
				case 4:
					tr.appendChild(td);
					if(roleList[i].rule[0]==""){
						td.innerHTML=roleList[i].rule;
						continue;
					}
					var ul=document.createElement("ul");
					ul.className="intable";
					td.appendChild(ul);
					for(var cnt=0;cnt<roleList[i].rule.length;cnt++){
						var li=document.createElement("li");
						li.innerHTML=roleList[i].rule[cnt];
						ul.appendChild(li);
					}
					continue;
					break;
				}
			}
		}
	tr.appendChild(td);
	}
}
/*==========================================================*/
//キャラクターテーブル
/*=========================================================*/
function CharTable(){
	var $waku = document.getElementById("waku");
	var $table = document.createElement("table");
	//テーブル名、テーブル、行の数、列の数
	$table.id="CharList";
	makeChartr("CharList",$table);
	$waku.appendChild($table);
}

function makeChartr(name,table){
	for(var i=-1;i<charlist.length;i++){
		var tr=document.createElement("tr");
		tr.id = name+'x'+i;
		table.appendChild(tr);
		//td
		makeChartd(name,i,tr);
	}
	//HauntedStage
	if(custom==4||custom==9){//2013.07.04.add
		$("#writer").css({"height":"700px"});
	}
	//↑↑HauntedStage
}

function makeChartd(name,i,tr){
	//head作成
	var charHEAD = new Array("","名前","不安臨界","初期位置","移動不可","属性","友好能力");
	//td作成
	for(var j=-1;j<charHEAD.length;j++){
		var td=document.createElement("td");
		//左端
		if(j==-1){
			if(i==0){
				td.id=name+'x'+i+'y'+j;
			td.style.fontSize="300%";
			td.style.textAlign="center";
				td.innerHTML="C<br>h<br>a<br>r<br>a<br>c<br>t<br>e<br>r<br>";
				td.rowSpan=charlist.length;
				tr.appendChild(td);
			}
			if(i==-1){
				var td=document.createElement("th");
				td.id=name+"sumi";
				td.innerHTML="";
				tr.appendChild(td);
			}
			continue;
		}else{
			//最上段
			if(i==-1){
				var td=document.createElement("th");
				td.id=name+'x'+i+'y'+j;
				if(j!=-1)td.innerHTML=charHEAD[j];
			}else{
				td.id=name+i+j;
				switch(j){
				case 0:
					$(td).append($(document.createElement("img")).attr({"src":$CHARPATH+defcharimg[i]}).css({"width":$CARDWIDTH+"px","height":$CARDHEIGHT+"px"}));
					break;
				case 1:
					td.innerHTML=charlist[i].name;
					break;
				case 2:
					td.innerHTML=charlist[i].huanrinkai;
					td.style.fontSize="130%";
					td.style.textAlign="center";
					break;
				case 3:
					td.innerHTML=charlist[i].defpos;
					td.style.textAlign="center";
					break;
				case 4:
					if(charlist[i].idouhuka=="")break;
					if(charlist[i].idouhuka.indexOf("+")==-1){
						$(td).append($(document.createElement("ul")).attr({"class":"intable"}).append($(document.createElement("li")).css({"width":"3em"}).text(charlist[i].idouhuka)));
						break;
					}
					var tmp=charlist[i].idouhuka.split("+");
					var ul=document.createElement("ul");
					ul.className="intable";
					td.appendChild(ul);
					for(var cnt=0;cnt<tmp.length;cnt++){
						var li=document.createElement("li");
						li.style.width="3em";
						li.innerHTML="<nobr>"+tmp[cnt]+"</nobr>";
						ul.appendChild(li);
					}
					break;
				case 5:
					if(charlist[i].zokusei.indexOf("+")==-1){
						$(td).append($(document.createElement("ul")).attr({"class":"intable"}).append($(document.createElement("li")).css({"width":"3em"}).text(charlist[i].zokusei)));
						break;
					}
					var zokusei=charlist[i].zokusei.split("+");
					var ul=document.createElement("ul");
					ul.className="intable";
					td.appendChild(ul);
					for(var cnt=0;cnt<zokusei.length;cnt++){
						var li=document.createElement("li");
						li.style.width="3em";
						li.innerHTML="<nobr>"+zokusei[cnt]+"</nobr>";
						ul.appendChild(li);
					}
					break;
				case 6:
					tr.appendChild(td);
					if(charlist[i].hituyoyuko[0]==""){
						td.innerHTML="";
						continue;
					}
					var ul=document.createElement("ul");
					ul.className="intable";
					td.appendChild(ul);
					for(var cnt=0;cnt<charlist[i].hituyoyuko.length;cnt++){
						var li=document.createElement("li");
						li.id="char"+i+"yuko"+cnt;
						if(charlist[i].hituyoyuko[cnt]=="0"){
							var yuko="特性";
						}else{
							var yuko="友好"+charlist[i].hituyoyuko[cnt];
						}
						li.innerHTML=yuko+"："+charlist[i].yukonoryoku[cnt]+"";
						ul.appendChild(li);
					}
					continue;
					break;
				}
			}
		}
	tr.appendChild(td);
	}

}
