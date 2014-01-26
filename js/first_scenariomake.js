//jQuery.event.add(window, "load",function(event){
//var CHARNUM=20;//2013/11/7追記
var path="../rooper/";
var samplepath='samplescenario/';//2013.11.25.add
var charArr=new Array("","男子学生","女子学生","お嬢様","巫女","刑事","サラリーマン","情報屋","医者","入院患者","委員長","イレギュラー","異世界人","神格","アイドル","マスコミ","大物","ナース","手先","学者","幻想");
var CHARNUM=charArr.length-1;
var scenariolist={}
scenariolist[6]={"tsubasawokudasai":"翼をください","tyoukoukoukyuunosangeki":"超高校級の惨劇"};
scenariolist[7]={"tamaranai":"惨劇したくてたまらない！","kagerou":"カゲロウデイズ","youkoso":"惨劇RoopeRχへようこそ","marudesaigonokibou":"まるで最後の希望の光と見間違う",
				"yuureibyoutou":"幽霊病棟","tuyoikyaraonnani":"強いキャラ女に偏りすぎじゃないっすかね？",
				"idoukinsituyoi":"移動禁止強い","ursiidaro":"シリアルキラーがいるぜ！嬉しいだろ？","cat":"ネコ"
				,"loversbom":"ラバーズ爆発","adultless":"大人はいません"};
scenariolist[8]={"sekaiwodamase":"世界を騙せ","koerubekiisssen":"超えるべき一線",
				"silverbullet":"銀の銃弾","jikoboueikinou":"自己防衛機能",
				"timeitekinazure":"致命的なズレ","mysterypokunai":"ミステリーっぽくはない",
				"anositaiha":"あの死体はいったい？"};
scenariolist[9]={"kodokunokakurenbo":"孤独ノ隠レンボ","jibunkansatunikki":"ジブン観察日記",
				"nisemonotyuuihou":"ニセモノ注意報","kanzenhanzailoveletter":"完全犯罪ラブレター",
				"sarumaneisutori":"猿マネ椅子盗りゲーム","daikoutennsi":"代行天使"};
scenariolist[10]={"watasijituha":"私、実は……","watasihahutuunoningen":"私は普通の人間",
				"tumerooper_another_1":"詰め惨劇","sekaidetattahitorinokimini":"世界でたった一人の君に伝わりますように",
				"kyokouhoukai":"虚構崩壊"};
/************************************************************************/
/***2013.11.25.add*******************************************************/
/************************************************************************/
function makeSampleScenarioList(flg){
	var select=$("#samplescenario");
	for(var i in scenariolist[flg]){
		select.append($(document.createElement("option")).val(i).text(scenariolist[flg][i]));
	}
}

function samplescenario(){
	var select=$("#samplescenario");
	if(select.val()==-1){sample.resetscenario();return;}
	sample.use=1;
	sample.resetchar();
	var $url;
	var dd= new Date();
	var flg=$("#custom").attr("value");
	$url=path+samplepath+select.val()+'.txt';
	$.ajax({
		url:$url,
		dataType:'csv',
		success:function(result){loadSampleScenario(result,flg)	}
	});
}

