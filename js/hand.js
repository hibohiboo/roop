
//==================================================================================================================
//手札オブジェクト作成
function makehand(){
	for(var i=0;i<$PLAYNUM;i++){
		var tmpobj=new function(){
			this.card=-1;//カード番号
			this.char=-1;//選択キャラクター番号
			this.x=0;
			this.y=0;
			
			if(i<$HERONUM){
				this.name="pl"+i;
				this.anyaku=0;//暗躍禁止チェッカー
				this.yuko_plus_2=0;//友好＋２チェッカーthis.order=i;//順番チェック
				this.idou_kinsi=0;//移動禁止チェッカーthis.nextorder=i+1;//次の順番
				this.huan_minus_1_pl=0;//不安マイナス１チェック
			//	alert("友好リセット");
				this.order=i;
				this.nextorder=i-1;
				if(i==0)this.nextorder=$HERONUM-1;
			}else{
				this.name="gm"+i;
				this.idou_naname=0;//移動斜めチェッカー
				this.anyaku_plus_2=0;//暗躍＋２チェッカー
			//	alert("idou_naname"+this.idou_naname);
			}
		}       
		handlist.push(tmpobj);
	}
}

/*-------------------------------------------------------*/
/*ボード手札配置*/
function makeselecthand(){
	//右側プレビュー画面作成

	$("#right").append($(document.createElement("div")).attr({"id":"prevarea"}).css({'width':$RIGHTWIDTH+"px",'height':"200px",'top':"70px",'position':"absolute",'left':20+"px"}));
	//下側プレビュー画面作成

	$("#center").append($(document.createElement("div")).attr({"id":"sumiarea"}).css({'width':"400px",'height':"140px",'top':"290px",'position':"absolute",'left':20+"px"}));
	for(var i=0;i<$PLAYNUM;i++){
		var div = document.createElement("div");
		if(i<$HERONUM){
			div.className="handcard";
		}else{
			div.className="gmhandcard";
		}
		/*2012.0505追加→→*/
		if(i==0){
			div.style.border="solid 1px #00BFFF";
		}else if(i==1){
			div.style.border="solid 1px #00FF7F";
		}else if(i==2){
			div.style.border="solid 1px yellow";
		}else{
			div.style.border="solid 1px red";
		}
		/*←←*/
		div.id="hand"+i;
		div.style.backgroundImage="url("+$HANDPATH+handimg[i]+")";
		var $board = document.getElementById("board");
		$board.appendChild(div);
		//右側プレビュー画面作成

		var prev = $(document.createElement("div"));
		prev.attr({'id':"player"+i});
		prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+handimg[i]+")",'position':"absolute",'top':($CARDMARGIN-(-i)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':$CARDMARGIN+"px"});
		/*2012.0505追加→→*/
		if(i==0){
			prev.css({"border":"solid 1px #00BFFF"});
		}else if(i==1){
			prev.css({"border":"solid 1px #00FF7F"});
		}else if(i==2){
			prev.css({"border":"solid 1px yellow"});
		}else{
			prev.css({"border":"solid 1px red"});
		}
		/*←←*/
		if(handlist[i].order==0){
			var img=$(document.createElement("img"));
			img.attr({'src':"../rooper/img/leader.png",'alt':"leader"+i,'id':"leader"+i});
			img.css({'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
			prev.append(img);
		}else{
			prev.html("");
		}

		$("#prevarea").append(prev);

		var prev = $(document.createElement("div"));
		prev.attr({'id':"handprev"+i});
		prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+handimg[i]+")",'position':"absolute",'top':($CARDMARGIN-(-i)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':$CARDWIDTH-(-$CARDMARGIN*2)+"px"});
		/*2012.0505追加→→*/
		if(i==0){
			prev.css({"border":"solid 1px #00BFFF"});
		}else if(i==1){
			prev.css({"border":"solid 1px #00FF7F"});
		}else if(i==2){
			prev.css({"border":"solid 1px yellow"});
		}else{
			prev.css({"border":"solid 1px red"});
		}
		/*←←*/
		$("#prevarea").append(prev);

		var prev = $(document.createElement("div"));
		prev.attr({'id':"handcharprev"+i});
		prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$CHARPATH+"silhouette.png"+")",'position':"absolute",'top':$CARDMARGIN-(-i)*($CARDMARGIN-(-$CARDHEIGHT))+"px",'left':$CARDWIDTH*2-(-$CARDMARGIN*3)+"px"});
		$("#prevarea").append(prev);
		/*2012.0505追加→→*/
		if(i==0){
			prev.css({"border":"solid 1px #00BFFF"});
		}else if(i==1){
			prev.css({"border":"solid 1px #00FF7F"});
		}else if(i==2){
			prev.css({"border":"solid 1px yellow"});
		}else{
			prev.css({"border":"solid 1px red"});
		}
		/*←←*/
		
	}
		//下側プレビュー画面作成
	for(var i=0;i<2;i++){
		//hero1,2
		var prev = $(document.createElement("div"));
		prev.attr({'id':"playersumi"+i});
		prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+handimg[i]+")",'position':"absolute",'top':($CARDMARGIN-(-i)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':$CARDMARGIN+"px"});
			/*2012.0505追加→→*/
		if(i==0){
			prev.css({"border":"solid 1px #00BFFF"});
		}else if(i==1){
			prev.css({"border":"solid 1px #00FF7F"});
		}else{
		}
		/*←←*/
		$("#sumiarea").append(prev);
		for(var j=1;j<4;j++){
			var prev = $(document.createElement("div"));
			prev.attr({'id':"sumiprev"+i+"hand"+j});
			prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+plhandimg[j]+")",'position':"absolute",'top':($CARDMARGIN-(-i)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':$CARDWIDTH*j-(-$CARDMARGIN*(j+1))+"px"});

		/*2012.0505追加→→*/
		if(i==0){
			prev.css({"border":"solid 1px #00BFFF"});
		}else if(i==1){
			prev.css({"border":"solid 1px #00FF7F"});
		}else{
		}
		/*←←*/
		/*2013.06.02.add*/
		if(prev_card_flg=="gm"&&(custom>=6)){//2013/8/18.add
			prev.data({"i":i,"j":j});
			prev.click(function(){
　					card_revive($(this).data("i"),$(this).data("j"));
			});
		}
		
		
			$("#sumiarea").append(prev);
		}
	}
	//hero3
	var prev = $(document.createElement("div"));
	prev.attr({'id':"playersumi"+2});
	prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+handimg[2]+")",'position':"absolute",'top':($CARDMARGIN-(-0)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':200-(-$CARDMARGIN)+"px"});
		/*2012.0505追加→→*/
		prev.css({"border":"solid 1px yellow"});
		/*←←*/
	$("#sumiarea").append(prev);
	for(var j=1;j<4;j++){
		var prev = $(document.createElement("div"));
		prev.attr({'id':"sumiprev"+2+"hand"+j});
		prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+plhandimg[j]+")",'position':"absolute",'top':($CARDMARGIN-(-0)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':200-(-$CARDWIDTH*j)-(-$CARDMARGIN*(j+1))+"px"});
		/*2012.0505追加→→*/
		prev.css({"border":"solid 1px yellow"});
		/*←←*/
		/*2013.06.02.add*/
		if(prev_card_flg=="gm"&&(custom>=6)){//2013.8.18.add
			prev.data("i",2).data("j",j);
			prev.click(function(){
　					card_revive($(this).data("i"),$(this).data("j"));
			});
		}
		$("#sumiarea").append(prev);
	}
	
	//writer
	var prev = $(document.createElement("div"));
	prev.attr({'id':"playersumi"+3});
	prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+handimg[3]+")",'position':"absolute",'top':($CARDMARGIN-(-1)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':200-(-$CARDMARGIN)+"px"});
		/*2012.0505追加→→*/
	prev.css({"border":"solid 1px red"});
		/*←←*/
	$("#sumiarea").append(prev);
	for(var j=0;j<2;j++){
		var prev = $(document.createElement("div"));
		prev.attr({'id':"sumiprev"+3+"hand"+j});
		prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px","background-image":"url("+$HANDPATH+gmhandimg[j]+")",'position':"absolute",'top':($CARDMARGIN-(-1)*($CARDMARGIN-(-$CARDHEIGHT)))+"px",'left':200-(-$CARDWIDTH*(j+1))-(-$CARDMARGIN*(j+2))+"px"});
		/*2012.0505追加→→*/
			prev.css({"border":"solid 1px red"});
		/*←←*/
		//2013.11.09.add 委員長能力脚本家に適用
		if(prev_card_flg=="gm"&&(custom==10)){
			prev.data("j",j);
			prev.click(function(){
　					card_revive_writer($(this).data("j"));
			});
		}
		$("#sumiarea").append(prev);
		//2013.11.09↑↑
	}

	//ExCounter
	var prev = $(document.createElement("div"));
	prev.attr({'id':'prev_ExCounter'});//2013.5.20.adds

	prev.css({'width':$CARDWIDTH+"px",'height':$CARDHEIGHT+"px",'border':"solid 2px",'position':"absolute",'top':($CARDMARGIN-(-1)*($CARDMARGIN-(-$CARDHEIGHT)))-(-5)+"px",'left':200-(-$CARDWIDTH*(2+1))-(-$CARDMARGIN*(2+2))-(-5)+"px"});
	if(!document.all){
		prev.css({"text-align":"center","vertical-align":"middle"});
	}else{
		prev.css({"text-align":"center"});
	}
	

	prev.html("Ex<hr style='padding:0px 1px;margin:0px;' /><strong id='ExConPrev'>0</strong>");
	$("#sumiarea").append(prev);

}

/*==========================================================*/
//手札選択画面。
/*=========================================================*/
function makehandTable(num,pl){
	var $form = $(document.createElement("form"));
	$form.attr({"name":pl+"handform"+num,'id':pl+"handform"+num,'class':pl+"form"});
	$form.css({"float":"left"});
	/*
	if(pl=="pl"){
		$("#left").append($form);
	}else{
		$("#writer").append($form);
	}*/
	//
	var $ul=$(document.createElement("ul"));
	$ul.css({"list-style":"none"});
	$form.append($ul);

	var $li=$(document.createElement("li"));
	$li.css({"border":"solid 1px","width":"80px","height":"70px"});
	$ul.append($li);
		var div=$(document.createElement("div"));
		div.css({"float":"left"});
		$li.append(div);
	var $div=$(document.createElement("div"));
	$div.attr({"name":"",'class':"charcard",'id':"prevhand"+pl+num});
	$div.css({"background-image":"url("+$HANDPATH+"Unselected.png"+")",'display':"block",'position':"static"});
		/*2012.0505追加→→*/
		if(num==0){
			$div.css({"border":"solid 1px #00BFFF"});
		}else if(num==1){
			$div.css({"border":"solid 1px #00FF7F"});
		}else if(num==2){
			$div.css({"border":"solid 1px yellow"});
		}else{
			$div.css({"border":"solid 1px red"});
		}
		/*←←*/
	div.append($div);
		var div=$(document.createElement("div"));
		div.css({"float":"left"});
		$li.append(div);
	var $div=$(document.createElement("div"));
	$div.attr({"name":"",'class':"charcard",'id':"prevchar"+pl+num});
	$div.css({"background-image":"url("+$CHARPATH+"silhouette.png"+")",'display':"block",'position':"static"});
	div.append($div);//てすと
	//
	var select= $(document.createElement("select"));
	select.css({'clear':"both"});//てすと
	select.attr({'name' :pl+"hand",'id':pl+"hand"+num,"disabled":false});
	//select.change(function(){selectchar(pl,num,select.attr('id'))});
	select.change(function(){selectchar(pl,num)});
	$li.append(select);
	for(var cnt=-1;cnt<charlist.length;cnt++){
		var option =$(document.createElement("option"));
		option.attr({"value":cnt,"id":pl+"hand"+num+"opt"+cnt});
		if(cnt!=-1){option.text(charlist[cnt].name);
		}else{
			option.text("キャラ選択");
		}
		select.append(option);
	}
	for(var cnt=0;cnt<boards.length;cnt++){
		var option =$(document.createElement("option"));
		option.attr({"value":cnt+charlist.length});
		option.text(boards[cnt].name);
		select.append(option);
	}
	if(pl=="pl"){
		var $hand=plhand;
		var $handimg=plhandimg;
	}else{
		var $hand=gmhand;
		var $handimg=gmhandimg;
	}
	for(var i=0;i<$hand.length;i++){
		if(i%2==0){
			var $li=$(document.createElement("li"));
			$li.css({"border":"solid 1px","clear":"both","width":"80px","height":"70px"});
			$ul.append($li);
		}
		var div=$(document.createElement("div"));
		div.css({"float":"left"});
		$li.append(div);
		var $div=$(document.createElement("div"));
		$div.attr({"name":"",'class':"charcard","id":pl+"hand"+num+"cardimg"+i});
		$div.css({"background-image":"url("+$HANDPATH+$handimg[i]+")",'position':"static","display":"block"});
		$div.data("i",i);
		div.append($div);
		var $input=$(document.createElement("input"));
		$input.attr({"type":"radio","id":pl+"hand"+num+"card"+i,"name":pl+"hand"+num+"card"});
		$input.val(i);
		$input.data("num",num);
		$input.change(function(){selecthand(pl,this.value,num);});
		div.append($input);
		$div.click(function(){
			var tmp = parseInt($(this).data("i"));
			if(num<$HERONUM&&tmp<4&&tmp>0){
				var dis = disposable[tmp-1];
				if(handlist[num][dis]==1)return;
			}
			if(num>=$HERONUM&&tmp<2){
				var dis = disposable[tmp+3];
				
				if(handlist[num][dis]==1)return;
			}
			var radio=$('#'+pl+"hand"+num+"card"+$(this).data("i"));
			radio.attr({"checked":true});
			selecthand(pl,radio.val(),num);
		});
	}
	//2013.11.10
	if(pl=="pl"){
		$("#left").append($form);
	}else{
		$("#writer").append($form);
	}


}

/*======================================================================================================*/
//コントロール
/*======================================================================================================*/




//-----------------------------------------------
function selectchar(pl,num){
	var id=pl+"hand"+num;
	var val=$('#'+id+' option:selected').val();
	if(pl=="pl"){
		var $bias=10;
	}else{
		var $bias=5;
	}
	if(val<charlist.length){
		//HauntedStage(custom==4)では死体にカードセット可能//2013.7.14.add custom==9
		if(!(custom==9 || custom == 4)&&charlist[val]&&charlist[val].kill==1){
			alert("死体にカードはセットできません");
			$('#'+id).val(-1);
			return;
		}
		//ミステリー・サークル用↓↓
		if((custom==8||custom == 5)&&pl=="pl"&&charlist[val].kashi==1){//2013.07.03.add
			alert("主人公は仮死のキャラクターにカードをセットできません");
			$('#'+id).val(-1);
			$('#prevchar'+pl+num).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"}).html("");
			return;
		}
		//↑↑
	}
	
	if(val!=-1){switch(num){
	case 0:
		if(handlist[1].char==val||handlist[2].char==val){
			alert("すでに他の主人公カードがセットされています");
			$('#'+id).val(-1);
			$('#prevchar'+pl+num).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"}).html("");//2013/3/5追記
			return;
		}
		break;
	case 1:
		if(handlist[0].char==val||handlist[2].char==val){
			alert("すでに他の主人公カードがセットされています");
			$('#prevchar'+pl+num).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"}).html("");//2013/3/5追記
			$('#'+id).val(-1);
			return;
		}
		break;
	case 2:
		if(handlist[0].char==val||handlist[1].char==val){
		 	alert("すでに他の主人公カードがセットされています");
			$('#prevchar'+pl+num).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"}).html("");//2013/3/5追記
		 	$('#'+id).val(-1);
			return;
		}
		break;
	case 3:
		if(handlist[4].char==val || handlist[5].char==val){
			alert("すでにカードがセットされています");
			$('#'+id).val(-1);
			return;
		}
		break;
	case 4:
		if(handlist[$HERONUM].char==val || handlist[5].char==val){
			alert("すでにカードがセットされています");
			$('#'+id).val(-1);
			return;
		}
		break;
	case 5:
		if(handlist[$HERONUM].char==val || handlist[4].char==val){
			alert("すでにカードがセットされています");
			$('#'+id).val(-1);
			return;
		}
		break;
	}}
	
	handlist[num].char=val;
	if(val<0){
		$('#prevchar'+pl+num).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"});
		selectcardset(num);
		return;
	}
	
	$('#prevchar'+pl+num).css({"background-image":"url("+$CHARPATH+charimg[val]+")"});
	$('#handcharprev'+num).css({"background-image":"url("+$CHARPATH+charimg[val]+")"});
	if(val<charlist.length){
		handlist[num].x=charlist[val].x-(-$bias);
		handlist[num].y=charlist[val].y-(-$bias);
		addcounter($('#handcharprev'+num),charlist[val].yuko,charlist[val].huan,charlist[val].anyaku,val);
	}else{
		handlist[num].x=boards[val-charlist.length].x-(-$bias);
		handlist[num].y=boards[val-charlist.length].y-(-$bias);
		addanyaku($('#handcharprev'+num),boards[val-charlist.length],num);
	}
	selectcardset(num);
}

function selecthand(pl,i,num){
	//if(i!=-1){
	switch(num){
		case 3:
			if(handlist[4].card==i|| handlist[5].card==i){
				alert("そのカードはボードにセットされています。");
				$('#'+'gmhand3card'+i).attr({"checked":false});//2013.11.11.10add
				$('#'+'gmhand3card'+handlist[3].card).attr({"checked":true});//2013.11.11.10add
				return;
			}
			break;
		case 4:
			if(handlist[$HERONUM].card==i || handlist[5].card==i){
				alert("そのカードはボードにセットされています。");
				$('#'+'gmhand4card'+i).attr({"checked":false});//2013.11.11.10add
				$('#'+'gmhand4card'+handlist[4].card).attr({"checked":true});//2013.11.11.10add
				return;
			}
			break;
		case 5:
			if(handlist[4].card==i || handlist[$HERONUM].card==i){
				alert("そのカードはボードにセットされています。");
				$('#'+'gmhand5card'+i).attr({"checked":false});//2013.11.11.10add
				$('#'+'gmhand5card'+handlist[5].card).attr({"checked":true});//2013.11.11.10add
				return;
			}
			break;
	}
	//}
	$("#sumi"+num+"hand"+handlist[num].card).remove();
	if(pl=="pl"){
		var $hand=plhand;
		var $handimg=plhandimg;
	}else{
		var $hand=gmhand;
		var $handimg=gmhandimg;
	}
	$('#prevhand'+pl+num).css({"background-image":"url("+$HANDPATH+$handimg[i]+")"});
	/*
	if(i==0){
		this.anyaku=1;
	}else {
		this.anyaku=0;
	}*/
	if(pl=="pl"&&i>0&&i<4){
		var img=$(document.createElement("img"));
		img.attr({'src':"../rooper/img/sumi.png",'alt':"sumi",'id':"sumi"+num+"hand"+i});
		img.css({'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
		$("#"+pl+"hand"+num+"cardimg"+i).append(img);
	}
	if(pl=="gm"&&i>-1&&i<2){
		var img=$(document.createElement("img"));
		img.attr({'src':"../rooper/img/sumi.png",'alt':"sumi",'id':"sumi"+num+"hand"+i});
		img.css({'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
		$("#"+pl+"hand"+num+"cardimg"+i).append(img);
	}
	handlist[num].card=i;
	selectcardset(num);
}


//一度使ったカードを使用不可にする。update,recraimhandより
function disablecard(i){
	for(var j=0;j<disposable.length;j++){
		var tmp=disposable[j];
		if(j<$HERONUM){
			var cardnumber=j+1;
			var pl="pl";
		}else{
			var cardnumber=j-$HERONUM;
			var pl="gm";
		}
		if(handlist[i][tmp]&&handlist[i][tmp]==1){
			$("#"+pl+"hand"+i+"card"+cardnumber).hide();
			$("#"+pl+"hand"+i+"cardimg"+cardnumber).css({"background-image":"url("+$HANDPATH+tmp+"_sumi.png)"});
			if(phase.phase>10){$("#sumiprev"+i+"hand"+cardnumber).css({"background-image":"url("+$HANDPATH+tmp+"_sumi.png)"});}
		}else{
		//2013.06.03.add//2013.06.09.more.add//2013.8.18.more.add
			if(i<$HERONUM&&pl=="pl"&&(custom>=6)){
				$("#"+pl+"hand"+i+"cardimg"+cardnumber).css({"background-image":"url("+$HANDPATH+tmp+".png)"});
				$("#sumiprev"+i+"hand"+cardnumber).css({"background-image":"url("+$HANDPATH+tmp+".png)"});
				$("#sumi"+i+"hand"+cardnumber).remove();
				$("#"+pl+"hand"+i+"card"+cardnumber).show();
			}else if(i>=$HERONUM&&pl=="gm"&&(custom>=6)){//2013.11.18.add
				$("#"+pl+"hand"+i+"cardimg"+cardnumber).css({"background-image":"url("+$HANDPATH+tmp+".png)"});
				$("#sumiprev"+i+"hand"+cardnumber).css({"background-image":"url("+$HANDPATH+tmp+".png)"});
				$("#sumi"+i+"hand"+cardnumber).remove();
				$("#"+pl+"hand"+i+"card"+cardnumber).show();
			}
		}
	}
}
//手札回収
function reclaimhand(){
	for(var i=0;i<$PLAYNUM;i++){
		handlist[i].char=-1;
		$("#hand"+i).hide();
		//使用したループ１回を使用済みに
		if(i<$HERONUM){
			handlist[i].anyaku=0;
			var pl="pl";
			if(handlist[i].card==1){
				handlist[i].yuko_plus_2=1;
				$("#sumiprev"+i+"hand"+1).css({"background-image":"url("+$HANDPATH+disposable[0]+"_sumi.png)"});
			}
			if(handlist[i].card==2){
				handlist[i].idou_kinsi=1;
				$("#sumiprev"+i+"hand"+2).css({"background-image":"url("+$HANDPATH+disposable[1]+"_sumi.png)"});
			}
			if(handlist[i].card==3){
				handlist[i].huan_minus_1_pl=1;
				$("#sumiprev"+i+"hand"+3).css({"background-image":"url("+$HANDPATH+disposable[2]+"_sumi.png)"});
			}
			
			disablecard(i);
		}else{
			var pl="gm";
			if(handlist[i].idou_naname==1){
				var num=0;
				//GMの手札は共通
				for(var cnt=$HERONUM;cnt<$PLAYNUM;cnt++){
					$("#"+pl+"hand"+cnt+"card"+num).hide();
					$("#"+pl+"hand"+cnt+"cardimg"+num).css({"background-image":"url("+$HANDPATH+"idou_naname_sumi.png)"});
					$("#sumiprev"+3+"hand"+num).css({"background-image":"url("+$HANDPATH+"idou_naname"+"_sumi.png)"});
					handlist[cnt].idou_naname=1;
				}
			}
			if(handlist[i].anyaku_plus_2==1){
				var num=1;
				for(var cnt=$HERONUM;cnt<$PLAYNUM;cnt++){
					$("#"+pl+"hand"+cnt+"card"+num).hide();
					$("#"+pl+"hand"+cnt+"cardimg"+num).css({"background-image":"url("+$HANDPATH+"anyaku_plus_2_sumi.png)"});
					$("#sumiprev"+3+"hand"+num).css({"background-image":"url("+$HANDPATH+"anyaku_plus_2"+"_sumi.png)"});
					handlist[cnt].anyaku_plus_2=1;
				}
			}
		}
		//カードを裏返す
		$('#prevchar'+pl+i).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"}).html("");
		$('#prevhand'+pl+i).css({"background-image":"url("+$HANDPATH+"Unselected.png"+")"});
		$('#handcharprev'+i).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"}).html("");
		$('#handprev'+i).css({"background-image":"url("+$HANDPATH+handimg[i]+")"});
		$('#'+pl+'hand'+i).val(-1);
		$('#'+pl+"hand"+i+"card"+handlist[i].card).attr({"checked":false});
		$("#hand"+i).css({"background-image":"url("+$HANDPATH+handimg[i]+")"});
		handlist[i].card=-1;
	}
	//2013.11.10.addうわさ話カード回収
	if(custom==10){
		rumor=-1;
		$("#rumorcard").hide();
		$("#rumor").val(-1);
	}
}

function reversehand(){
	for(var i=0;i<$PLAYNUM;i++){
		if(i<$HERONUM){
			var pl="pl";
		}else{
			var pl="gm";
		}
		//カードを裏返す
		$('#prevchar'+pl+i).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"}).html("");
		$('#prevhand'+pl+i).css({"background-image":"url("+$HANDPATH+"Unselected.png"+")"});
		$('#handcharprev'+i).css({"background-image":"url("+$CHARPATH+"silhouette.png"+")"}).html("");
		$('#handprev'+i).css({"background-image":"url("+$HANDPATH+handimg[i]+")"});
		$('#'+pl+'hand'+i).val(-1);
		$('#'+pl+"hand"+i+"card"+handlist[i].card).attr({"checked":false});
		$("#hand"+i).css({"background-image":"url("+$HANDPATH+handimg[i]+")"});
	}
}
//初期化
function resethand(){
	for(var i=0;i<$PLAYNUM;i++){
		$("#hand"+i).hide();
		handlist[i].char=-1;//選択キャラクター
		handlist[i].x=0;
		handlist[i].y=0;
		if(i<$HERONUM){
			handlist[i].anyaku=0;
			handlist[i].yuko_plus_2=0;
			handlist[i].idou_kinsi=0;
			handlist[i].huan_minus_1_pl=0;
			var pl="pl";
			for(var j=1;j<4;j++){
				var dis=disposable[j-1];
				$("#"+pl+"hand"+i+"cardimg"+j).css({"background-image":"url("+$HANDPATH+dis+".png)"});
				$("#sumiprev"+i+"hand"+j).css({"background-image":"url("+$HANDPATH+dis+".png)"});
				$("#sumi"+i+"hand"+j).remove();
				$("#"+pl+"hand"+i+"card"+j).show();
			}
		}else{
			handlist[i].idou_naname=0;//
			handlist[i].anyaku_plus_2=0;//
			var pl="gm";
			for(var j=0;j<2;j++){
				var dis=disposable[j+3];
				$("#"+pl+"hand"+i+"cardimg"+j).css({"background-image":"url("+$HANDPATH+dis+".png)"});
				$("#sumiprev"+3+"hand"+j).css({"background-image":"url("+$HANDPATH+dis+".png)"});
				$("#sumi"+i+"hand"+j).remove();
				$("#"+pl+"hand"+i+"card"+j).show();
			}
		}
		$('#'+pl+"hand"+i+"card"+handlist[i].card).attr({"checked":"false"});
		handlist[i].card=-1;//カード番号
	}
	reclaimhand();//手札裏返し
}
//////////////////////////////////////////////////////////////////////////////////////////////////////
//--------------------------------------------
//手札場所設定
//--------------------------------------------
function sethandpos(){
	for(var i=0;i<$PLAYNUM;i++){
		selectcardset(i);
	}
}

//カードを設置。
function selectcardset(num){
	if(handlist[num].card==-1||handlist[num].char==-1){
	$("#hand"+num).css({"display":"none"});
		return;
	}
	$("#hand"+num).css({"display":"block","top":handlist[num].y+"px","left":handlist[num].x+"px"});
	
	var val=handlist[num].char;
	$('#handcharprev'+num).css({"background-image":"url("+$CHARPATH+charimg[val]+")"});
	if(val<charlist.length){
		addcounter($('#handcharprev'+num),charlist[val].yuko,charlist[val].huan,charlist[val].anyaku,val);
	}else{
		addanyaku($('#handcharprev'+num),boards[val-charlist.length],num);
	}
}
//手札公開。
function openhand(){
	for(var i=0;i<6;i++){
		var num=handlist[i].card;
		var charnum=handlist[i].char;
		if(handlist[i].card==-1)continue;//2013.11.10.change{return;}
		if(handlist[i].char==-1)continue;//2013.11.10.change{return;}
		if(i<3){
			var tmp=plhandimg;
		}else{
			var tmp=gmhandimg;
		}
		$("#hand"+i).css({"background-image":"url("+$HANDPATH+tmp[num]+")"});
		$('#handcharprev'+i).css({"background-image":"url("+$CHARPATH+charimg[charnum]+")"});
		$('#handprev'+i).css({"background-image":"url("+$HANDPATH+tmp[num]+")"});
	}
	$("#prevarea").show();
}
//公開した手札を少し動かす。2013.11.08.add
function moveOpenHand(){
	for(var i=0;i<3;i++){
		for(var j=3;j<6;j++){
			if(handlist[i].char==handlist[j].char){
				$("#hand"+i).animate({"top":handlist[i].y+45,"left":handlist[i].x},1000);}
		}
	}
}

//手札反映
function cardEffect(){
	$("#refbutton").hide();//2013.11.10.add
	var tmpmovechar=new Array();
	var charlistlen=charlist.length;
	var tmpboardcount=new Array();
	for(var i=0;i<4;i++){
		tmpboardcount[i]={
			'yuko':0,
			'huan':0,
			'anyaku':0
		}
	}
	var fantasypos=charlist[19].nownum;
	for(var i=0;i<3;i++){
		tmpmovechar[i]=-1;
		var card=handlist[i].card;
		var char=handlist[i].char;
		switch(card){
			case 0://暗躍禁止
				break;
			case 1://友好＋２
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(handlist[3].char==char&&handlist[3].card==8||handlist[4].char==char&&handlist[4].card==8||handlist[5].char==char&&handlist[5].card==8)
						break;//友好禁止チェック
					tmpboardcount[char-charlistlen].yuko -= -2;
				}
				break;
			};//ボードには無効
			//友好禁止チェック
			if(handlist[3].char==char&&handlist[3].card==8||handlist[4].char==char&&handlist[4].card==8||handlist[5].char==char&&handlist[5].card==8){
				break;
			}
			//反映
				$("#con"+char+"n"+2).val(charlist[char].yuko-(-2));
				break;
			case 2://移動禁止
				break;
			case 3://不安-1
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(handlist[3].char==char&&handlist[3].card==9||handlist[4].char==char&&handlist[4].card==9||handlist[5].char==char&&handlist[5].card==9)
						break;//不安禁止チェック
					tmpboardcount[char-charlistlen].huan-=1;
				}
				break;
			};//ボードには無効
			//不安禁止禁止チェック
			if(handlist[3].char==char&&handlist[3].card==9||handlist[4].char==char&&handlist[4].card==9||handlist[5].char==char&&handlist[5].card==9){
				break;
			}
			//反映
				var tmp=$("#con"+char+"n"+3).val();
				$("#con"+char+"n"+3).val(tmp-1);
				break;
			case 4://移動↑↓
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(fantasypos==char-charlistlen){
						char=19;
					}else break;
				}else break;
			};//ボードには無効
				if(charlist[char].nownum==0){var next=1;}
				if(charlist[char].nownum==1){var next=0;}
				if(charlist[char].nownum==2){var next=3;}
				if(charlist[char].nownum==3){var next=2;}
				$('#con'+char+'n1').val(next);
				tmpmovechar[i]=char;
				//setnext(char,'con'+char+'n1');
				break;
			case 5://移動←→
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(fantasypos==char-charlistlen){
						char=19;
					}else break;
				}else	break;
			};//ボードには無効
				if(charlist[char].nownum==0){var next=2;}
				if(charlist[char].nownum==1){var next=3;}
				if(charlist[char].nownum==2){var next=0;}
				if(charlist[char].nownum==3){var next=1;}
				$('#con'+char+'n1').val(next);
				tmpmovechar[i]=char;
				//setnext(char,'con'+char+'n1');
				break;
			case 6://友好＋１
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(handlist[3].char==char&&handlist[3].card==8||handlist[4].char==char&&handlist[4].card==8||handlist[5].char==char&&handlist[5].card==8)
						break;//友好禁止チェック
					tmpboardcount[char-charlistlen].yuko-= -1;
				}
				break;
			};//ボードには無効
			//友好禁止チェック
			if(handlist[3].char==char&&handlist[3].card==8||handlist[4].char==char&&handlist[4].card==8||handlist[5].char==char&&handlist[5].card==8){
				break;
			}
			//反映
				$("#con"+char+"n"+2).val(charlist[char].yuko-(-1));
				break;
			case 7://不安＋１
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(handlist[3].char==char&&handlist[3].card==9||handlist[4].char==char&&handlist[4].card==9||handlist[5].char==char&&handlist[5].card==9)
						break;//不安禁止チェック
					tmpboardcount[char-charlistlen].huan-= -1;
				}
			break;
			};//ボードには無効
			//不安禁止禁止チェック
			if(handlist[3].char==char&&handlist[3].card==9||handlist[4].char==char&&handlist[4].card==9||handlist[5].char==char&&handlist[5].card==9){
				break;
			}
			//反映
			var tmp=$("#con"+char+"n"+3).val();
				$("#con"+char+"n"+3).val(tmp-(-1));
				break;
			case 8://ExAor不安－１
			if(custom!=2){break;}//custom=2（α版）以外は無効。
			if(char>=charlistlen){break;};//ボードには無効
			//不安禁止禁止チェック
			if(handlist[3].char==char&&handlist[3].card==9||handlist[4].char==char&&handlist[4].card==9||handlist[5].char==char&&handlist[5].card==9){
				break;
			}
			//反映
			var tmp=$("#con"+char+"n"+3).val();
			$("#con"+char+"n"+3).val(tmp-1);
			break;
		}
	}
	for(var i=3;i<6;i++){
		var card=handlist[i].card;
		var char=handlist[i].char;
//var gmhand = new Array("移動斜め","暗躍＋２","移動↑↓","移動←→","不安＋１","不安＋１","不安－１","暗躍＋１","友好禁止","不安禁止");
//var boardimg= new Array("hospital.png","city.png","shrine.png","school.png");
		switch(card){
			case 0://移動斜め
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(handlist[0].char==char&&handlist[0].card==2 || handlist[1].char==char&&handlist[1].card==2 || handlist[2].char==char&&handlist[2].card==2)
						break;//移動禁止チェック
					if(fantasypos==char-charlistlen){
						char=19;
					}else break;
				}else	break;
				
			};//ボードには無効
			//移動禁止チェック↓↓2013.06.23.add
			if(handlist[0].char==char&&handlist[0].card==2 || handlist[1].char==char&&handlist[1].card==2 || handlist[2].char==char&&handlist[2].card==2){
				break;
			}
			//↑↑2013.06.23.add
				var now=$('#con'+char+'n1').val();
				if(now==0){var next=3;}
				if(now==1){var next=2;}
				if(now==2){var next=1;}
				if(now==3){var next=0;}
				$('#con'+char+'n1').val(next);
				setnext(char,'con'+char+'n1');
				break;
			case 1://暗躍＋２
			//暗躍禁止チェック
			if(handlist[0].char==char&&handlist[0].card==0||handlist[1].char==char&&handlist[1].card==0||handlist[2].char==char&&handlist[2].card==0){
				//2枚以上出ていたら無効
				if(handlist[0].card==0&&handlist[1].card==0||handlist[0].card==0&&handlist[2].card==0||handlist[1].card==0&&handlist[2].card==0){
				}else{//1枚だけなら有効
					break;
				}
			}
			if(charlist[19].remove==0&&char>=charlistlen){//幻想用
				tmpboardcount[char-charlistlen].anyaku -= -2;
			}
			//反映
			var tmp=$("#con"+char+"n"+4).val();
				$("#con"+char+"n"+4).val(tmp-(-2));
				break;
			case 2://移動↑↓
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(handlist[0].char==char&&handlist[0].card==2 || handlist[1].char==char&&handlist[1].card==2 || handlist[2].char==char&&handlist[2].card==2)
						break;//移動禁止チェック
					//移動↑↓チェック
					if(handlist[0].char==char&&handlist[0].card==4 || handlist[1].char==char&&handlist[1].card==4 || handlist[2].char==char&&handlist[2].card==4)
						break;
					if(fantasypos==char-charlistlen)
						char=19;
				}else{
					break;
				}
			};//ボードには無効
			//移動禁止チェック
			if(handlist[0].char==char&&handlist[0].card==2 || handlist[1].char==char&&handlist[1].card==2 || handlist[2].char==char&&handlist[2].card==2){
				break;
			}
			//移動↑↓チェック
			if(handlist[0].char==char&&handlist[0].card==4 || handlist[1].char==char&&handlist[1].card==4 || handlist[2].char==char&&handlist[2].card==4){
				break;
			}
			//反映
			var now=$('#con'+char+'n1').val();
			if(now==0){var next=1;}
			if(now==1){var next=0;}
			if(now==2){var next=3;}
			if(now==3){var next=2;}
			$('#con'+char+'n1').val(next);
			setnext(char,'con'+char+'n1');
			break;
			case 3:////移動←→
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					if(handlist[0].char==char&&handlist[0].card==2 || handlist[1].char==char&&handlist[1].card==2 || handlist[2].char==char&&handlist[2].card==2)
						break;//移動禁止チェック
					//移動←→チェック
					if(handlist[0].char==char&&handlist[0].card==5 || handlist[1].char==char&&handlist[1].card==5 || handlist[2].char==char&&handlist[2].card==5)
						break;
					if(fantasypos==char-charlistlen){
						char=19;
					}else break;
				}else	break;
			};//ボードには無効
			//移動禁止チェック
			if(handlist[0].char==char&&handlist[0].card==2 || handlist[1].char==char&&handlist[1].card==2 || handlist[2].char==char&&handlist[2].card==2){
				break;
			}
			//移動←→チェック
			if(handlist[0].char==char&&handlist[0].card==5 || handlist[1].char==char&&handlist[1].card==5 || handlist[2].char==char&&handlist[2].card==5){
				break;
			}
			//反映
			var now=$('#con'+char+'n1').val();
			if(now==0){var next=2;}
			if(now==1){var next=3;}
			if(now==2){var next=0;}
			if(now==3){var next=1;}
			$('#con'+char+'n1').val(next);
			setnext(char,'con'+char+'n1');
			break;
			case 4://不安＋１
			case 5:
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					tmpboardcount[char-charlistlen].huan -= -1;
				}
			break;
			};//ボードには無効
				//反映
				var tmp=$("#con"+char+"n"+3).val();
				$("#con"+char+"n"+3).val(tmp-(-1));
				break;
			case 6://不安－１
			if(char>=charlistlen){
				if(charlist[19].remove==0){//幻想用
					tmpboardcount[char-charlistlen].huan -= 1;
				}
				break;
			};//ボードには無効
				//反映
				var tmp=$("#con"+char+"n"+3).val();
				$("#con"+char+"n"+3).val(tmp-1);
				break;
			case 7://暗躍＋１
				//暗躍禁止チェック
				if(handlist[0].char==char&&handlist[0].card==0||handlist[1].char==char&&handlist[1].card==0||handlist[2].char==char&&handlist[2].card==0){
					//2枚以上出ていたら無効
					if(handlist[0].card==0&&handlist[1].card==0||handlist[0].card==0&&handlist[2].card==0||handlist[1].card==0&&handlist[2].card==0){
					}else{//1枚だけなら有効
						break;
					}
				}
				if(charlist[19].remove==0&&char>=charlistlen){//幻想用
					tmpboardcount[char-charlistlen].anyaku -= -1;
				}
				//反映
				var tmp=$("#con"+char+"n"+4).val();
				$("#con"+char+"n"+4).val(tmp-(-1));
				break;
			case 8://友好禁止
			case 9://不安禁止
		}
	}

	for(var i=0;i<3;i++){
		if(tmpmovechar[i]!=-1){
			//$('#con'+tmpmovechar[i]+'n1').val();
			setnext(tmpmovechar[i],'con'+tmpmovechar[i]+'n1');
		}
	}
	if(charlist[19].remove==0){

		var fantasynow=$('#'+'con'+19+'n1'+ ' option:selected').val();//charlist[19].nextnum;
		for(var i=0;i<4;i++){
			if(fantasynow==i){
				//var tmp=$("#con"+19+"n"+2).val();
				$("#con"+19+"n"+2).val(charlist[19].yuko-(-tmpboardcount[i].yuko));
				//var tmp=$("#con"+19+"n"+3).val();
				$("#con"+19+"n"+3).val(charlist[19].huan-(-tmpboardcount[i].huan));
				//var tmp=$("#con"+19+"n"+4).val();
				$("#con"+19+"n"+4).val(charlist[19].anyaku-(-tmpboardcount[i].anyaku));
			}
		}
	}
	for(var i=0;i<charlistlen;i++){
		if($("#con"+i+"n"+3).val()<0){
			$("#con"+i+"n"+3).val(0);
		}
	}
}

