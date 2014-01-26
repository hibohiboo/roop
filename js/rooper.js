//共通定数
//var $PHASEIMG="../rooper/img/loopready.png";
var $SAVECGI = "./save.cgi";
var $SYSTEMCGI='./system.cgi';
var $dataText="dat/save.dat";
var updateTime=60;//自動更新時間

//手札
var $HERONUM=3;
var $PLAYNUM=$HERONUM+3;
var $CARDWIDTH=35;
var $CARDHEIGHT=50;
var $CARDMARGIN=5;
var $RIGHTWIDTH=160;

//キャッシュ
var disp;//etDisplayCache()で定義

//最初に実行
jQuery.event.add(window, "load",function(event){
	makehand();
	makeselecthand();

	setphaseHTML();

	loadFile();

	autoupdate(updateTime);

});
//自動更新
var myinterval;
function autoupdate(time){
	var uptime=parseInt(time);
	clearInterval(myinterval);
	if(uptime==0)return;
	myinterval = setInterval("loadData('data')",uptime*1000);
}
//更新時間変更
function changeuptime(time){
	updateTime=parseInt(time.value);
	autoupdate(updateTime);
}
var $sheetopen=0;//シート公開設定
//ボード
var boards =new Array();
var $boardx=new Array("10","220");
var $boardy=new Array("30","170");
//rule
var ruleHEAD  = new Array("ルール名","役職追加","ルール追加");
var ruleY = new Array();
var ruleX = new Array();
//role
var roleHEAD = new Array("名前","人数上限","条文能力","追加能力","逆引きルール")
var roleList=new Array();

/*======================================================*/

function makeRule(dat){
	var tmparr=dat.split(",");//,で分割
	switch(tmparr[0]){
	case "boards":
		for(var i=0;i<4;i++){
		var tmpobj = new function(){
			this.name = tmparr[i+1];
			this.pos = new Array(charlist.length);
			for(var j=0;j<charlist.length;j++){
				this.pos[j]=new Array("x","y");
			}
			if(i==0){
				var x=0;var y=0;
				this.x=160;
				this.y=85;
			}
			if(i==1){
				var x=0;var y=1;
				this.x=160;
				this.y=230;
			}
			if(i==2){
				var x=1;var y=0;
				this.x=360;
				this.y=85;
			}
			if(i==3){
				var x=1;var y=1;
				this.x=360;
				this.y=230;
			}
			this.pos[0].x=$boardx[x];
			this.pos[0].y=$boardy[y];
			positionSet(this.pos);
			//
			this.anyaku=0;
		}
		boards.push(tmpobj);
		}
		break;
	case "role":
		var tmpobj = new function(){
			this.name = tmparr[1];
			this.max = tmparr[2];
			this.yukomusi=tmparr[3];
			if(tmparr[3].indexOf("+") != -1){
				//2013.10.26.add↓↓
				var tmp=tmparr[3].split("+");
				if(tmp[0]=="死後活性")tmp[0]="<li><font color='yellow'>"+tmp[0]+"</font></li>";
				if(tmp[0]=="表裏選択")tmp[0]="<li><font color=''>"+tmp[0]+"</font></li>";
				if(tmp[0]=="友好無視")tmp[0]="<li><font color='#b0e0#00ff7fe8'>"+tmp[0]+"</font></li>";
				if(tmp[1]=="友好暴発")tmp[1]="<li><font color='#ff4500'>"+tmp[1]+"</font></li>";
				if(tmp[1]=="絶対友好無視")tmp[1]="<li><strong><font color='#b0e0e8'>"+tmp[1]+"</font></strong></li>";
				this.yukomusi="<ul>"+tmp[0]+tmp[1]+"</ul>";
				//2013.10.26.add↑↑
				//this.yukomusi=this.yukomusi.replace(/\+/g,"</li><li>");
				//this.yukomusi="<ul><li>"+this.yukomusi+"</li></ul>";
			}
			this.noryoku=tmparr[4];
			if(tmparr[5]){
				var tmp = tmparr[5].split("+");
				this.rule=tmp;
			}else{this.rule=new Array("");}
		}
		roleList.push(tmpobj);
		break;
	default:
		var tmpobj=new function(){
			this.name=tmparr[1];
			if(tmparr[2]){
				var tmp = tmparr[2].split("+");
				this.role=tmp;
			}else{this.role=new Array("");}
			this.rule=tmparr[3];
		}
		if(tmparr[0]=="Y")ruleY.push(tmpobj);
		if(tmparr[0]=="X")ruleX.push(tmpobj);
	}

}

//部品追加関連
function addclick(id,func){
	id.onclick=addScript;
	function addScript(){
		eval(func);
	}
}