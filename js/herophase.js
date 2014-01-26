var prev_card_flg="pl";
var HERO=0;
$(window).load(function(){HERO=$("#hero").val();});

function nextPhase(){
	switch(phase.phase){
		case 1:
		case 2:
		case 6:
		case 10:
		case 11:
		case 12:
		case 13:
		case 15:
			setswitch();
			break;
		case 7:
			var check=nextPhaseSetHeroCard(HERO,7);
			break;
		case 8:
			var check=nextPhaseSetHeroCard(HERO,8);
			break;
		case 9:
			var check=nextPhaseSetHeroCard(HERO,9);
			break;
	}
	if(check==-1)return;
	nextPhaseLast();
}


function phasecheck(){
	if(phase.loop<phase.nextloop){
		nextloop();
		loadData("data");
	}
	if($sheetopen=="1"){$("#closesheet").show();}else{$("#closesheet").hide();}
	if(phase.phase==16){phase.phase=4;}
	if(phase.day==phase.nextday&&phase.phase>=phase.nextphase)return;//巻き戻り防止。
	if(phase.nextphase==phase.phase&&phase.day==0)return;
	if(phase.phase<5&&phase.nextphase>=5)phase.phase=4;
	phase.phase++;//フェイズを進める。

	switch(phase.phase){
		case 0:
			$("#nextloopbutton").hide();
			break;
		case 1://カウンターの除去と配置
		if(custom>=6){//χでは時の狭間
		}else{
			resetcounter();
		}
			break;
		case 2://キャラクターの配置
				if(custom>=6){//χではカウンターの配置
					usechar_check();
					resetcounter();
				}else{
			setdefpos();
		}
			break;
		case 3://手札の配布
			if(custom>=6){//χではキャラクターの配置
					setdefpos();
			}else{
				resethand();
			}
			break;
		case 4:
			if(custom>=6){//χでは手札の配布
				resethand();
			}
			break;
		case 5://ターン開始時処理
			phase.day-=(-1);
			$("#day").text(phase.day);
			//reclaimhand()//2013.11.08.change before:
			reversehand();
			usechar_check();
			break;
		case 6://脚本家行動フェイズ

			break;
		case 7://主人公行動フェイズ１
			phaseHeroAction(HERO,0);
			break;
		case 8://主人公行動フェイズ２
			phaseHeroAction(HERO,1);
			break;
		case 9://主人公行動フェイズ３
			phaseHeroAction(HERO,2);
			break;
		case 10://行動解決フェイズ
			phaseHeroAction(HERO,3);
			openhand();
			moveOpenHand();
			break;
		case 11://脚本家能力使用フェイズ
			chartablecontrol();
			if(phase.nextphase>10){reclaimhand();}//手札回収
			break;
		case 12://主人公能力使用フェイズ
			chartablecontrol();
			break;
		case 13://事件フェイズ
			chartablecontrol();
			break;
		case 14://リーダー交代フェイズ
			break;
		case 15://ターン終了フェイズ
			break;
		case 16:
			phasecheck();
			break;
	}
	phaseCheckLast();
}
	