function loadSampleScenario(result,flg){
	var datarr=result.split("\n");//改行で分割
	var flg_open_or_close=0;
	var opentext="";
	var closetext="";
	for(var i=0;i<datarr.length;i++){//各行に対し操作
		//「//」より後はコメントとして除去
		if(datarr[i].indexOf("//")!=-1){var tmp=datarr[i].split("//");datarr[i]=tmp[0];}
		//空白除去
		datarr[i]=jQuery.trim(datarr[i]);if(datarr[i]=="")continue;
		var tmp=datarr[i].split(":");//「:」で分割
		switch(tmp[0]){
			case 'タイトル':$('#scenarioTitle').val(tmp[1]);break;
			case 'ループ回数':$('#sloop').val(tmp[1]);break;
			case '日数':sample.days(tmp[1]);break;
			case 'Y':sample.ruleY(tmp[1]);break;
			case 'X1':sample.ruleX(1,tmp[1]);break;case 'X2':sample.ruleX(2,tmp[1]);break;
			case '男子学生':case '女子学生':case 'お嬢様':case '巫女':case '刑事':case 'サラリーマン':case '情報屋':case '医者':case '入院患者':
			case '委員長':case 'イレギュラー':case '異世界人':case 'アイドル':case 'マスコミ':case '大物':case 'ナース':case '手先':
			case '学者':case '幻想':
				sample.selectchar(tmp[0],tmp[1]);break;
			case '神格':
				$("#sinkaku_add").val(tmp[2]);
				sample.selectchar(tmp[0],tmp[1]);break;
			case '#1':case '#2':case '#3':case '#4':case '#5':case '#6':case '#7':case '#8':case '#9':case '#10':
				sample.selectjiken(tmp[0].replace('#',''),tmp[1],tmp[2]);break;
			case 'open':flg_open_or_close=0;break;
			case 'close':flg_open_or_close=1;break;
			default:
				if(flg_open_or_close==0)opentext+=tmp[0]+'\n';
				if(flg_open_or_close==1)closetext+=tmp[0]+'\n';
		}
	}
	$("#opentext").text(opentext);
	$("#closetext").text(closetext);
}
var sample={};
sample.use=0;
sample.ruleY=function(val){
	$("#sruleY").val(val);
	for(var j=0,l=ruleY.length;j<l;j++){
		if(ruleY[j].name==val){
			RoleRuleY=ruleY[j].role;
			makecharRole();
			var ul=document.createElement("ul");$(ul).css({"list-style-type":"none"});for(var cnt=0;cnt<ruleY[j].role.length;cnt++){var li=document.createElement("li");li.innerHTML=ruleY[j].role[cnt];ul.appendChild(li);}//2013/3/7追記
			$("#ruleYrole").html(ul);//2013/3/7追記
			$("#ruleYskill").html(ruleY[j].rule);//2013/3/7追記
			$("#ruleYadd").val(ruleY[j].rule);//2013/3/7追記
			return;
		}
	}
}
sample.days=function(tmp){
	$('#sloopday').val(tmp);
	for(var i=0;i<=10;i++){
		if(i>tmp){$('#jikentr_'+i).hide();$('#sday'+i).val('');$('#shan'+i).val('');$('#kouka'+i).html('');
		}else{$('#jikentr_'+i).show();}
	}
}
sample.ruleY=function(val){
	$("#sruleY").val(val);
	for(var j=0,l=ruleY.length;j<l;j++){
		if(ruleY[j].name==val){
			RoleRuleY=ruleY[j].role;
			makecharRole();
			var ul=document.createElement("ul");$(ul).css({"list-style-type":"none"});for(var cnt=0;cnt<ruleY[j].role.length;cnt++){var li=document.createElement("li");li.innerHTML=ruleY[j].role[cnt];ul.appendChild(li);}//2013/3/7追記
			$("#ruleYrole").html(ul);//2013/3/7追記
			$("#ruleYskill").html(ruleY[j].rule);//2013/3/7追記
			$("#ruleYadd").val(ruleY[j].rule);//2013/3/7追記
			return;
		}
	}
}
sample.ruleX=function(num,val){
	$("#sruleX"+num).val(val);
	for(var j=0,l=ruleX.length;j<l;j++){
		if(ruleX[j].name==val){
				if(num==1)RoleRuleX1=ruleX[j].role;
				if(num==2)RoleRuleX2=ruleX[j].role;
				makecharRole();
				var ul=document.createElement("ul");$(ul).css({"list-style-type":"none"});for(var cnt=0;cnt<ruleX[j].role.length;cnt++){var li=document.createElement("li");li.innerHTML=ruleX[j].role[cnt];ul.appendChild(li);}//2013/3/7追記
				$("#ruleX"+num+"role").html(ul);//2013/3/7追記
				$("#ruleX"+num+"skill").html(ruleX[j].rule);//2013/3/7追記
				$("#ruleX"+num+"add").val(ruleX[j].rule);//2013/3/7追記
		}
	}
}
sample.resetchar=function(){
	for(var i=0;i<CHARNUM;i++){
		$('#usecheck_'+i).attr({"checked":false});
		$('#schar'+i).attr({'disabled':true});
		$('.shanopt'+(i- -1)).hide();
		$("#jobunbox"+i).html('');
		$("#skillbox"+i).html('');
		$("#jobun"+i).val('');
		$("#skill"+i).val('');
		if(i==12){
			$("#sinkaku_add").attr({'disabled':true});
		}
	}
}
sample.resetscenario=function(){
	$("#mainform")[0].reset();
	$("#ruleYrole").html('');
	$("#ruleYskill").html('');
	$("#ruleX1role").html('');
	$("#ruleX1skill").html('');
	$("#ruleX2role").html('');
	$("#ruleX2skill").html('');
	$('#opentext').text('');
	$('#closetext').text('');
	sample.resetchar();
	for(var daynum=1;daynum<11;daynum++){
		$("#kouka"+daynum).html('');
		if(daynum!=1)$("#jikentr_"+daynum).hide();
	}
	sample.use=0;
}
sample.selectchar=function(val,role){
	var i=charArr.indexOf(val)-1;
	$('#usecheck_'+i).attr({"checked":true});
	$('#schar'+i).attr({'disabled':false});
	$('.shanopt'+(i - -1)).show();
	if(i==12)$("#sinkaku_add").attr({'disabled':false});
	$("#jobunbox"+i).html(roleHashJobun[role]);
	$("#skillbox"+i).html(roleHashSkill[role]);
	$("#jobun"+i).val(roleHashJobun[role]);
	$("#skill"+i).val(roleHashSkill[role]);
	$('#schar'+i).val(role);
}

