var $PHASEIMG="../rooper/first/img/loopready.png";
var $CHARPATH="../rooper/first/img/character/";
var $HANDPATH="../rooper/first/img/hand/";
var $BOARDPATH="../rooper/img/board.png";
var $charText="../rooper/kai/Hauntedchar.csv";
var $ruleText="../rooper/HauntedStage/rule.csv";
var custom=9;


//キャラクター
var charlist = new Array();
var defcharimg=[];
var CHARALLNUM=20;
for(var i=0;i<CHARALLNUM;i++){
	defcharimg[i]="char"+i+".png";
}
defcharimg[CHARALLNUM]="wolf.png";
defcharimg[CHARALLNUM+1]="dragon.png";
defcharimg[CHARALLNUM+2]="dinasor.png";


//手札
var plhand = new Array("暗躍禁止","友好＋２","移動禁止","不安－１","移動↑↓","移動←→","友好＋１","不安＋１");
var plhandimg= new Array("anyaku_kinsi.png","yuko_plus_2.png","idou_kinsi.png","huan_minus_1_pl.png","idou_ue_sita.png","idou_hidari_migi.png","yuko_plus_1.png","huan_plus_1.png");
var boardimg= new Array("hospital.png","city.png","shrine.png","school.png");
var gmhand = new Array("移動斜め","暗躍＋２","移動↑↓","移動←→","不安＋１","不安＋１","不安－１","暗躍＋１","友好禁止","不安禁止");
var gmhandimg=new Array("idou_naname.png","anyaku_plus_2.png","idou_ue_sita.png","idou_hidari_migi.png","huan_plus_1.png","huan_plus_1.png","huan_minus_1.png","anyaku_plus_1.png","yuko_kinsi.png","huan_kinsi.png");
var handlist= new Array();
var defhandimg=new Array("hero0.png","hero1.png","hero2.png","write.png","write.png","write.png");
//使い捨て
var disposable=new Array("yuko_plus_2","idou_kinsi","huan_minus_1_pl","idou_naname","anyaku_plus_2");
var charimg=new Array();
var handimg=defhandimg;
/*
function usechar_check(){
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
	var rowspan=CHARALLNUM+3;
	for(var i=0;i<datarr.length;i++){
		datarr[i]=jQuery.trim(datarr[i]);//空白除去
		var tmp = datarr[i].replace(/</g,"&lt;");
		tmp = tmp.replace(/>/g,"&gt;");
		tmp = tmp.replace(/\\n/g,"<br>");
		if(tmp=="")continue;
		var chararr=tmp.split(",");//,で分割
		if(!(chararr[1]=="on")){
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
				}
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
*/
function checkformMonster(num){
	name="#con"+num+"n5";
	if($(name).attr('checked')){
		charlist[num].kaihou=1;
		$("#char"+num).show();
		$("#plhand0opt"+num).show();
		$("#plhand1opt"+num).show();
		$("#plhand2opt"+num).show();
		$("#gmhand3opt"+num).show();
		$("#gmhand4opt"+num).show();
		$("#gmhand5opt"+num).show();
	}else{
		charlist[num].kaihou=0;
		$("#char"+num).hide();
		$("#plhand0opt"+num).hide();
		$("#plhand1opt"+num).hide();
		$("#plhand2opt"+num).hide();
		$("#gmhand3opt"+num).hide();
		$("#gmhand4opt"+num).hide();
		$("#gmhand5opt"+num).hide();
	}
}
