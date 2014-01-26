//ExCounter
$ExCounter=0;
//キャラクターリスト
/*======================================================*/
function makeChar(dat){
		var chararr=dat.split(",");//,で分割
		//キャラクターデータ作成。
		var tmpobj = new function(){
			this.name=chararr[0];//名前を定義
			this.huanrinkai=chararr[1];//不安臨界を定義
			this.defpos    =chararr[2];//初期位置を定義
			this.nownum    =0;//現在位置のi
			this.nowpos    =0;//現在位置(boards[i].pos[j])
			this.nextnum=0;
			this.nextpos=0;
			this.idouhuka  =chararr[3];//移動禁止ボードを定義
			this.zokusei   =chararr[4];//属性を定義
			//必要友好を定義
			if(chararr[5]){
				var tmp = chararr[5].split("+");
				this.hituyoyuko = tmp;
			}else{this.hituyoyuko=new Array("");}
			//友好能力を定義
			if(chararr[6]){
				var tmp = chararr[6].split("+");
				this.yukonoryoku=tmp;
			}else{this.yukonoryoku=new Array("");}

			//共通
			this.y=0;
			this.x=0;
			this.anyaku=0;
			this.huan=0;
			this.yuko=0;
			this.card=0;//カード登録領域
			this.kill=0;//死亡確認
			//カスタム専用URL定義。orファーストステップ2013.5.18.add
			if(custom==1&&chararr[7]||custom>=6&&chararr[7]){//2013.07.27.add
				chararr[7]=chararr[7].replace(/\@\@/g,"//");
				this.url=chararr[7];
			}
		//↓↓ホーンテッドステージ
			if(custom==4||custom==9){//2013.07.03.add
				this.kaihou=0;//魔獣解放確認
			}
		//↑↑ホーンテッドステージ
		//↓↓ミステリー・サークル
			if(custom==5||custom==8){//2013.07.03.add
				this.kashi=0;//仮死確認
			}
		//↑↑ミステリーサークル
		//↓↓幻想用
			if(custom>=6&&i==19){
				this.remove=0;//除外確認
			}
		//↑↑幻想用2013.11.09
		}
		charlist.push(tmpobj);
}

