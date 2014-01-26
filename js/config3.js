var $PHASEIMG="../rooper/img/loopready.png";
var $CHARPATH="../rooper/img/character/";
var $HANDPATH="../rooper/img/hand/";
var $BOARDPATH="../rooper/img/board.png";
var $charText="../rooper/VisualNovel/char.csv";
var $ruleText="../rooper/VisualNovel/rule.csv";
var custom=0;


//キャラクター
var charlist = new Array();
var defcharimg=new Array("Shonen.png","Shojo.png","Ojo.png","Miko.png","Keiji.png","Salary.png","Joho.png","Isha.png","Kanja.png");
//手札
var plhand = new Array("暗躍禁止","友好＋２","移動禁止","不安－１","移動↑↓","移動←→","友好＋１","不安＋１","拡張A","拡張B");
var plhandimg= new Array("anyaku_kinsi.png","yuko_plus_2.png","idou_kinsi.png","huan_minus_1_pl.png","idou_ue_sita.png","idou_hidari_migi.png","yuko_plus_1.png","huan_plus_1.png","exA.png","exB.png");
var boardimg= new Array("hospital.png","city.png","shrine.png","school.png");
var gmhand = new Array("移動斜め","暗躍＋２","移動↑↓","移動←→","不安＋１","不安＋１","不安－１","暗躍＋１","友好禁止","不安禁止","拡張A","拡張B");
var gmhandimg=new Array("idou_naname.png","anyaku_plus_2.png","idou_ue_sita.png","idou_hidari_migi.png","huan_plus_1.png","huan_plus_1.png","huan_minus_1.png","anyaku_plus_1.png","yuko_kinsi.png","huan_kinsi.png","exA.png","exB.png");
var handlist= new Array();
var defhandimg=new Array("hero0.png","hero1.png","hero2.png","write.png","write.png","write.png");
//使い捨て
var disposable=new Array("yuko_plus_2","idou_kinsi","huan_minus_1_pl","idou_naname","anyaku_plus_2");
var charimg=new Array();
var handimg=defhandimg;