sample.selectjiken=function(daynum,accident,culprit){
	$('#sday'+daynum).val(accident);
	$("#kouka"+daynum).html(kouka[accident]+"<input type='hidden' name='kouka"+daynum+"' value='"+kouka[accident]+"'>");
	$('#shan'+daynum).val(culprit);
}

/*************************************************************************/
function changeselectbox(){
	//$('#rule2').hide();
	loadData();
	loadChar();
	checkbox_first();
	$("#samplescenario").change(function(){samplescenario();});//2013.11.25.add
	$("#submitbutton").click(function(){
		if(!document.getElementById("schar"+0)||$('#sruleY').val()=="ruleY"||$('#sruleX1').val()=="ruleX1"){
			alert("ルールが選択されていません");
			return false;
		}
		var cntA=0;
		var cntB=0;
		for(var i=0;i<CHARNUM;i++){//2013/11/7変更
			if(i==10){continue;}//イレギュラーは数えない。
			cntA-=-(document.getElementById("schar"+i).selectedIndex);
		}
		for(var i=0;i<charRoleList.length;i++){
			if(i==10){continue;}//イレギュラーは数えない。
			cntB+=i;
		}
		if(cntA!=cntB&&!($('#sruleX1').val()=="最低の脚本")&&sample.use==0){
			alert("割り振られていない役職があります");
			return false;
		}
		for(var i=1;i<=10;i++){
			if($("#sday"+i).val()!="" && $("#shan"+i).val()==""){
				alert(i+"日目の事件の犯人が決まっていません");
				return false;
			}
			if($("#sday"+i).val()=="" && $("#shan"+i).val()!=""){
				alert(i+"日目の事件が決まっていません");
				return false;
			}
		}
	});
}
//});

/****************************************************************/
//ファイル読み込み
/****************************************************************/
function loadData(){
	var $url;
	var dd= new Date();
	var flg=$("#custom").attr("value");
	makeSampleScenarioList(flg);//2013.11.25.add
	switch(flg){
	case "6":
		$url=path+"first/rule.csv";
		break;
	case "7":
		$url=path+"kai/rule.csv";
		break;
	case "8":
		$url=path+"MysteryCircle/rule.csv";
		break;
	case "9":
		$url=path+"HauntedStage/rule.csv";
		break;
	case "10"://2013.11.7追記
		$url=path+"AnotherHorizon/rule.csv";
		break;
	}

	$.ajax({
		url:$url,
		dataType:'csv',
		success:function(result){loadDataAfter(result,flg)	}
	});

}
/*=====================================================*/
//データ読み込み後処理
function loadDataAfter(result,flg){
	//データ解析
	var datarr=result.split("\n");//改行で分割
	for(var i=0;i<datarr.length;i++){
		if(datarr[i].indexOf("//")!=-1){
			var tmp=datarr[i].split("//");
			datarr[i]=tmp[0];
		}
		datarr[i]=jQuery.trim(datarr[i]);//空白除去
		var tmp = datarr[i].replace(/</g,"&lt;");
		tmp = tmp.replace(/>/g,"&gt;");
		tmp = tmp.replace(/\\n/g,"<br>");
		if(tmp=="")continue;
		makeRule(tmp);
	}
	changepulldown();
}


/*======================================================*/