//killしたら入力できないようにする。
function formdisabled(name,num){
	name="#"+name;
	if($(name).attr('checked')){
		charlist[num].kill=1;
		var tmp=$(document.createElement("img"));
		tmp.attr({"src":"../rooper/img/x.png","alt":"x","id":"kill"+num});
		tmp.css({'position':"absolute",'top':"0px",'left':"0px",'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
		$("#char"+num).append(tmp);
		//HauntedStageでは死体にもカードをおける
		if(!(custom==4||custom==9)){//2013.07.03.add
		for(var i=1;i<=4;i++){
			$(name+'n'+i).attr({'disabled':true});
		}
		}
	}else{
		$("#kill"+num).remove();
		for(var i=1;i<=4;i++){
			$(name+'n'+i).attr({'disabled':false});
		}
		//charlist[num].kill=0;
	}
	//↓↓ミステリー//2013.07.03.add
	if(custom==5||custom==8){//mystery circle 仮死チェック
		if($("#con"+num+"n5").attr('checked')){
			charlist[num].kashi=1;
			var tmp=$(document.createElement("img"));
			tmp.attr({"src":"../rooper/img/hand/exA.png","alt":"x","id":"kashi"+num});
			tmp.css({'position':"absolute",'top':"20px",'left':"15px",'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
			$("#char"+num).append(tmp).css({"overflow":"visible"});
		}else{
			$("#kashi"+num).remove();
		}
	}
	//↑↑ここまでミステリー
}
//killしたら入力できないようにする。チェック時用
function checkformdisabled(name,num){
	name="#"+name;
	if($(name).attr('checked')){
		charlist[num].kill=1;
		var tmp=$(document.createElement("img"));
		tmp.attr({"src":"../rooper/img/x.png","alt":"x","id":"kill"+num});
		tmp.css({'position':"absolute",'top':"0px",'left':"0px",'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
		$("#char"+num).append(tmp);
		for(var i=1;i<=4;i++){
			//HauntedStageでは死体にもカードをおける
			if(!(custom==4||custom==9)){//2013.07.03.add
				$(name+'n'+i).attr({'disabled':true});
			}
		}
	}else{
		$("#kill"+num).remove();
		
		for(var i=1;i<=4;i++){
			$(name+'n'+i).attr({'disabled':false});
		}
		charlist[num].kill=0;
	}
	//↓↓
	/*
	if(custom==5){//mystery circle 仮死チェック
		if($("#con"+num+"n5").attr('checked')){
			charlist[num].kashi=1;
			var tmp=$(document.createElement("img"));
			tmp.attr({"src":"../rooper/img/hand/exA.png","alt":"x","id":"kashi"+num});
			tmp.css({'position':"absolute",'top':"20px",'left':"15px",'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
			$("#char"+num).append(tmp).css({"overflow":"visible"});
		}else{
			$("#kashi"+num).remove();
			charlist[num].kashi=0;
		}
	}
	*/
	//↑↑ここまでミステリーサークル
}



//killを反映(update)
function killchar(i){
	$("#kill"+i).remove();//一旦消してから作成
	if(charlist[i].kill==1){
		var tmp=$(document.createElement("img"));
		tmp.attr({"src":"../rooper/img/x.png","alt":"x","id":"kill"+i});
		tmp.css({'position':"absolute",'top':"0px",'left':"0px",'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
		$("#char"+i).append(tmp);
	}
}
/*-------------------------------------------------------*/
/*キャラクター作成*/
function setChar(){
	var charnum=charlist.length;//2013.07.03.add
	for(var i=0;i<charnum;i++){
		var div = document.createElement("div");
		div.style.display="block";
		div.className="charcard";
		div.id="char"+i;
		div.style.backgroundImage="url("+$CHARPATH+charimg[i]+")";
		var $board = document.getElementById("board");
		$board.appendChild(div);
//↓↓ホーンテッドステージ
		if((custom==9||custom==4)&&i>=(charnum-3)&&i<charnum){//2013.07.03.add
			div.style.display="none";
		}
//↑↑ホーンテッドステージ
	}

	//ボードも作成
	for(var i=0;i<boards.length;i++){
		var div = document.createElement("div");
		div.style.display="block";
		div.className="charcard";
		var tmp=charlist.length-(-i);
		div.id="char"+tmp;
		div.style.left=boards[i].x+"px";
		div.style.top=boards[i].y+"px";
		div.style.backgroundImage="url("+$CHARPATH+charimg[i+charlist.length]+")";
		var $board = document.getElementById("board");
		$board.appendChild(div);
	}
}
//初期位置設定----------------------
function setdefpos(){
	for(var i=0;i<boards.length;i++){
		for(var j=0;j<charlist.length;j++){
			boards[i].pos[j].space=0;
		}
	}
	for(var i=0;i<charlist.length;i++){
		if(charlist[i].nownum==5){continue;}//2013.5.18.add
		setCharPos(charlist[i]);
		$("#char"+i).css({"left":charlist[i].x+"px","top":charlist[i].y+"px"});
		$('#con'+i+'n1').val(charlist[i].nownum);
		charlist[i].nextpos=charlist[i].nowpos;
		charlist[i].nextnum=charlist[i].nownum;
	}
}

//----------------------------------
function setCharPos(char){
	for(var i=0;i<boards.length;i++){
		if(char.defpos==boards[i].name){
			for(var j=0;j<charlist.length;j++){
				if(boards[i].pos[j].space==0){
					char.x=boards[i].pos[j].x;
					char.y=boards[i].pos[j].y;
					boards[i].pos[j].space=1;
					char.nowpos=j;
					char.nownum=i;
					return;
				}
			}
		}
	}
}

/*==========================================================*/
//コントロールパネル
/*=========================================================*/
function controleTable(){
	var $waku = $("#writer");
	var $form = $(document.createElement("form"));
	$form.attr({"name":"control",'id':"control"});
	$waku.append($form);
	var $table = $(document.createElement("table"));
	//テーブル名
	$table.attr({"id":"Controltable"});
	$table.css({"position":"absolute","top":"30px","left":"5px"});
	makecontroletr("con",$table);
	var button = $(document.createElement("input"));
	button.attr({"type":"button","value":"移動セット","id":"movebutton","class":"writerbutton"});
	button.css({"display":"none"});
	button.click(function(){charmove()});
	$form.append(button);

//
	var button = $(document.createElement("input"));
	button.attr({"type":"button","value":"カウンターセット","id":"countbutton","class":"writerbutton"});
	button.click(function(){getcounter();$("#writer").hide();});
	button.css({"display":"none"});
	$form.append(button);
//	$form.append($table);
//
	var button = $(document.createElement("input"));
	button.attr({"type":"button","value":"プレビュー","id":"setbutton"});
	button.click(function(){setswitch()});
	//button.css({"display":"block","position":"absolute"}); 2013.11.08.delete
	$form.append(button); //2013.11.08
	//var left=$("#left");//2013.11.08.add
	//left.append(button);//2013.11.08.add
//	$form.append($table);
//
	var button = $(document.createElement("input"))
		.attr({"type":"button","value":"ループを終える","id":"nextloopbutton","class":"writerbutton"})
		.click(function(){nextloop()})
		.css({"display":"none"});
	//$form.append(button); 2013.11.08.delete
	$("#tableLoopEnd").append(button);//2013.11.08 add

	var button = $(document.createElement("input"))
		.attr({"type":"button","value":"手札反映","id":"refbutton"})
		.click(function(){cardEffect()})
	//button.css({"display":"none","position":"absolute","left":"100px"}); 2013.11.08.delete
		.css({"display":"none"});//2013.11.08.add
	$form.append(button);
//	$form.append($table);
	$form.append($table);
	//Excounter作成
	$table.append($(document.createElement("tr")).attr({"id":"ExCounter"}));
	var Ex=$("#ExCounter");
	Ex.append($(document.createElement("td")))
		.append($(document.createElement("td")).text("Exカウンター").attr({"id":"td_ExCounter"}))
		.append($(document.createElement("td")).append($(document.createElement("input")).attr({"size":"2","name":"ExCon","id":"ExCon","value":"0","class":"number"})));
	var tmp=$(document.createElement("td")).attr({"colspan":"4"});
	if(custom!=1){tmp.html("<span id='dischargetext' style='display:none;'>患者退院。<input type='checkbox' id='discharge'></span>");}
	Ex.append(tmp);
	//幻想用2013.11.09
	if(custom>=6){
		$table.append(
			$(document.createElement("tr")).attr({"id":"fantasy"})
			.append($(document.createElement("td")))
			.append($(document.createElement("td")).text("幻想をボードから取り除く。").attr({"colspan":"4"})
			.append($(document.createElement("input"))
			.attr({"type":"checkbox","name":"fantasyRemove","id":"fantasyRemove"}))
			.click(function(){
				if($("#fantasyRemove").attr('checked')){
					charlist[19].remove=1;
				}else{
					charlist[19].remove=0;
				}
				checkformFantasy(charlist[19].remove);
			})
			)
			.append($(document.createElement("td")))
		);
	}
}



//行動セットを押したときにキャラクターを動かしてカウンターをセットする。手札は回収。
function setswitch(){
	charmove();
	getcounter();
	for(var i=0;i<$PLAYNUM;i++){
		$("#hand"+i).hide();
	}
//	reclaimhand();
	$("#writer").hide();
//	医者友好能力用
	if(custom!=1 && $("#con7n2").val()>=3||custom==10&&$("#con7n3").val()>=3&&$ExCounter==0){$("#dischargetext").show();}
//キャラテーブルプレビュー
	chartablecontrolprev();
}

function makecontroletr(name,table){
	for(var i=-1;i<charlist.length+boards.length;i++){
		var tr=$(document.createElement("tr")).attr({"id":"control_tr_"+i});//2013.5.17.add
		table.append(tr);
		//td
		makecontroletd(name,i,tr);
	}


}

function makecontroletd(name,i,tr){
	var charnum=charlist.length;//2013.07.04
	//td作成
	var head = new Array("キャラ","移動","友好","不安","暗躍");
	//HauntedStage
	if(custom==4 || custom==9){//2013.07.03.add
		head[5]="解放";
	}
	//↑↑HauntedStage
	//↓↓ミステリーサークル
	if(custom==5||custom==8){//2013.07.03.add
		head[5]="仮死";
	}
	//↑↑ミステリーサークル
	var headlen=head.length;//2013.07.04
	//alert(headlen);
	for(var j=-1;j<headlen;j++){
		var td=$(document.createElement("td"));
		//左端
		if(j==-1){
			if(i==-1){
				var td=$(document.createElement("th"));
				td.attr({"id":name+"sumi"});
				td.text("kill");
			}else if(i!=-1&&i<charlist.length){
				var input= $(document.createElement("input"));
				input.attr({'type':"checkbox",'id':name+i,'id':name+i,'checked':false});//input.attr({'type':"checkbox",'id':name+i,'checked':false});
				input.click(function(){checkformdisabled(name+i,i)});
				td.append(input);
			}
		}else{
			//最上段
			if(i==-1){
				var td=$(document.createElement("th"));
				td.attr({"id":name+i+j});
				if(j!=-1)td.text(head[j]);
			}else{
				//td.id=name+i+j;
				switch(j){
				case 0:
					if(i<charnum){
						td.text(charlist[i].name);

				}	else{
						td.text(boards[i-charlist.length].name);
					}
					break;
				case 1:
					if(i>=charlist.length)break;
					var select= $(document.createElement("select"));
					select.attr({'name' :name+i+'n'+j,'id':name+i+'n'+j});
					select.attr({"disabled":false});
					select.change(function(){setnext(i,select.attr('id'))});
					td.append(select);
					for(var cnt=0;cnt<boards.length;cnt++){
						var option =$(document.createElement("option"));
						option.attr({"value":boards[cnt].name});
						option.text(boards[cnt].name);
						option.val(cnt);
						select.append(option);
					}
					select.val(charlist[i].nownum);
					break;
				case 2:
				case 3:
				if(i>=charnum)break;
				case 4:
					var input = $(document.createElement("input"));
					input.attr({'size':"2",'name':name+i+'n'+j,'id':name+i+"n"+j,'value':"0",'class':"number",'disabled':false});
					//↓↓2013.06.17.add
					input.keydown(function(event){

						//var m = String.fromCharCode(event.keyCode);
						//if("0123456789\b".indexOf(m, 0) < 0) return false;
						//0-9,←→,backspace,delet,insert以外は入力不可
						switch(event.keyCode){
							case 48: case 49: case 50: case 51: case 52:case 53:case 54:case 55: case 56:case 57:
							case 45:case 46:case 36: case 37:case 38:case 39:case 8:
							case 96:case 97:case 98: case 99:case 100:case 101:case 102:case 103:case 104:case 105:
								break;
							default:return false;
						}
						return true;
					})
					.blur(function(){
						if(this.value==""){this.value=0;}
					});
					//↑↑2013.06.17.add
					td.append(input);
					break;
				case 5:
					//HauntedStage
				if(custom==4 || custom==9){//2013.07.03.add
					if(i>=(charnum-3) && i<charnum){
						var input= $(document.createElement("input"));
						input.attr({'type':"checkbox",'id':name+i,'id':name+i+"n"+j,'checked':false});
						input.data({"i":i});
						input.click(function(){checkformMonster($(this).data("i"))});
					td.append(input);
					}
				}
					//↑↑HauntedStage
					//↓↓ミステリーサークル
				if(custom==5||custom==8){//2013.07.03.add
					if(i<charnum+1){
						var input= $(document.createElement("input"));
						input.attr({'type':"radio","name":"kashi",'id':name+i,'id':name+i+"n"+j,'checked':false});
						input.data({"i":i});
						input.click(function(){checkformdisabledkashi(name+$(this).data("i"),$(this).data("i"))});
					td.append(input);
					}
				}
					//↑↑ミステリーサークル
					break;
				}
			}
		}
	if((i%3)==0){
		td.css({"background-color":"#440000"});
	}else if(i%3==1){
		td.css({"background-color":"#000044"});
	}else{
		td.css({"background-color":"#000000"});
	}
	tr.append(td);
	}
}


//========================================================================================================
//次の移動先を選ぶ。
function setnext(i,id){
	var val=$('#'+id + ' option:selected').val();
	if(custom!=1&&$("#discharge").attr('checked')&&i==8){//患者が退院していた場合。
		charlist[i].nextnum=val;
		return;
	}
	if(charlist[i].idouhuka.indexOf(boards[val].name)!=-1){
	　　var answer=confirm(charlist[i].name+"は"+boards[val].name+"に本来行くことができません。\n本当によいですか？");
　		　if(answer==true){
　		　	//alert(charlist[i].name+"は"+boards[val].name+"に移動します");
　	　	}else{
　	　		alert(charlist[i].name+"の"+boards[val].name+"への移動をキャンセルしました");
　	　		$('#con'+i+'n1').val(charlist[i].nownum);
　		　return;
　		}
　　}
	charlist[i].nextnum=val;
}
//--------------------------------------------
//キャラクター場所設定
//--------------------------------------------
function setpos(){
	for(var i=0;i<charlist.length;i++){
		$("#char"+i).css({"left":charlist[i].x+"px","top":charlist[i].y+"px"});
		$('#con'+i+'n1').val(charlist[i].nownum);
		var now=charlist[i].nownum;
		var pos=charlist[i].nowpos;
		if(now==5){continue;}//2013.5.20.add
		boards[now].pos[pos].space=1;
	}
}
//移動する======================================
function charmove(){
	//alert("!");
	for(var i=0;i<charlist.length;i++){
		var next = charlist[i].nextnum;
		var now = charlist[i].nownum;
		var nowpos=charlist[i].nowpos;
		if(next != now){
			for(var j=0;j<charlist.length;j++){
				if(now==5){continue;}//2013.5.25.add
				if(boards[next].pos[j].space==0){
					boards[now].pos[nowpos].space=0;
					$("#char"+i).animate({"top":boards[next].pos[j].y,"left":boards[next].pos[j].x},1000);
					charlist[i].x=boards[next].pos[j].x;
					charlist[i].y=boards[next].pos[j].y;
					charlist[i].nownum=next;
					charlist[i].nowpos=j;
					boards[next].pos[j].space=1;
					break;
				}
			}
		}
	}
}


/********************************************************************************************************/
//値を取得しボードに反映
function getcounter(){
	for(var i=0;i<charlist.length;i++){
		charlist[i].yuko=$("#con"+i+"n"+2).val();
		charlist[i].huan=$("#con"+i+"n"+3).val();
		charlist[i].anyaku=$("#con"+i+"n"+4).val();
		addcounter($("#char"+i),charlist[i].yuko,charlist[i].huan,charlist[i].anyaku,i);
	}
	for(var i=charlist.length;i<charlist.length+boards.length;i++){
		boards[i-charlist.length].anyaku=$("#con"+i+"n"+4).val();
		addanyaku($("#char"+i),boards[i-charlist.length],i);
	}
	$ExCounter=$("#ExCon").val();
	if(custom==10){if($ExCounter==0){
		$("#board").css({"background-image":"url("+$ANOTHERBOATDPATH+")"});//anotherhorizon表世界裏世界
	}else{
		$("#board").css({"background-image":"url("+$BOARDPATH+")"});
	}}
	$("#ExConPrev").text($ExCounter);
}
//---------------------------------------------
function addcounter(card,yuko,huan,anyaku,num){
	var txt="";
	//huan
	txt+="<span class='huan'>";
	if(huan<3){
		for(var i=0;i<huan;i++){
			txt+="●";
		}
	}else{
		txt+="　"+"<strong class='huanmoji'>"+huan+"</strong>";
	}
	txt+="</span><br>";
	//yuko
	txt+="<span class='yuko'>";
	if(yuko<3){
		for(var i=0;i<yuko;i++){
			txt+="●";
		}
	}else{
		txt+="　"+"<strong class='yukomoji'>"+yuko+"</strong>";
	}
	txt+="</span><br>";
	//anyaku
	txt+="<span class='anyaku'>";
	if(anyaku<3){
		for(var i=0;i<anyaku;i++){
			txt+="●";
		}
	}else{
		txt+="　"+"<strong class='anyakumoji'>"+anyaku+"</strong>";
	}
	txt+="</span>";
	card.html(txt);
	var name="con"+num;
	formdisabled(name,num);
}
//カウンターをセットする。
function setcounter(){
	for(var i=0;i<charlist.length;i++){
		$("#con"+i+"n"+2).val(charlist[i].yuko);
		$("#con"+i+"n"+3).val(charlist[i].huan);
		$("#con"+i+"n"+4).val(charlist[i].anyaku);
		addcounter($("#char"+i),charlist[i].yuko,charlist[i].huan,charlist[i].anyaku,i);
	}
	for(var i=charlist.length;i<charlist.length+boards.length;i++){
		$("#con"+i+"n"+4).val(boards[i-charlist.length].anyaku);
		addanyaku($("#char"+i),boards[i-charlist.length],i);
	}
	//Ex
	$("#ExCon").val($ExCounter);
	$("#ExConPrev").text($ExCounter);
}
function addanyaku(card,board,j){
	var txt="";
	txt+="<span class='anyaku'>";
	if(board.anyaku<3){
		for(var i=0;i<board.anyaku;i++){
			txt+="●";
		}
	}else{
		txt+=""+"<strong class='anyakumoji'>"+board.anyaku+"</strong>";
	}
	txt+="</span>";
	card.html(txt);
}

//値をリセットする
function resetcounter(){
	var charnum=charlist.length;//2013.07.04.add
	for(var i=0;i<charnum;i++){
		//キャラ復活
		$("#con"+i).attr({"checked":false})
		charlist[i].kill=0;
		$("#kill"+i).remove();
		//仮死解除↓↓
		if(custom==5||custom==8){//2013.07.03.add2014.01.16update
			$("#con"+i+"n5").attr({'checked':false});
			charlist[i].kashi=0;
			$("#kashi"+i).remove();
		}//↑↑
		//カウンターリセット
		charlist[i].yuko=0;
		$("#con"+i+"n"+2).val(0);
		charlist[i].huan=0;
		$("#con"+i+"n"+3).val(0);
		charlist[i].anyaku=0;
		$("#con"+i+"n"+4).val(0);
		addcounter($("#char"+i),0,0,0,i);
		resetchartablecontrol(i);
		//↓↓ホーンテッドステージ
		if((custom==9||custom==4)&&i>=(charnum-3)&&i<charnum){//2013.07.03.add
			charlist[i].kaihou=0;
			$("#con"+i+"n5").attr({'checked':false});
			checkformMonster(i);
		}
		//↑↑ホーンテッドステージ
	}
	//仮死解除↓↓
	if(custom==5||custom==8){//2013.07.03.add
		$("#con"+9+"n5").attr({'checked':false});
	}//↑↑
	for(var i=charnum;i<charnum+boards.length;i++){//2013.07,04.add
		boards[i-charlist.length].anyaku=0;
		$("#con"+i+"n"+4).val(0);
		addanyaku($("#char"+i),boards[i-charlist.length],i);
	}
	if(!(custom==4||custom==9||custom==10)){//2013.07.21.addホーンテッドはリセットしない。2013.11.08アナザーホライゾンもリセットしない
		$ExCounter=0;
	}
	if(custom==10&&phase.loop==1){//2013.11.08AnotherHorizon
		$ExCounter=1;
		$("#board").css({"background-image":"url("+$BOARDPATH+")"});
	}
	$("#ExCon").val($ExCounter);
	$("#ExConPrev").text($ExCounter);
	//患者再入院
	if(custom!=1){$("#discharge").attr({"checked":false});}
}
//キャラテーブルコントロール
function chartablecontrol(){
	var charnum=charlist.length;//2013.07,04.add
	for(var i=0;i< charnum;i++){
		//2013.11.08
		yukoCounterColor(i,charlist[i].yuko,charlist[i].huan);
		huanCounterColor(i,charlist[i].huan,charlist[i].yuko);
		killCounterColor(i,charlist[i].kill);
	}
}
function yukoCounterColor(i,yuko,huan){
	if(custom==10&&$ExCounter==0)
		yuko=huan;//2013.11.08.anotherhorizon
	for(var j=0,l=charlist[i].hituyoyuko.length;j<l;j++){
		if(yuko>=charlist[i].hituyoyuko[j]){
			$("#char"+i+"yuko"+j).css({"color":"yellow"});
		}else{
			$("#char"+i+"yuko"+j).css({"color":"#ffffff"});
		}
	}
}
function huanCounterColor(i,huan,yuko){
	if(custom==10&&$ExCounter==0)
		huan=yuko;//2013.11.08.anotherhorizon
	if(huan>=charlist[i].huanrinkai){
		$("#CharList"+i+"2").css({"color":"blue"});
	}else{
		$("#CharList"+i+"2").css({"color":"#ffffff"});
	}
}
function killCounterColor(i,kill){
	if(kill==1){
		$("#CharList"+i+"1").css({"color":"red"});
	}else{
		$("#CharList"+i+"1").css({"color":"#ffffff"});
	}
}
//プレビュー用キャラテーブルコントロール
function chartablecontrolprev(){
	var charnum=charlist.length;//2013.07,04.add
	for(var i=0;i<charnum;i++){
		//2013.11.08
		yukoCounterColor(i,$("#con"+i+"n2").val(),$("#con"+i+"n3").val());
		huanCounterColor(i,$("#con"+i+"n3").val(),$("#con"+i+"n2").val());
		killCounterColor(i,$("#con"+i).attr('checked'));
	}
}
function resetchartablecontrol(i){
	$("#char"+i+"yuko0").css({"color":"#ffffff"});
	if(charlist[i].hituyoyuko[1]){
			$("#char"+i+"yuko1").css({"color":"#ffffff"});
	}
	$("#CharList"+i+"2").css({"color":"#ffffff"});
	$("#CharList"+i+"1").css({"color":"#ffffff"});
}
/******************************************************************************************************/
//キャラクターカード表示
function makebottomprev(){
	//プレビュー画面作成
	$("#bottom").append($(document.createElement("ul")).attr({"id":"bottomprev","class":"float"}).css({'width':400+"px",'height':"50px",'top':"20px",'position':"absolute",'left':20+"px"}));
	//カード作成
	for(i=0;i<charlist.length;i++){
		$("#bottomprev").append($(document.createElement("li")).attr({"id":"bottomprev"+i,'class':""}).css({"background-image":"url('"+$CHARPATH+charimg[i]+"')",'height':"50px",'width':"35px","cursor":"pointer"}).data("i",i-(-1)).click(function(){
			var tmp = parseInt($(this).data("i"));
			if(custom==0 || custom==3 || custom==4|| custom==5){
				$("#bottomprevchar").css({"background-image":"url('../rooper/img/charcard/chara_cards_0"+tmp+"_00.png')"});
			}else if(custom==1&&charlist[tmp-1].url ||custom>=6){//カスタムorファーストステップ2013.5.18.add//2013.07.27.add
				$("#bottomprevchar").css({"background-image":"url('"+charlist[tmp-1].url+"')","background-repeat":"no-repeat"});
			}
			$("#bottomprevname").text(charlist[tmp-1].name);
			$("#bottomprevyuko").text(charlist[tmp-1].yuko);
			$("#bottomprevhuan").text(charlist[tmp-1].huan);
			$("#bottomprevanyaku").text(charlist[tmp-1].anyaku);
		})
		);
	}
	//キャラクターカード本体
	$("#bottom").append($(document.createElement("div")).attr({"id":"bottomprevchar",'class':""}).css({"background-image":"url('../rooper/img/charcard/chatemp.png')",'height':"526px",'width':"373px",'position':"absolute",'top':"80px",'left':20+"px"}));
	//↓↓HauntedStage or ファーストステップ2013.5.18.add
	if(custom==4 || custom>=6){//2013.07.03.add
		$("#bottomprevchar").css({"top":"140px"});

	}
	//↑↑HauntedStage
	//現在パラメータ
	$("#bottom").append($(document.createElement("div")).attr({"id":"bottomprevchar",'class':""}).css({'height':"8em",'width':"200px",'position':"absolute",'top':"80px",'left':410+"px",'border':"solid 2px","padding":"5px"}).html("<span id='bottomprevname'>パラメータ表示</span><hr>友好：<span id='bottomprevyuko'>"+""+"</span><hr>不安：<span id='bottomprevhuan'>"+""+"</span><hr>暗躍：<span id='bottomprevanyaku'>"+""+"</span>"));
}

/******************************************************************************************************/
//キャラクターカード表示

function usechar_check(){
	if(custom==6){
	$("#ExCon").hide();
	$("#td_ExCounter").text("");
	$("#prev_ExCounter").hide();
	}
	if(phase.nextphase<2 && phase.nextday<2 && phase.nextloop<2){return;}
	var dd= new Date();
	$.ajax({
		url:"dat/kaichar.dat?"+dd.getTime(),
		dataType:'csv',
		success:function(result){usechar_After(result);}
	});
}

function usechar_After(result){
	//データ解析
	var datarr=result.split("\n");//改行で分割
	var rowspan=CHARALLNUM;
	for(var i=0,l=datarr.length;i<l;i++){
		datarr[i]=jQuery.trim(datarr[i]);//空白除去
		var tmp = datarr[i].replace(/</g,"&lt;");
		tmp = tmp.replace(/>/g,"&gt;");
		tmp = tmp.replace(/\\n/g,"<br>");
		if(tmp=="")continue;
		var chararr=tmp.split(",");//,で分割
		if(!(chararr[1]=="on")){
		/*
				$("#bottomprev"+i).hide();
				$("#char"+i).hide();
				$("#control_tr_"+i).hide();
				$("#CharListx"+i).hide();
				$("#gmhand3opt"+i).hide();
				$("#gmhand4opt"+i).hide();
				$("#gmhand5opt"+i).hide();
				$("#plhand0opt"+i).hide();
				$("#plhand1opt"+i).hide();
				$("#plhand2opt"+i).hide();
				if(charlist[i].nownum != 5){
					boards[charlist[i].nownum].pos[charlist[i].nowpos].space=0;
					charlist[i].nownum=5;//現在位置のi
					charlist[i].nowpos=20;//現在位置(boards[i].pos[j])
					charlist[i].nextnum=5;
					charlist[i].nextpos=20;
				}*///2013.11.10.delete
				no_use_char_hide(i);//2013.11.10.add
				rowspan--;
		}
		if(i==12&&chararr[1]=="on"){
			if(parseInt(chararr[2])>phase.nextloop || phase.nextphase<2){
				no_use_char_hide(i);
				rowspan--;
			}else{
				sinkaku_show();
			}
		}
	}
	$("#CharListx0y-1").attr({"rowspan":rowspan});
}

function no_use_char_hide(number){
	$("#bottomprev"+number).hide();
	$("#char"+number).hide();
	$("#control_tr_"+number).hide();
	$("#CharListx"+number).hide();
	$("#gmhand3opt"+number).hide();
	$("#gmhand4opt"+number).hide();
	$("#gmhand5opt"+number).hide();
	$("#plhand0opt"+number).hide();
	$("#plhand1opt"+number).hide();
	$("#plhand2opt"+number).hide();
	if(charlist[number].nownum != 5){
		boards[charlist[number].nownum].pos[charlist[number].nowpos].space=0;
		charlist[number].nownum=5;//現在位置のi
		charlist[number].nowpos=20;//現在位置(boards[i].pos[j])
		charlist[number].nextnum=5;
		charlist[number].nextpos=20;
	}
	if(number==19){
		$("#fantasy").hide();//幻想能力用2013.11.10.add
		charlist[number].remove=1;
	}
}

function sinkaku_show(){
	$("#bottomprev"+12).show();
	$("#char"+12).show();
	$("#control_tr_"+12).show();
	$("#CharListx"+12).show();
	$("#gmhand3opt"+12).show();
	$("#gmhand4opt"+12).show();
	$("#gmhand5opt"+12).show();
	$("#plhand0opt"+12).show();
	$("#plhand1opt"+12).show();
	$("#plhand2opt"+12).show();
	charlist[12].nownum=2;//現在位置のi
	charlist[12].nowpos=2;//現在位置(boards[i].pos[j])
	charlist[12].nextnum=2;
	charlist[12].nextpos=2;
	boards[charlist[12].nownum].pos[charlist[12].nowpos].space=1;
}
/******************************************************************************************************/
//幻想用

function checkformFantasy(flg){
	var num=19;
	//if($("#fantasyRemove").attr('checked')){
	if(flg==0){
//		charlist[num].remove=1;
		$("#char"+num).show();
		/*
		$("#plhand0opt"+num).show();
		$("#plhand1opt"+num).show();
		$("#plhand2opt"+num).show();
		$("#gmhand3opt"+num).show();
		$("#gmhand4opt"+num).show();
		$("#gmhand5opt"+num).show();
		*/
	}else{
//		charlist[num].remove=0;
		$("#char"+num).hide();/*
		$("#plhand0opt"+num).hide();
		$("#plhand1opt"+num).hide();
		$("#plhand2opt"+num).hide();
		$("#gmhand3opt"+num).hide();
		$("#gmhand4opt"+num).hide();
		$("#gmhand5opt"+num).hide();*/
	}
		$("#plhand0opt"+num).hide();
		$("#plhand1opt"+num).hide();
		$("#plhand2opt"+num).hide();
		$("#gmhand3opt"+num).hide();
		$("#gmhand4opt"+num).hide();
		$("#gmhand5opt"+num).hide();
}
