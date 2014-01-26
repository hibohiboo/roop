var prev_card_flg="gm";

function nextPhase(){
	switch(phase.phase){
		case 1:
		case 2:
		case 3:
		case 4:
		case 7:
		case 8:
		case 9:
		case 10:
		case 11:
		case 12:
		case 13:
		case 14:
		case 15:
			setswitch();
			break;
		case 5://2013.06.20.add
			setswitch();
			var query="mode=phase5&"+"loop="+phase.loop+"&day="+phase.day;
			$.post($SYSTEMCGI,query,function(){});
			break;
		case 6:
			if(handlist[3].card==-1||handlist[3].char==-1
				||handlist[4].card==-1||handlist[4].char==-1
				||handlist[5].card==-1||handlist[5].char==-1){
				alert("カードを３枚ボードにセットしてください");
				return;
			}
			setswitch();//2013.06.17.add
			var query="mode=phase6&"
					 +"char3="+handlist[3].char+"&"+"hand3="+handlist[3].card+"&"
					 +"char4="+handlist[4].char+"&"+"hand4="+handlist[4].card+"&"
					 +"char5="+handlist[5].char+"&"+"hand5="+handlist[5].card
					 +"&custom="+custom+"&hero=writer";
			if(custom==10){if($("#leaderskip").attr("checked")){
				query+="&leaderskip=true";
				phase.nextphase=7;
				$("#leaderskip").attr({"checked":false});//リーダースキップ初期化
			}}
			$.post($SYSTEMCGI,query,function(){});
			break;
	}
	nextPhaseLast();
}


function phasecheck(){
	if(phase.loop<phase.nextloop)phase.loop=phase.nextloop;
	if(phase.phase==16){phase.phase=4;}
	if(phase.day==phase.nextday&&phase.phase>=phase.nextphase)return;//巻き戻り防止。
	if(phase.nextphase==phase.phase&&phase.day==0)return;
	if(phase.phase<5&&phase.nextphase>=5)phase.phase=4;
	phase.phase++;//フェイズを進める。
	disp.show(["#closesheet",'#nextphasebutton']);
	switch(phase.phase){
		case 0:
			autoupdate(0);$("#uptime").attr('disabled',true);//自動更新一時停止。再開→autoupdate(updateTime);
			disp.hide(["#updatebutton","#nextloopbutton",".gmform"]);
			disp.show(["#openclosesheet","#resetgame"]);
			break;
		case 1://カウンターの除去と配置
				if(custom>=6){//χでは時の狭間
				}else{
					counter_remove_set();
				}
			break;
		case 2://キャラクターの配置
				if(custom>=6){//χではカウンターの配置
					usechar_check();
					counter_remove_set();
				}else{
					charcter_position_set();
				}
			break;
		case 3://手札の配布
				if(custom>=6){//χではキャラクターの配置
					charcter_position_set();
				}else{
					hand_set();
				}
			break;
		case 4://時の狭間
				if(custom>=6){//χでは手札の配布
					hand_set();
				}
			break;
		case 5://ターン開始時処理
			disp.hideUpdate();//2013.11.24.add
			phase.day-=(-1);
			reversehand();//2013.11.09.delete
			$("#day").text(phase.day);
			$("#writer").hide();
			disp.show(["#control","#nextloopbutton","#writerbutton"]);
			break;
		case 6://脚本家行動フェイズ
			disp.hideUpdate();//2013.11.24.add
			disp.hide(["#updatebutton",'#control']);
			disp.show([".gmform","#nextloopbutton","#writerbutton","#writer","#toggleHandCon"]);
			break;
		case 7://主人公行動フェイズ１
		disp.showUpdate();//2013.11.24.add
			disp.hide(['#nextloopbutton','#toggleHandCon','#nextphasebutton','#writer','#writerbutton','.gmform','#nextloopbutton']);
			break;
		case 8://主人公行動フェイズ２
			disp.showUpdate();//2013.11.24.add
			disp.hide(['#writer','#writerbutton','.gmform','#nextphasebutton']);
			break;
		case 9://主人公行動フェイズ３
			disp.showUpdate();//2013.11.24.add
			disp.hide(['#writer','#writerbutton','.gmform','#nextphasebutton']);
			break;
		case 10://行動解決フェイズ
			disp.hideUpdate();//2013.11.24.add
			openhand();
			moveOpenHand();
			disp.show(['#nextphasebutton','#writerbutton','#writer','#control','#refbutton']);
			$('.gmform').hide();
			break;
		case 11://脚本家能力使用フェイズ
			disp.hideUpdate();//2013.11.24.add
			chartablecontrol();
			if(phase.nextphase>10)reclaimhand();//手札回収
			disp.show(['#writerbutton','#writer','#control',"#nextloopbutton"]);
			$("#refbutton").hide();
			break;
		case 12://主人公能力使用フェイズ
			disp.hideUpdate();//2013.11.24.add
			if(phase.nextphase>10)reclaimhand();//手札回収
			disp.show(['#writerbutton','#writer','#control',"#nextloopbutton"]);
			if(custom!=1 && charlist[7].yuko>=3){$("#dischargetext").show();}
			chartablecontrol();
			break;
		case 13://事件フェイズ
			disp.hideUpdate();//2013.11.24.add
			if(phase.nextphase>10)reclaimhand();//手札回収
			chartablecontrol();
			if(custom!=1 && charlist[7].yuko>=3)$("#dischargetext").hide();
			disp.show(['#writerbutton','#writer','#control','#nextloopbutton']);
			break;
		case 14://リーダー交代フェイズ
			disp.hideUpdate();//2013.11.24.add
			if(phase.nextphase>10)reclaimhand();//手札回収
			if(phase.nextphase>14)break;//2012.5.5追記。
			disp.show(['#writerbutton','#control','#nextloopbutton']);
			disp.hide(['#writer','#countbutton']);
			for(var i=0;i<3;i++){
				handlist[i].order=handlist[i].nextorder;
				handlist[i].nextorder--;
				if(handlist[i].nextorder==-1)handlist[i].nextorder=2;
				checkleader(i);
			}
			break;
		case 15://ターン終了フェイズ
			disp.hideUpdate();//2013.11.24.add
			if(phase.nextphase>10){reclaimhand();}//手札回収
			disp.show(['#writerbutton','#writer','#nextloopbutton','#control']);
			break;
		case 16:
			phasecheck();
			break;
	}
	phaseCheckLast();
}
	