function callbackFunc(result){}
/***********************************************************************************************************************************/
var ruleY = new Array();
var ruleX = new Array();
var roleList=new Array();
var boards=new Array();
var roleHashJobun={};
var roleHashSkill={};
function makeRule(dat){
	var tmparr=dat.split(",");//,で分割
	switch(tmparr[0]){
	case "boards":
		for(var i=0;i<4;i++){
		var tmpobj = new function(){
			this.name = tmparr[i+1];
		}
		boards.push(tmpobj);
		}
		break;
	case "role":
		var tmpobj = new function(){
			this.name = tmparr[1];
			this.max = tmparr[2];
			this.yukomusi=tmparr[3];
			this.noryoku=tmparr[4];
			if(tmparr[5]){
				var tmp = tmparr[5].split("+");
				this.rule=tmp;
			}else{this.rule=new Array();}
		}
		roleList.push(tmpobj);
		//↓↓2013/3/7追記
		switch(tmparr[3]){
			case "友好無視":
				roleHashJobun[tmparr[1]]="<font color='#b0e0e6'>友好無視</font>";
				break;
			case "絶対友好無視":
				roleHashJobun[tmparr[1]]="<strong><font color='#b0e0e6'>絶対友好無視</font></strong>";
				break;
			case "死後活性":
				roleHashJobun[tmparr[1]]="<font color='#ffff00'>死後活性</font>";
				break;
			case "友好暴発"://2013.11.7追記
				roleHashJobun[tmparr[1]]="<font color='#ff4500'>友好暴発</font>";
				break;
			case "表裏選択"://2013.11.7追記
				roleHashJobun[tmparr[1]]="<font color='#00ff7f'>表裏選択</font>";
				break;
			default:
				roleHashJobun[tmparr[1]]=tmparr[3];
		}
		roleHashSkill[tmparr[1]]=tmparr[4];
		//↑↑2013/3/7追記
		break;
	default:
		var tmpobj=new function(){
			this.name=tmparr[1];
			if(tmparr[2]){
				var tmp = tmparr[2].split("+");
				this.role=tmp;
			}else{this.role=new Array();}
			this.rule=tmparr[3];
		}
		if(tmparr[0]=="Y")ruleY.push(tmpobj);
		if(tmparr[0]=="X")ruleX.push(tmpobj);
	}
}
var RoleRuleY=new Array();;
var RoleRuleX1=new Array();;
var RoleRuleX2=new Array();;
var namelist=["shonen","shojo","ojo","miko","keiji","salary","joho","isha","kanja"];
function changepulldown(){
	//ルール作成
	var rule =new Array("ruleY","ruleX1","ruleX2");
	var ruleArr=new Array(ruleY,ruleX,ruleX);
	var tmp;
	//2013/3/7追記↓↓

	$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","id":"ruleYadd","name":"ruleYadd"}));
	$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","id":"ruleX1add","name":"ruleX1add"}));
	$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","id":"ruleX2add","name":"ruleX2add"}));

	//2013/3/7追記↑↑
	for(var i=0;i<rule.length;i++){
		tmp=$(document.createElement("select"));
		$("#"+rule[i]).html("").append(tmp);
		tmp.attr({"name":rule[i],"id":"s"+rule[i]});
		tmp.change(function(){
			if(this.selectedIndex==0){
				if(this.id=="sruleY"){RoleRuleY=new Array();}
				if(this.id=="sruleX1"){RoleRuleX1=new Array();}
				if(this.id=="sruleX2"){RoleRuleX2=new Array();}
					makecharRole();
				return;
			}
			if($("#sruleX1").val()==$("#sruleX2").val()&&this.selectedIndex!=0){
				alert(this.value+"は既に選択されています。");
				this.selectedIndex=0;
				return;
			}
			if(this.id=="sruleY"){
				for(var j=0;j<ruleY.length;j++){
					if(ruleY[j].name==this.value){
						RoleRuleY=ruleY[j].role;
						makecharRole();
						var ul=document.createElement("ul");$(ul).css({"list-style-type":"none"});for(var cnt=0;cnt<ruleY[j].role.length;cnt++){var li=document.createElement("li");li.innerHTML=ruleY[j].role[cnt];ul.appendChild(li);}//2013/3/7追記
						$("#ruleYrole").html(ul);//2013/3/7追記
						$("#ruleYskill").html(ruleY[j].rule);//2013/3/7追記
						$("#ruleYadd").val(ruleY[j].rule);//2013/3/7追記
						return;
					}
				}
				alert("!");
			}else{
				for(var j=0;j<ruleX.length;j++){
					if(ruleX[j].name==this.value){
						if(this.id=="sruleX1"){
							RoleRuleX1=ruleX[j].role;
							var ul=document.createElement("ul");$(ul).css({"list-style-type":"none"});for(var cnt=0;cnt<ruleX[j].role.length;cnt++){var li=document.createElement("li");li.innerHTML=ruleX[j].role[cnt];ul.appendChild(li);}//2013/3/7追記
							$("#ruleX1role").html(ul);//2013/3/7追記
							$("#ruleX1skill").html(ruleX[j].rule);//2013/3/7追記
							$("#ruleX1add").val(ruleX[j].rule);//2013/3/7追記
						}else{
							RoleRuleX2=ruleX[j].role;
							var ul=document.createElement("ul");$(ul).css({"list-style-type":"none"});for(var cnt=0;cnt<ruleX[j].role.length;cnt++){var li=document.createElement("li");li.innerHTML=ruleX[j].role[cnt];ul.appendChild(li);}//2013/3/7追記
							$("#ruleX2role").html(ul);//2013/3/7追記
							$("#ruleX2skill").html(ruleX[j].rule);//2013/3/7追記
							$("#ruleX2add").val(ruleX[j].rule);//2013/3/7追記
						}
						makecharRole();
						return;
					}
				}
			}
			
		});
		tmp.append($(document.createElement("option")).attr({"value":rule[i]}).text(rule[i]).val(rule[i]));
		for(var cnt=0;cnt<ruleArr[i].length;cnt++){
			var option =$(document.createElement("option"));
//				if(i==2&&cnt==1){option.attr({"selected":true});}
				option.text(ruleArr[i][cnt].name);
				option.val(ruleArr[i][cnt].name);
			tmp.append(option);
		}
	}
	var loopday=10;
	//2013/3/7追記↓↓

	$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","name":"selectedversion","id":"selectedversion","value":"selectedversion"}));
	//2013/3/7追記↑↑
	for(var i=0;i<CHARNUM;i++){//2013/11/7変更
		$("#char"+i).html("<input type='hidden' name='"+namelist[i]+"' value='パーソン'>");
		//2013/3/7追記↓↓
		$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","id":"jobun"+i,"name":"jobun"+i}));
		$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","id":"skill"+i,"name":"skill"+i}));
		//2013/3/7追記↑↑
	}
	makecharRole();//2013.5.17.add
	if($("#custom").attr("value")=="6"){
		jiken=new Array("","殺人事件","不安拡大","自殺","病院の事件","遠隔殺人","行方不明","流布");
		kouka={"":"","殺人事件":"犯人と同一エリアにいる犯人以外の任意のキャラクター１人を死亡させる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","自殺":"犯人は死亡する。","病院の事件":"病院に[暗躍カウンター]が１つ以上→病院にいる全てのキャラクターを死亡させる。病院に[暗躍カウンター]が２つ以上→主人公を死亡させる。","遠隔殺人":"[暗躍カウンター]が２つ以上置かれたキャラクター１人を死亡させる","行方不明":"犯人を任意のボードに移動させる。その後、犯人のいるボードに[暗躍カウンター]を１つ置く","流布":"任意のキャラクター１人から[友好カウンター]を２つ取り除き、別のキャラクター１人に[友好カウンター]を２つ置く。"};
	}else if($("#custom").attr("value")=="7"){
		jiken=new Array("","殺人事件","不安拡大","邪気の汚染","自殺","病院の事件","遠隔殺人","行方不明","流布","蝶の羽ばたき");
		kouka={"":"","殺人事件":"犯人と同一エリアにいる犯人以外の任意のキャラクター１人を死亡させる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","邪気の汚染":"神社に[暗躍カウンター]を２つ置く。","自殺":"犯人は死亡する。","病院の事件":"病院に[暗躍カウンター]が１つ以上→病院にいる全てのキャラクターを死亡させる。病院に[暗躍カウンター]が２つ以上→主人公を死亡させる。","遠隔殺人":"[暗躍カウンター]が２つ以上置かれたキャラクター１人を死亡させる","行方不明":"犯人を任意のボードに移動させる。その後、犯人のいるボードに[暗躍カウンター]を１つ置く","流布":"任意のキャラクター１人から[友好カウンター]を２つ取り除き、別のキャラクター１人に[友好カウンター]を２つ置く。","蝶の羽ばたき":"犯人と同一エリアにいるキャラクター1人にいずれかのカウンターを１つ置く。"};
	}else if($("#custom").attr("value")=="8"){
		jiken=new Array("","殺人事件","不安拡大","自殺","病院の事件","遠隔殺人","行方不明","流布","蝶の羽ばたき","テロリズム","前兆","猟奇殺人","偽装自殺","不和","クローズドサークル","銀の銃弾","連続殺人","集団自殺");
		 kouka={"":"","殺人事件":"犯人と同一エリアにいる犯人以外の任意のキャラクター１人を死亡させる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","自殺":"犯人は死亡する。","病院の事件":"病院に[暗躍カウンター]が１つ以上→病院にいる全てのキャラクターを死亡させる。病院に[暗躍カウンター]が２つ以上→主人公を死亡させる。","遠隔殺人":"[暗躍カウンター]が２つ以上置かれたキャラクター１人を死亡させる","行方不明":"犯人を任意のボードに移動させる。その後、犯人のいるボードに[暗躍カウンター]を１つ置く","流布":"任意のキャラクター１人から[友好カウンター]を２つ取り除き、別のキャラクター１人に[友好カウンター]を２つ置く。","蝶の羽ばたき":"犯人と同一エリアにいるキャラクター1人にいずれかのカウンターを１つ置く。","テロリズム":"都市に暗躍カウンターが１つ以上置かれている場合、都市にいるキャラクター全員が死亡する。さらに、都市に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。","前兆":"＜不安臨界－１＞犯人と同じエリアにいるキャラクター１人に不安カウンターを１つ置く。","猟奇殺人":"＜不安臨界＋１＞＜Exゲージ非増加＞「殺人事件」と「不安拡大」をこの順で発生させる。（結果、Exゲージは２増加する）","偽装自殺":"犯人にExカードAを置く。ExカードAが置かれたキャラクターに主人公はカードを置くことができない。","不和":"犯人と同じエリアにいるキャラクターのうち、友好カウンターの置かれた１人からすべての友好カウンターを取り除く。","クローズドサークル":"犯人のいるボードを指定する。事件発生の日を含め３日間、そのボードからの移動とボードへの移動を禁止する。","銀の銃弾":"＜Exゲージ非増加＞このフェイズの終了時にループを終了させる。","連続殺人":"可能ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。他の連続殺人の犯人となっているキャラクターを事件の犯人とすることができる。","集団自殺":"犯人に[暗躍カウンター]が１つ以上→犯人と同じエリアにいるキャラクター全てを死亡させる。"};
	
	}else if($("#custom").attr("value")=="9"){
		 jiken=new Array("","連続殺人","不安拡大","集団自殺","病院の事件","代行者","冒涜","魔獣の解放","百鬼夜行","呪怨","蔓延","繰り返す悪夢");
		 kouka={"":"","連続殺人":"可能ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。他の連続殺人の犯人となっているキャラクターを事件の犯人とすることができる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","集団自殺":"犯人に[暗躍カウンター]が１つ以上→犯人と同じエリアにいるキャラクター全てを死亡させる。","病院の事件":"病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。","代行者":"＜不安臨界－２＞Exゲージを１増加させ、リーダーであるプレイヤーはキャラクターを１人選ぶ。そのキャラクターを死亡させる。","冒涜":"任意の死体１つに[不安カウンター]と[暗躍カウンター]を１つずつ置く。","魔獣の解放":"犯人のいるエリアに「魔獣」カードを置く。以降、そのカードは「魔獣」という名前の役職がナイトメアであるキャラクターとして扱う。","百鬼夜行":"＜死後発生＞神社に[暗躍カウンター]が１つ以上→Exゲージを４増加させる。","呪怨":"＜死後発生＞犯人と同じエリアにあるカード１つを任意の別のボードに移動させる。","蔓延":"＜死後発生＞犯人のいるボードに［暗躍カウンター］を２つ置く。","繰り返す悪夢":"＜死後発生＞Exゲージを1増加させ、犯人は蘇生する。"};
	}else if($("#custom").attr("value")=="10"){
		 jiken=new Array("","狂気殺人","洗脳工作","行方不明","病院の事件","異界漂流","暗殺","世界崩壊","世界収束","小さな力","打開","告白");
		 kouka={"":"","狂気殺人":"犯人と同一エリアにいる任意のキャラクター１人を死亡させる。","洗脳工作":"任意のキャラクター１人に[不安カウンター]を２つ置き、別の任意のキャラクター１人に[友好カウンター]を２つ置く。","行方不明":"犯人を任意のボードに移動させる。その後、犯人のいるボードに[暗躍カウンター]を１つ置く","病院の事件":"病院に[暗躍カウンター]が１つ以上→病院にいる全てのキャラクターを死亡させる。病院に[暗躍カウンター]が２つ以上→主人公を死亡させる。","異界漂流":"学校に[暗躍カウンター]が１つ以上→学校にいる全てのキャラクターを死亡させる。学校に[暗躍カウンター]が２つ以上→主人公を死亡させる。","暗殺":"犯人と同一エリアか、犯人と対角線上にあるボードにいる犯人以外の任意のキャラクター１人を死亡させる。この事件が発生するか判定するとき、本来のカウンターの代わりに[暗躍カウンター]の個数を参照する。","世界崩壊":"表世界にいる場合、主人公とすべてのキャラクターは死亡する。","世界収束":"表世界へと移るように世界移動を行う。その後、このループの間の世界移動を禁止する。","小さな力":"リーダーであるプレイヤーはキャラクター１人と[友好カウンター][不安カウンター][暗躍カウンター]から１種を選ぶ。そのキャラクターに選ばれたカウンターを1つ置く。この事件は犯人の不安臨界を1少ないものとして判定する。","打開":"リーダーであるプレイヤーはキャラクター1人かボード1つを選ぶ。そこから[暗躍カウンター]を2つ取り除く。","告白":"犯人の役職を知る"};
	}else{
		 jiken=new Array("","殺人事件","不安拡大","自殺","病院の事件","邪気の汚染","別離","暴露");
		kouka={"":"","殺人事件":"可能ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","自殺":"犯人は死亡する。","病院の事件":"病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。","邪気の汚染":"神社に暗躍カウンターを２つ置く。","別離":"犯人を任意のボードに移動させる。","暴露":"どちらかを選ぶ。１．犯人と同じエリアにいるキャラクターから友好カウンターを２つまで取り除く（２人に割り振ってもよい）。２．犯人と同じエリアにいるキャラクターに友好カウンターを２つまで置く（２人に割り振ってもよい）。"};
	}
	for(var i=1;i<=loopday;i++){
		tmp=$(document.createElement("select"));
		$("#day"+i).html("").append(tmp);
		$("#kouka"+i).html("");
		tmp.attr({"name":"day"+i,"id":"sday"+i});
		tmp.data("i",i);
		tmp.change(function(){
			
			$("#kouka"+$(this).data("i")).html(kouka[this.value]+"<input type='hidden' name='kouka"+$(this).data("i")+"' value='"+kouka[this.value]+"'>");
		});
		for(var cnt=0;cnt<jiken.length;cnt++){
			var option =$(document.createElement("option"));
				option.text(jiken[cnt]);
				option.val(jiken[cnt]);
				if(cnt==0){option.text("なし");}
			tmp.append(option);
		}
		tmp=$(document.createElement("select"));
		tmp.attr({"name":"han"+i,"id":"shan"+i});
		tmp.data({"i":i});
		$("#han"+i).html("").append(tmp);
		tmp.change(function(){
			for(var x=1;x<10;x++){
				if($(this).val()==$("#shan"+x).val()&&this.selectedIndex!=0&&this.id!="shan"+x){
					if($("#sday"+$(this).data("i")).val()=="連続殺人"&&$("#sday"+x).val()=="連続殺人"){return;}
					alert(this.value+"は既に選択されています。");
					this.selectedIndex=0;
					return;
				}
			}
		});
		for(var cnt=0;cnt<CHARNUM+1;cnt++){
			var option =$(document.createElement("option"));
				option.text(charArr[cnt]);
				option.attr({"class":"shanopt"+cnt});
				if(cnt==0||cnt==1||cnt==2||cnt==4||cnt==6||cnt==8||cnt==9){
				}else{
					option.css({"display":"none"});
				}
				option.val(charArr[cnt]);
				if(cnt==0){option.text("なし");}
			tmp.append(option);
		}
	}

	tmp=$(document.createElement("select")).attr({"name":"loop","id":"sloop"});
	$("#loop").html("").append(tmp);
	for(var i=1;i<=10;i++){
		var option =$(document.createElement("option"));
			option.text(i);
			option.val(i);
		if(i==4){option.attr({"selected":true});}
		tmp.append(option);
	}
	tmp=$(document.createElement("select")).attr({"name":"loopday","id":"sloopday"})
		.change(function(){for(var i=0;i<11;i++){if(i>$('#sloopday').val()){$('#jikentr_'+i).hide();$('#sday'+i).val('');$('#shan'+i).val('');$('#kouka'+i).html('');}else $('#jikentr_'+i).show();}});//2013.11.25.add
	$('#jikentr_9').hide();$('#jikentr_10').hide();//2013.11.25.add
	$("#loopday").html("").append(tmp);
	for(var i=1;i<=10;i++){
		var option =$(document.createElement("option"));
			option.text(i);
			option.val(i);
			if(i==8){option.attr({"selected":true});}
		tmp.append(option);
	}
	//5/22/add
	tmp=$(document.createElement("select"))
		.attr({"name":"sinkaku_add_loop","disabled":"true","id":"sinkaku_add"});
	$("#sinkaku_add_loop").html("").append(tmp);
	for(var i=1;i<=10;i++){
		var option =$(document.createElement("option"));
			option.text(i);
			option.val(i);
			if(i==4){option.attr({"selected":true});}
		tmp.append(option);
	}

}