function checkleader(i){
	if(handlist[i].order==0){
		$("#player"+i).html("");
		var img=$(document.createElement("img"));
		img.attr({'src':"../rooper/img/leader.png",'alt':"leader"+i,'id':"leader"+i});
		img.css({'width':$CARDWIDTH+'px','height':$CARDHEIGHT+'px'});
		$("#player"+i).append(img);
	}else{
		$("#player"+i).html("");
	}
}
			
			
			
/****************************************/
/*キャラクターカードクリックで選択*/
/*****************************************/
var selectchar_check=-1;//2013.11.08.change
function clickselectcharacard(){
	for(var i=0;i<charlist.length+boards.length;i++){
		if(i==19)continue;//幻想には設定しない
		$('#char'+i).data("num",i);
		$('#char'+i).click(function(){
			if(selectchar_check==-1)return;// 2013.11.08.change
			$('#plhand'+selectchar_check).val($(this).data("num"));
			selectchar('pl',selectchar_check);
		});
	}
	for(var i=3;i<6;i++){
		$('#hand'+i).data("num",i);
		$('#hand'+i).click(function(){
			if(i<selectchar_check){return;}
			$('#plhand'+selectchar_check).val(handlist[$(this).data("num")].char);
			selectchar('pl',selectchar_check);
		});
	}
}

