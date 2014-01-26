var phase = new function(){
	this.loop=1;
	this.nextloop=1;
	this.day=0;
	this.nextday=1;
	this.phase=-1;
	this.nextphase=0;
}


function setphaseHTML(){
	$("#right").append($(document.createElement("img")).attr({"src":$PHASEIMG,"id":"phaseimg"}));
	$tmp=$(document.createElement("div"));
	$tmp.attr({"id":"loopbox"})
	$tmp.html("Loop:"+"<span id='loop'>1</span>");
	$("#right").append($tmp);
	$tmp=$(document.createElement("div"));
	$tmp.attr({"id":"daybox"})
	$tmp.html("Day:"+"<span id='day'>0</span>");
	$("#right").append($tmp);
}
function nextPhaseSetHeroCard(NUM_hero,NUM_phase){
//	switch(NUM_phase){case 7:	var order=0;break;case 8:	var order=1;break;case 9:	var order=2;break;}
	for(var i=0;i<3;i++){
		if(handlist[i].order==(NUM_phase-7)){
			var tmp=i;
			break;
		}
	}
	if(handlist[tmp].card==-1||handlist[tmp].char==-1){
		alert("カードをボードにセットしてください");
		return -1;
	}
	if(NUM_phase==9){
		var query="mode=phase9&"
					+"char0="+handlist[0].char+"&"+"hand0="+handlist[0].card+"&"
					+"char1="+handlist[1].char+"&"+"hand1="+handlist[1].card+"&"
					+"char2="+handlist[2].char+"&"+"hand2="+handlist[2].card+"&"
					+"char3="+handlist[3].char+"&"+"hand3="+handlist[3].card+"&"
					+"char4="+handlist[4].char+"&"+"hand4="+handlist[4].card+"&"
					+"char5="+handlist[5].char+"&"+"hand5="+handlist[5].card
					+"&custom="+custom+"&hero="+NUM_hero;

	}else{
		var query="mode=phase"+NUM_phase+"&"
					+"char="+handlist[tmp].char
					+"&custom="+custom+"&hero="+NUM_hero;
	}
	$.post($SYSTEMCGI,query,function(){});
	//2013.11.12.add
	$('#prevhandpl'+NUM_hero).css({"background-image":"url("+$HANDPATH+"Unselected.png"+")"});
	$('#plhand'+tmp+"card"+handlist[tmp].card).attr({"checked":false});

}

function nextPhaseLast(){
	phase.nextphase++;
	if(phase.nextphase==16){
		phase.nextphase=5;
		phase.nextday++;
	}
	var query=makeQuery();
	$.post($SAVECGI,query,function(){});
	var x= -160;
	x -= 160*(phase.phase);
	$("#phaseimg").animate({"top":25,"left":x},1000);
	phasecheck();
}
function phaseHeroAction(NUM_hero,order){
	if(NUM_hero==3)return;
	if(order==3){disp.showUpdate();selectchar_check=-1;disp.hide(["#plhandform0","#plhandform1","#plhandform2"]);}
	for(var i=0;i<3;i++){
		if(order!=0&& handlist[i].order==(order-1) && i==NUM_hero ||order!=0&& handlist[i].order==(order-1)&& NUM_hero==4){
			if(NUM_hero!=4)disp.showUpdate();//2013.11.24.add
			disp.hide(["#plhandform"+i]);
			if(NUM_hero!=4||order==3){
				disp.showUpdate();
				selectchar_check=-1;
			}
		}
		if(handlist[i].order==order && i==NUM_hero ||handlist[i].order==order&& NUM_hero==4){
			disp.hideUpdate();
			disp.show(["#plhandform"+i]);
			selectchar_check=i;
		}
	}
}