/////////////////////////////////////////////////////////////////////
var charRoleList=new Array("パーソン");
var IrregularRoleList=new Array("パーソン");
function makecharRole(){
	charRoleList=new Array("パーソン");
	IrregularRoleList=new Array("パーソン");
//	alert(RoleRuleY[0]);
	if(RoleRuleY)charRoleList=charRoleList.concat(RoleRuleY);
	if(RoleRuleX1)charRoleList=charRoleList.concat(RoleRuleX1);
	if(RoleRuleX2)charRoleList=charRoleList.concat(RoleRuleX2);
	for(var i=0;i<roleList.length;i++){
		if(roleList[i].max=="")continue;
		var count=0;
		for(var j=0;j<charRoleList.length;j++){
			if(charRoleList[j]==roleList[i].name){
				if(count<roleList[i].max){
					count++;
				}else{
					charRoleList.splice(j,1);
				}
			}
		}
	}
	for(var i=0;i<CHARNUM;i++){//2013/11/7変更

		//↓↓2013/3/7追記
		$("#jobunbox"+i).html("");
		$("#skillbox"+i).html("");
		$("#jobun"+i).val("");
		$("#skill"+i).val("");
		//↑↑2013/3/7追記
		tmp=$(document.createElement("select")).attr({"name":'char'+i,"id":"schar"+i}).data({"i":i});
		if(!$('#usecheck_'+i).attr('checked')){
			tmp.attr({'disabled':true});
		}

		$("#char"+i).html("").append(tmp);
		tmp.change(function(){
			for(var x=0;x<CHARNUM;x++){//2013/11/7変更
				if($(this).data("i")==10){break;}
				if(x!=10&&document.getElementById("schar"+x).selectedIndex==this.selectedIndex&&this.selectedIndex!=0&&this.id!="schar"+x){
					alert(this.value+"は既に選択されています。");
					this.selectedIndex=0;
					return;
				}
			}
				$("#jobunbox"+$(this).data("i")).html(roleHashJobun[this.value]);
				$("#skillbox"+$(this).data("i")).html(roleHashSkill[this.value]);
				$("#jobun"+$(this).data("i")).val(roleHashJobun[this.value]);
				$("#skill"+$(this).data("i")).val(roleHashSkill[this.value]);
		});
		if(i==10){//イレギュラー専用。
			for(var cnt=0,len=roleList.length;cnt<len;cnt++){
				Irregular_Role_check=0;
				for(var j=0,jlen=charRoleList.length;j<jlen;j++){
					if(charRoleList[j]==roleList[cnt].name){
						Irregular_Role_check=1;
						break;
					}
				}
				if(Irregular_Role_check==1){continue;}
				var option =$(document.createElement("option"));
					option.text(roleList[cnt].name);
					option.val(roleList[cnt].name);
				tmp.append(option);
			}
			if($('#usecheck_10').attr('checked')){
				$("#jobunbox10").html(roleHashJobun[$('#schar10').val()]);
				$("#skillbox10").html(roleHashSkill[$('#schar10').val()]);
				$("#jobun10").val(roleHashJobun[$('#schar10').val()]);
				$("#skill10").val(roleHashSkill[$('#schar10').val()]);
			}
			continue;
		}
		for(var cnt=0;cnt<charRoleList.length;cnt++){
			var option =$(document.createElement("option"));
				option.text(charRoleList[cnt]);
				option.val(charRoleList[cnt]);
			tmp.append(option);
		}
	}
}
/****************************************************************/
//キャラクタファイル読み込み
/****************************************************************/
function loadChar(){
	var filename="char.csv";
	$.ajax({
		url:path+"kai/char.csv",
		dataType:'csv',
		success:function(result){After(result,filename)	}
	});
}

