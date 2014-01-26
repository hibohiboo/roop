var $PHASEIMG="../rooper/first/img/loopready.png";
var $CHARPATH="../rooper/first/img/character/";
var $HANDPATH="../rooper/first/img/hand/";
var $BOARDPATH="../rooper/img/board.png";
var $charText="../rooper/kai/char.csv";
var $ruleText="../rooper/MysteryCircle/rule.csv";
var custom=8;


//キャラクター
var charlist = new Array();
var defcharimg=[];
var CHARALLNUM=20;
for(var i=0;i<CHARALLNUM;i++){
	defcharimg[i]="char"+i+".png";
}
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




function formdisabledkashi(num){
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
function checkformdisabledkashi(name,num){
	var charnum=charlist.length;
	for(var i=0;i<charnum;i++){
		$("#kashi"+i).remove();
		charlist[i].kashi=0;
	}
	if(num==9){return;}
	if($("#con"+num+"n5").attr('checked')){
		charlist[num].kashi=1;
		var tmp=$(document.createElement("img"));
		tmp.attr({"src":"../rooper/img/hand/exA.png","alt":"x","id":"kashi"+num});
		tmp.css({'position':"absolute",'top':"20px",'left':"15px",'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
		$("#char"+num).append(tmp).css({"overflow":"visible"});
	}
}



//kashiを反映(update)
function kashichar(i){
	$("#kashi"+i).remove();//一旦消してから作成
	if(charlist[i].kashi==1){
		var tmp=$(document.createElement("img"));
		tmp.attr({"src":"../rooper/img/hand/exA.png","alt":"x","id":"kashi"+i});
		tmp.css({'position':"absolute",'top':"20px",'left':"15px",'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
		$("#char"+i).append(tmp).css({"overflow":"visible"});
	}
}