function card_revive(i,j){
	switch(j){
		case 1:var cardname="yuko_plus_2";
		break;
		case 2:var cardname="idou_kinsi";
		break;
		case 3:var cardname="huan_minus_1_pl";
		break;
	}
	if(handlist[i][cardname]==0){return;}
	var answer=confirm("委員長の能力を使ってカードを主人公の手札に戻します。\n本当によいですか？");
	if(answer==true){
	}else{
		return;
	}

	handlist[i][cardname]=0;
	var pl="pl";
	var dis=disposable[j-1];
	$("#"+pl+"hand"+i+"cardimg"+j).css({"background-image":"url("+$HANDPATH+dis+".png)"});
	$("#sumiprev"+i+"hand"+j).css({"background-image":"url("+$HANDPATH+dis+".png)"});
	$("#sumi"+i+"hand"+j).remove();
	$("#"+pl+"hand"+i+"card"+j).show();
}
function card_revive_writer(j){
	switch(j){
		case 0:var cardname="idou_naname";
		break;
		case 1:var cardname="anyaku_plus_2";
		break;
	}
	if(handlist[$HERONUM][cardname]==0){return;}
	var answer=confirm("委員長の能力を使ってカードを脚本家の手札に戻します。\n本当によいですか？");
	if(answer==true){
	}else{
		return;
	}
	var pl="gm";
	var dis=disposable[j+3];
	$("#sumiprev"+3+"hand"+j).css({"background-image":"url("+$HANDPATH+dis+".png)"});

	for(var i=$HERONUM;i<$PLAYNUM;i++){
		handlist[i][cardname]=0;
		$("#"+pl+"hand"+i+"cardimg"+j).css({"background-image":"url("+$HANDPATH+dis+".png)"});
		$("#sumi"+i+"hand"+j).remove();
		$("#"+pl+"hand"+i+"card"+j).show();
	}
}