/*=====================================================*/
//データ読み込み後処理
function After(result,filename){
	//データ解析
	var datarr=result.split("\n");//改行で分割
	var cnt=0;
	for(var i=0;i<datarr.length;i++){
		if(datarr[i].indexOf("//")!=-1){
			var tmp=datarr[i].split("//");
			datarr[i]=tmp[0];
		}
		datarr[i]=jQuery.trim(datarr[i]);//空白除去
		var tmp = datarr[i].replace(/</g,"&lt;");
		tmp = tmp.replace(/>/g,"&gt;");
		tmp = tmp.replace(/\\n/g,"<br>");
		if(tmp=="")continue;
		if(filename=="char.csv"){
			makeChar(tmp,cnt);
		}
		cnt++;
	}
}
function makeChar(dat,cnt){
	var chararr=dat.split(",");//,で分割
		//名前を定義
	document.getElementById("customcharnameprev"+cnt).innerHTML=chararr[0];
	document.getElementById("customcharname"+cnt).value=chararr[0];
}

/***********************************************************************/
function checkbox_first(){
	for(var i=0;i<CHARNUM;i++){//2013/11/7変更
		$('#usecheck_'+i).data("i",i).click(
		function(){box_click($(this).data("i"));});
	}
}
function box_click(cnt){
	if($('#usecheck_'+cnt).attr('checked')){
		$('#schar'+cnt).attr({'disabled':false});
		$('.shanopt'+(cnt - -1)).show();
		if(cnt==10){
			$("#jobunbox10").html(roleHashJobun[$('#schar10').val()]);
			$("#skillbox10").html(roleHashSkill[$('#schar10').val()]);
			$("#jobun10").val(roleHashJobun[$('#schar10').val()]);
			$("#skill10").val(roleHashSkill[$('#schar10').val()]);
		}else if(cnt==12){
			$("#sinkaku_add").attr({'disabled':false});
		}
	}else{
		$('#schar'+cnt).attr({'disabled':true});
		$('.shanopt'+(cnt- -1)).hide();
		if(cnt==12){
			$("#sinkaku_add").attr({'disabled':true});
		}
	}
}