function phaseCheckLast(){
	//データの反映
	setcounter();//カウンター配置
	sethandpos();//手札配置
	setpos();//キャラクター位置設定
	for(var i=0;i<charlist.length;i++)killchar(i);//死亡判定
	$("#day").text(phase.day);
	$("#loop").text(phase.loop);
	if(phase.phase==16)return;
	var x = -160;
	x -= 160*(phase.phase);
	$("#phaseimg").animate({"top":25,"left":x},1000);
	if(phase.phase>16||phase.day>20){
		phase.phase=5;
		phase.day=20;
		alert("エラーが起こりました。読み込みなおしてください");
		return;
	}

	if(phase.nextday-phase.day>1)phase.day=phase.nextday;//入り直し対策
	if(phase.day<phase.nextday||phase.phase<phase.nextphase){//2013.12.3.change
		phasecheck();//日付とフェーズとループが同じになるまで繰り返す
	}else{
		phase.nextday=phase.day;
		phase.nextphase=phase.phase;
	}
}


function nextloop(){
	if(prev_card_flg=='gm'&&phase.loop!=0){
	　	var answer=confirm("ループを終了させます。よろしいですか？");
　		if(answer==true){
		}else{alert("キャンセルしました");return;}
		$.post($SYSTEMCGI,"mode=loopend&loop="+phase.loop,function(){});//2013.11.18.add
	}

	phase.loop-=(-1);
	if(prev_card_flg=='gm')phase.nextloop-=(-1);
	$("#loop").text(phase.loop);
	phase.day=0;
	phase.nextday=1;
	$("#day").text(phase.day);
	phase.phase=-1;
	phase.nextphase=0;
	resethand();//手札リセット
	phasecheck();
	$("#writer").hide();
	$("#writerbutton").hide();
	
	var query=makeQuery();
	$.post($SAVECGI,query,
		function(){
			phasecheck();
		});
	
	var x= -160;
	x   -= 160*(phase.phase);
	$("#phaseimg").animate({"top":25,"left":x},5000);


}
function resetphase(){
	phase.loop=0;
	phase.nextloop=0;
	$("#loop").text(phase.day);
	phase.day=0;
	phase.nextday=1;
	$("#day").text(phase.day);
	phase.phase=-1;
	phase.nextphase=0;
	phasecheck();
	$("#writer").hide();
	$("#writerbutton").hide();
	for(var i=0;i<3;i++){
		handlist[i].order=i;
		handlist[i].nextorder=i-1;
		if(i==0)handlist[i].nextorder=2;
	}
	$sheetopen=0;//シート公開設定
	nextloop();
}

var Display = function() {}; //Constructorだけ定義
Display.prototype.hide=function(target){//methodを定義
	var N=target.length;
	for(var i=0;i<N;i++){
		this.cache[target[i]].hide();
	}
};
Display.prototype.show=function(target){//methodを定義
	var N=target.length;
	for(var i=0;i<N;i++){
		this.cache[target[i]].show();
	}
};
function setDisplayCache(){//DOM構築後にキャッシュ
	Display.prototype.cache={
				"#closesheet":$("#closesheet"),
				"#updatebutton":$("#updatebutton"),
				"#nextloopbutton":$("#nextloopbutton"),
				".gmform":$(".gmform"),
				'#nextphasebutton':$('#nextphasebutton'),
				"#openclosesheet":$("#openclosesheet"),
				"#resetgame":$("#resetgame"),
				"#control":$("#control"),
				"#writerbutton":$("#writerbutton"),
				"#writer":$("#writer"),
				"#toggleHandCon":$("#toggleHandCon"),
				'#refbutton':$('#refbutton'),
				"#dischargetext":$("#dischargetext"),
				'#countbutton':$('#countbutton'),
				"#plhandform0":$("#plhandform0"),
				"#plhandform1":$("#plhandform1"),
				"#plhandform2":$("#plhandform2"),
				"#uptime": $("#uptime")
				//propertyを定義
	};
	disp=new Display();//オブジェクト生成
}
Display.prototype.hideUpdate=function(){//methodを定義
		//disp.hide(['#updatebutton']);
		this.cache['#updatebutton'].hide();
		this.cache['#nextphasebutton'].show();
		autoupdate(0);this.cache["#uptime"].attr('disabled',true);//自動更新一時停止。再開→autoupdate(updateTime);
};
Display.prototype.showUpdate=function(){//methodを定義
		this.cache['#updatebutton'].show();
		this.cache['#nextphasebutton'].hide();
		autoupdate(updateTime);//自動更新再開
		this.cache["#uptime"].attr('disabled',false);
};