/***************************************************************/
//クッキーにセーブ
function saveCookie(){
	var query=makeQuery();
	var theName="RoopeRdata";
//60日間有効なクッキーを設定
	var expire = new Date();
	expire.setTime(expire.getTime() + (60 * 24 * 60 * 60 * 1000));
	document.cookie=theName
					+ "="+query
					+'; expires=' + expire.toGMTString(); //60日間のクッキーセット
	alert("クッキーにボードデータを保存しました\n\n※脚本は保存されません");
}
/***************************************************************/
//クッキーからロード
function loadCookie(){
	var theData="";
	var theName="RoopeRdata=";
	var theCookie=document.cookie+";";
	var start = theCookie.indexOf(theName);
	if(start!=-1){
		var end=theCookie.indexOf(";",start);
		theData=unescape(theCookie.substring(start+theName.length,end));
	}else{
	//読み込めなかったら終了
		alert("クッキーにデータがありません");
		return;
	}
	var answer=confirm("クッキーからボードデータをロードします。\n本当によいですか？");
　	if(answer==true){
　	}else{
　　	return;
　　}
	//再構築
	var query=theData;
	
	$.post($SAVECGI,query,
		function(){
			window.location.reload();
		});
}
/*********************************************************************/
//add.2013.5.18
function counter_remove_set(){
	autoupdate(0);//自動更新一時停止。再開→autoupdate(updateTime);
	resetcounter();
	disp.show(['#writerbutton','#writer','#control','#nextloopbutton']);
	disp.hide(['#resetgame','#openclosesheet','#nextloopbutton']);
	//$("#writer").show();$("#writerbutton").show();$('#control').show();
	//$("#resetgame").hide();$("#openclosesheet").hide();$("#nextloopbutton2").hide();

}
function charcter_position_set(){
	autoupdate(0);//自動更新一時停止。再開→autoupdate(updateTime);
	chartablecontrol();
	setdefpos();
	disp.show(["#writer","#writerbutton"]);
	$("#countbutton").hide();
	if(custom!=1)$("#dischargetext").show();
}
function hand_set(){
	autoupdate(0);//自動更新一時停止。再開→autoupdate(updateTime);
	chartablecontrol();
	//$("#writer").hide();$("#writerbutton").hide();$('#control').hide();
	disp.hide(['#writerbutton','#writer','#control']);
	if(custom!=1)$("#dischargetext").hide();
	resethand();
}
