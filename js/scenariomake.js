//jQuery.event.add(window, "load",function(event){
var path="../rooper/";
function changeselectbox(){
	loadData();
	$("#submitbutton").click(function(){
		if(!document.getElementById("schar"+0)){
			alert("ルールが選択されていません");
			return false;
		}
		var cntA=0;
		var cntB=0;
		for(var i=0;i<9;i++){
			cntA-=-(document.getElementById("schar"+i).selectedIndex);
		}
		for(var i=0;i<charRoleList.length;i++){
			cntB+=i;
		}
		if(cntA!=cntB){
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
	switch(flg){
	case "0":
		$url=path+"def/rule.csv";
		break;
	case "1":
		return;
		$url=path+"custom/rule.csv";
		break;
	case "2":
		
		$url=path+"alpha/rule.csv";
		break;
	case "3":
		$url=path+"VisualNovel/rule.csv";
		break;
	case "4":
		$url=path+"HauntedStage/rule.csv";
		break;
	case "5":
		$url=path+"MysteryCircle/rule.csv";
		break;
	case "6":
		$url=path+"first/rule.csv";
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
	$("#ruleY").after($(document.createElement("td")).attr({"id":"ruleYskill"}).css({"width":"500px"}));
	$("#ruleX1").after($(document.createElement("td")).attr({"id":"ruleX1skill"}).css({"width":"500px"}));
	$("#ruleX2").after($(document.createElement("td")).attr({"id":"ruleX2skill"}).css({"width":"500px"}));
	$("#ruleY").after($(document.createElement("td")).attr({"id":"ruleYrole"}).css({"width":"150px"}));
	$("#ruleX1").after($(document.createElement("td")).attr({"id":"ruleX1role"}).css({"width":"150px"}));
	$("#ruleX2").after($(document.createElement("td")).attr({"id":"ruleX2role"}).css({"width":"150px"}));
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
	$("#chartablehead").append($(document.createElement("th")).text("条文能力").css({"width":"140px"}));
	$("#chartablehead").append($(document.createElement("th")).text("能力").css({"width":"500px"}));
	$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","name":"selectedversion","id":"selectedversion","value":"selectedversion"}));
	//2013/3/7追記↑↑
	for(var i=0;i<9;i++){
		$("#char"+i).html("パーソン<input type='hidden' name='"+namelist[i]+"' value='パーソン'>");
		//2013/3/7追記↓↓
		$("#char"+i).after($(document.createElement("td")).attr({"id":"jobunbox"+i}));
		$("#jobunbox"+i).after($(document.createElement("td")).attr({"id":"skillbox"+i}));
		$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","id":"jobun"+i,"name":"jobun"+i}));
		$("#mainform").append($(document.createElement("input")).attr({"type":"hidden","id":"skill"+i,"name":"skill"+i}));
		//2013/3/7追記↑↑
	}
	if($("#custom").attr("value")=="2"){
		var jiken=new Array("","殺人事件","不安拡大","自殺","病院の事件","邪気の汚染");
		var kouka={"":"","殺人事件":"可能ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","自殺":"犯人は死亡する。","病院の事件":"病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。"};
		
	}else if($("#custom").attr("value")=="3"){
		var jiken=new Array("","殺人事件","不安拡大","邪気の汚染","別離","暴露","テロリズム","不和","クローズドサークル","ルート確定","ときめく爆弾","引越し");
		var kouka={"":"","殺人事件":"可能ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","邪気の汚染":"神社に暗躍カウンターを２つ置く。","別離":"犯人を任意のボードに移動させる。","暴露":"どちらかを選ぶ。１．犯人と同じエリアにいるキャラクターから友好カウンターを２つまで取り除く（２人に割り振ってもよい）。２．犯人と同じエリアにいるキャラクターに友好カウンターを２つまで置く（２人に割り振ってもよい）。","テロリズム":"都市に暗躍カウンターが１つ以上置かれている場合、都市にいるキャラクター全員が死亡する。さらに、都市に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。","不和":"犯人と同じエリアにいるキャラクターのうち友好カウンターの置かれた一人から友好カウンターをすべて取り除く","クローズドサークル":"犯人のいるボードを指定する。事件発生の日を含み３日間、そのボードからの移動とそのボードへの移動を禁止する","ルート確定":"事件が起こり、かつ犯人の友好能力が１つでも使用できるだけの友好カウンターが乗っている時、犯人の役職をそのループ中キーパーソンに変更する。","ときめく爆弾":"事件が起こり、かつ犯人に友好カウンターが１つも乗っていない場合、EXカウンターを用意する。初期値は０である。その日からターン終了フェイズごとにEXカウンターが１ずつ増加する。３になった時点で全てのキャラクターの友好カウンターが２減少する。犯人に友好カウンターを乗せるとEXカウンターの値は０になる。","引越し":"以降、犯人を全てのボードにいないものとして扱い、カードをセットすることもできなくなる。"};
	}else if($("#custom").attr("value")=="4"){
		loopday=11;
		var jiken=new Array("","連続殺人","不安拡大","集団自殺","病院の事件","代行者","冒涜","魔獣の解放","百鬼夜行","呪怨","蔓延","繰り返す悪夢");
		var kouka={"":"","連続殺人":"可能ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。他の連続殺人の犯人となっているキャラクターを事件の犯人とすることができる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","集団自殺":"犯人に[暗躍カウンター]が１つ以上→犯人と同じエリアにいるキャラクター全てを死亡させる。","病院の事件":"病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。","代行者":"＜不安臨界－２＞Exゲージを１増加させ、リーダーであるプレイヤーはキャラクターを１人選ぶ。そのキャラクターを死亡させる。","冒涜":"任意の死体１つに[不安カウンター]と[暗躍カウンター]を１つずつ置く。","魔獣の解放":"犯人のいるエリアに「魔獣」カードを置く。以降、そのカードは「魔獣」という名前の役職がナイトメアであるキャラクターとして扱う。","百鬼夜行":"＜死後発生＞神社に[暗躍カウンター]が１つ以上→Exゲージを４増加させる。","呪怨":"＜死後発生＞犯人と同じエリアにあるカード１つを任意の別のボードに移動させる。","蔓延":"＜死後発生＞犯人のいるボードに［暗躍カウンター］を２つ置く。","繰り返す悪夢":"＜死後発生＞Exゲージを1増加させ、犯人は蘇生する。"};
	}else if($("#custom").attr("value")=="5"){
		loopday=11;
		var jiken=new Array("","殺人事件","不安拡大","自殺","病院の事件","テロリズム","前兆","猟奇殺人","偽装自殺","不和","クローズドサークル","銀の銃弾");
		var kouka={"":"","殺人事件":"可能ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","自殺":"犯人は死亡する。","病院の事件":"病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。","テロリズム":"都市に暗躍カウンターが１つ以上置かれている場合、都市にいるキャラクター全員が死亡する。さらに、都市に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。","前兆":"＜不安臨界－１＞犯人と同じエリアにいるキャラクター１人に不安カウンターを１つ置く。","猟奇殺人":"＜不安臨界＋１＞＜Exゲージ非増加＞「殺人事件」と「不安拡大」をこの順で発生させる。（結果、Exゲージは２増加する）","偽装自殺":"犯人にExカードAを置く。ExカードAが置かれたキャラクターに主人公はカードを置くことができない。","不和":"犯人と同じエリアにいるキャラクターのうち、友好カウンターの置かれた１人からすべての友好カウンターを取り除く。","クローズドサークル":"犯人のいるボードを指定する。事件発生の日を含め３日間、そのボードからの移動とボードへの移動を禁止する。","銀の銃弾":"＜Exゲージ非増加＞このフェイズの終了時にループを終了させる。"};
	}else{
		var jiken=new Array("","殺人事件","不安拡大","自殺","病院の事件","邪気の汚染","別離","暴露");
		var kouka={"":"","殺人事件":"可能ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。","不安拡大":"任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。","自殺":"犯人は死亡する。","病院の事件":"病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。","邪気の汚染":"神社に暗躍カウンターを２つ置く。","別離":"犯人を任意のボードに移動させる。","暴露":"どちらかを選ぶ。１．犯人と同じエリアにいるキャラクターから友好カウンターを２つまで取り除く（２人に割り振ってもよい）。２．犯人と同じエリアにいるキャラクターに友好カウンターを２つまで置く（２人に割り振ってもよい）。"};
	}
	var charArr=new Array("","男子学生","女子学生","お嬢様","巫女","刑事","サラリーマン","情報屋","医者","入院患者");
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
		for(var cnt=0;cnt<charArr.length;cnt++){
			var option =$(document.createElement("option"));
				option.text(charArr[cnt]);
				option.val(charArr[cnt]);
				if(cnt==0){option.text("なし");}
			tmp.append(option);
		}
	}

	tmp=$(document.createElement("select")).attr({"name":"loop"});
	$("#loop").html("").append(tmp);
	for(var i=1;i<=10;i++){
		var option =$(document.createElement("option"));
			option.text(i);
			option.val(i);
		if(i==4){option.attr({"selected":true});}
		tmp.append(option);
	}
	tmp=$(document.createElement("select")).attr({"name":"loopday"});
	$("#loopday").html("").append(tmp);
	for(var i=1;i<=10;i++){
		var option =$(document.createElement("option"));
			option.text(i);
			option.val(i);
			if(i==8){option.attr({"selected":true});}
		tmp.append(option);
	}
}

/////////////////////////////////////////////////////////////////////
var charRoleList=new Array("パーソン");
function makecharRole(){
	charRoleList=new Array("パーソン");
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
	for(var i=0;i<9;i++){
		//↓↓2013/3/7追記
		$("#jobunbox"+i).html("");
		$("#skillbox"+i).html("");
		$("#jobun"+i).val("");
		$("#skill"+i).val("");
		//↑↑2013/3/7追記
		tmp=$(document.createElement("select")).attr({"name":namelist[i],"id":"schar"+i}).data({"i":i});
		$("#char"+i).html("").append(tmp);
		tmp.change(function(){
			for(var x=0;x<9;x++){
				if(document.getElementById("schar"+x).selectedIndex==this.selectedIndex&&this.selectedIndex!=0&&this.id!="schar"+x){
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
		for(var cnt=0;cnt<charRoleList.length;cnt++){
			var option =$(document.createElement("option"));
				option.text(charRoleList[cnt]);
				option.val(charRoleList[cnt]);
			tmp.append(option);
		}
	}
}
