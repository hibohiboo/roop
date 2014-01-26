//読み込んだdataの反映。
function update(query){
	//&で分割
	var tmparr = query.split('&');
//	alert(query);
	var tmparrnum=tmparr.length;//2013.07.04.add
	var charnum=charlist.length;//2013.07.04.add
	for(var i=0;i<tmparrnum;i++){
		//@で分割
		var tmp = tmparr[i].split('@');
//		alert(tmp[0]);
		switch(tmp[0]){
		case "char":
			var num=parseInt(tmp[1]);
			var chararr=tmp[2].split(",");//,で分割
			charlist[num].nownum=parseInt(chararr[0]);
			charlist[num].nowpos=parseInt(chararr[1]);
			charlist[num].nextnum=parseInt(chararr[2]);
			charlist[num].nextpos=parseInt(chararr[3]);
			charlist[num].anyaku=parseInt(chararr[4]);
			charlist[num].huan=parseInt(chararr[5]);
			charlist[num].yuko=parseInt(chararr[6]);
			charlist[num].x=parseInt(chararr[7]);
			charlist[num].y=parseInt(chararr[8]);
			charlist[num].kill=parseInt(chararr[9]);
			//2012.5.5追記→→
			if(charlist[num].kill==1){
				$("#con"+num).attr({'checked':true});
				formdisabled("con"+num,num);
			}else{
				$("#con"+num).attr({'checked':false});
				formdisabled("con"+num,num);
			}
			//←←
			killchar(num);//5.21追記
		//↓↓ホーンテッドステージ
			//alert(num+":"+(charnum-3));
			if((custom==9||custom==4)&&num>=(charnum-3)&&num<charnum){//2013.07.04.add
				charlist[num].kaihou=parseInt(chararr[10]);
			if(charlist[num].kaihou==1){
				$("#con"+num+"n5").attr({'checked':true});
				checkformMonster(num);
			}else{
				$("#con"+num+"n5").attr({'checked':false});
				checkformMonster(num);
			}

			}
		//↑↑ホーンテッドステージ
		//↓↓ミステリーサークル
			if(custom==5||custom==8){//2013.07.04.add
				charlist[num].kashi=parseInt(chararr[10]);
				if(charlist[num].kashi==1){
					$("#con"+num+"n5").attr({'checked':true});
					formdisabledkashi(num);
				}else{
					$("#con"+num+"n5").attr({'checked':false});
					formdisabledkashi(num);
				}
				kashichar(num);
			}
		//↑↑ミステリーサークル
		//↓↓幻想用
			if(custom>=6&&num==19){
				charlist[num].remove=parseInt(chararr[11]);
				if(charlist[num].remove==0){//除外確認
					$("#fantasyRemove").attr({'checked':false});
				}else{
					$("#fantasyRemove").attr({'checked':true});
				}
				checkformFantasy(charlist[num].remove);
			}
		//↑↑幻想用2013.11.09
			break;
		case "plhand":
			var num=parseInt(tmp[1]);
			var arr=tmp[2].split(",");//,で分割
			handlist[num].card=parseInt(arr[0]);
			handlist[num].char=parseInt(arr[1]);
			handlist[num].x=parseInt(arr[2]);
			handlist[num].y=parseInt(arr[3]);
			handlist[num].order=parseInt(arr[4]);
			handlist[num].nextorder=parseInt(arr[5]);
			handlist[num].anyaku=parseInt(arr[6]);
			handlist[num].yuko_plus_2=parseInt(arr[7]);
			handlist[num].idou_kinsi=parseInt(arr[8]);
			handlist[num].huan_minus_1_pl=parseInt(arr[9]);
			disablecard(num);
			checkleader(num);
			break;
		case "gmhand":
			var num=parseInt(tmp[1]);
			var arr=tmp[2].split(",");//,で分割
			handlist[num].card=parseInt(arr[0]);
			handlist[num].char=parseInt(arr[1]);
			handlist[num].x=parseInt(arr[2]);
			handlist[num].y=parseInt(arr[3]);
			handlist[num].idou_naname=parseInt(arr[4]);
			handlist[num].anyaku_plus_2=parseInt(arr[5]);
			disablecard(num);
			break;
		case "board":
			var num=parseInt(tmp[1]);
			boards[num].anyaku=parseInt(tmp[2]);
			break;
		case "phase":
			var tmparr=tmp[1].split(",");//,で分割
			phase.nextloop=parseInt(tmparr[0]);
			phase.nextday=parseInt(tmparr[1]);
			phase.nextphase=parseInt(tmparr[2]);
			phasecheck();
			break;
		case "scenario":
			$sheetopen=tmp[1];
			break;
		case "excounter":
			$ExCounter=tmp[1];
			$("#ExConPrev").text($ExCounter);
			break;
		case 'rumor'://2013.11.10.anothrhorizon
			if(custom!=10)break;//2013.11.23.add
			rumor=tmp[1];
			checkrumor();
			break;
		}
	}
}