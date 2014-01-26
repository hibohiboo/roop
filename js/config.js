$CHARPATH="custom/img/character/";
$HANDPATH="custom/img/hand/";
$BOARDPATH="custom/img/board.png";
$PHASEIMG="custom/img/loopready.png";
$SAVECGI = "./save.cgi";
$SYSTEMCGI='./system.cgi';
var $charText="custom/char.csv";
var $ruleText="custom/rule.csv";
var $dataText="dat/save.dat";
custom=1;
var updateTime=60;//自動更新時間

//手札
$HERONUM=3;
$PLAYNUM=$HERONUM+3;
$CARDWIDTH=35;
$CARDHEIGHT=50;
$CARDMARGIN=5;
$RIGHTWIDTH=160;

//キャラクター
var charlist = new Array();
var defcharimg=new Array("char0.png","char1.png","char2.png","char3.png","char4.png","char5.png","char6.png","char7.png","char8.png","char9.png");
var boardimg= new Array("board0.png","board1.png","board2.png","board3.png");
//手札
var plhand = new Array("暗躍禁止","友好＋２","移動禁止","不安－１","移動↑↓","移動←→","友好＋１","不安＋１","拡張A","拡張B");
var plhandimg= new Array("anyaku_kinsi.png","yuko_plus_2.png","idou_kinsi.png","huan_minus_1_pl.png","idou_ue_sita.png","idou_hidari_migi.png","yuko_plus_1.png","huan_plus_1.png","exA.png","exB.png");
var gmhand = new Array("移動斜め","暗躍＋２","移動↑↓","移動←→","不安＋１","不安＋１","不安－１","暗躍＋１","友好禁止","不安禁止","拡張A","拡張B");
var gmhandimg=new Array("idou_naname.png","anyaku_plus_2.png","idou_ue_sita.png","idou_hidari_migi.png","huan_plus_1.png","huan_plus_1.png","huan_minus_1.png","anyaku_plus_1.png","yuko_kinsi.png","huan_kinsi.png","exA.png","exB.png");
var handlist= new Array();
var defhandimg=new Array("hero0.png","hero1.png","hero2.png","write.png","write.png","write.png");
//使い捨て
var disposable=new Array("yuko_plus_2","idou_kinsi","huan_minus_1_pl","idou_naname","anyaku_plus_2");
var charimg=new Array();
var handimg=defhandimg;
