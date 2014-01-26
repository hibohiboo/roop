#!/usr/bin/perl --
require "../rooper/jcode.pl";
require '../rooper/cgi-lib.pl';

#perl5.8で動作。
#perl5.16で動作しない。

#============================ ユーザー設定 ====
$CHARSET       = 'Shift_JIS';		# 文字コード
$ENTRYFILE     = './dat/entry.dat';		# 参加者ファイル
$CHATFILE      = './dat/chat.dat';		# 発言ログファイル
$LOGFILE      = './dat/log.dat';		# 発言ログファイル
$BOARDFILE    = './dat/board.dat';
$SAVEFILE = './dat/save.dat';
$CHARFILE = './dat/char.dat';
$KAICHARFILE = './dat/kaichar.dat';#2013.5.18.add
$SCENARIOFILE = './dat/scenario/scenario.dat';   # 脚本保存ファイル
$OPENSHEET = './scenario/open.htm';   # 公開シート保存ファイル
$CLOSESHEET = './scenario/close.htm'; #非公開シート保存ファイル
$REFRESH       = 30;			# リロード時間（秒）
$REPLYTIME     = 60;			# 最大応答時間（秒）
$MAXLINE       = 30;			# 最大ログ行数
$COOKIE_PREFIX = 'simplechat';		# クッキープリフィクス
$COOKIE_LIFE   = 10;			# クッキー期限（日）

$JSPATH=".";
$CSSPATH=".";

$CHARIMGPATH="../rooper/first/img/character";
#======================== メインプログラム ====
loadFormdata();
loadCookie();

if($FORM{'frame'} eq 'input') {
	# 入力フレーム
	printInputFrame();
}
elsif($FORM{'frame'} eq 'view') {
	# 表示フレーム
	loadChatfile();
	if($FORM{'mode'} eq 'write') {
		writeRemark($FORM{'name'}, $FORM{'email'}, $FORM{'text'},$FORM{'hero'});
	}
	printViewFrame();
}
elsif($FORM{'frame'} eq 'hero') {
	# HEROフレーム
	HeroFrame();
}
elsif($FORM{'frame'} eq 'writer') {
	# 脚本家フレーム
	WriterFrame($FORM{'custom'});
}
else {
	# フレームセット
	#脚本家画面------------------------------------------------------------------
	if($FORM{'mode'} eq 'enter2') {
		
		if($FORM{'name'} eq '') {
			printErrorPage("名前は必ず記入してください。");
		}
		$COOKIE{'name'}  = $FORM{'name'};
		printFramePage2();
		writeScenario();
	}
	#脚本入力パス画面------------------------------------------------------------------
	if($FORM{'mode'} eq 'enter3') {
		
		if($FORM{'name'} eq '') {
			printErrorPage("名前は必ず記入してください。");
		}
		$COOKIE{'name'}  = $FORM{'name'};
		printFramePage2();
	}
#------------------------------------------------------------------
	elsif($FORM{'mode'} eq 'hero') {
		if($FORM{'name'} eq '') {
			printErrorPage("名前は必ず記入してください。");
		}
		$COOKIE{'name'}  = $FORM{'name'};
		printFramePageHERO();
	}
#シナリオ頁------------------------------------------------------------------
	elsif($FORM{'mode'} eq 'scenario') {
		if($FORM{'name'} eq '') {
			printErrorPage("名前は必ず記入してください。");
		}
		$COOKIE{'name'}  = $FORM{'name'};
		if($FORM{'custom'} eq "1"){
			printCustomScenarioPage();
		}#elsif($FORM{'custom'} eq "6" || $FORM{'custom'} eq "7"){
		elsif($FORM{'custom'} >= 6){
			printFirstScenarioPage();
		}else{
			printScenarioPage();
		}
	}
#------------------------------------------------------------------
	elsif($FORM{'mode'} eq 'resetsave') {
		resetSave();
		if($FORM{'custom'} eq "1"){
			printCustomScenarioPage();
		}elsif($FORM{'custom'} eq "6"|| $FORM{'custom'} eq "7"){
			printFirstScenarioPage();
		}else{
			printScenarioPage();
		}
	}
#------------------------------脚本読み込み------------------------------------
	elsif($FORM{'mode'} eq 'loadscenario') {
		#resetSave();
		loadScenario();
	}
#--------------------------------------------------------------------
	elsif($FORM{'mode'} eq 'enter') {
		if($FORM{'name'} eq '') {
			printErrorPage("名前は必ず記入してください。");
		}
		loadChatfile();
		writeRemark("[INFO]", "",
			"『$FORM{'name'}』さんが参加されます。",$FORM{'hero'});
		updateEntrants();
		$COOKIE{'name'}  = $FORM{'name'};
		printFramePage();
	}
#====================================================================
	elsif($FORM{'mode'} eq 'exit') {
		loadChatfile();
		writeRemark("[INFO]", "",
			"『$FORM{'name'}』さんは退出されました。",$FORM{'hero'});
		updateEntrants(1);
		print "Location: $ENV{'SCRIPT_NAME'}\n\n";
	}
	else {
		printEntryPage();
	}
}
exit;


#==================== エントリーページ出力 ====
sub printEntryPage
{
	loadBoardfile();
	if($FORM{'board'} eq 'write') {writeBoard($FORM{'text'});}

# 二重投稿を抑制する
if ($FORM{'text'} ne "") {
    print "Location: http://$ENV{'HTTP_HOST'}$ENV{'SCRIPT_NAME'}\n\n";
    exit(0);
}
	
	my $entry = time;
	my @users = updateEntrants();
	my $entrants;
	
	if(@users > 0) {
		$entrants = "<ul class='float'><li>・"
			. join('</li><li>・', @users) . "</li></ul>";
	}
	
	printHttpHeader();

$tag_select = <<END_OF_DATA;
<select name="custom">
<option value="0">Basic Tragedy</option>
<option value="1">Original Tragedy</option>
<option value="2">α版ルール</option>
<option value="3">Visual Novel（仮）</option>
<option value="4">Haunted Stage</option>
<option value="5">Mystery Circle</option>
<option value="6">First Steps</option>
<option value="7" selected>Basic Tragedy χ</option>
<option value="8">Mystery Circle χ</option>
<option value="9">Haunted Stage χ</option>
<option value="10">Another Horizon</option>
</select>
END_OF_DATA

	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><title>惨劇RoopeRオンラインTool</title>
<meta name="description" content="BakaFire様製作の同人ボードゲーム惨劇RoopeRをブラウザ上で遊ぶCGIツールです。誰でも気軽に使用できます。このサイトは惨劇コモンズを使用しています。">
<meta name="keywords" content="惨劇RoopeR,惨劇ルーパー,オンラインセッション,ツール,支援">
<meta http-equiv="Content-Style-Type" content="text/css">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/jquery.js"></script>
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<script language="JavaScript">
function skipmakescenario(){
	if(\$("#scenarioskip").attr('checked')){
		\$("#mode").val("enter3");
	}else{
		\$("#mode").val("scenario");
	}
}
</script>
</head>
<body>
<div id="wrap"  style="position:absolute;">
<h1 class="namewriter">オンライン惨劇ツール</h1>
<div id="inroom" style="position:relative; padding:5px;	margin:10px;">
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="namewriter"> 脚本家</span>：<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="参加する">
<!--#2013.11.07.up-->
$tag_select

<input type="checkbox" id="scenarioskip" onclick="skipmakescenario()">脚本入力画面を飛ばす。
<br>

<input type="hidden" id="mode" name="mode" value="scenario">
<input type="hidden" name="entry" value="$entry">
<input type="hidden" name="hero" value="writer">
</form>
<hr>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="name0">主人公1</span>：<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="参加する">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="0">
<input type="hidden" name="entry" value="$entry">
</form>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="name1">主人公2</span>：<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="参加する">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="1">
<input type="hidden" name="entry" value="$entry">
</form>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="name2">主人公3</span>：<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="参加する">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="2">
<input type="hidden" name="entry" value="$entry">
</form>
<hr>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="name4">主人公1対1用</span>：<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="参加する">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="4">
<input type="hidden" name="entry" value="$entry">
</form>
<hr>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
見学用：<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="参加する">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="3">
<input type="hidden" name="entry" value="$entry">
</form>

</div>
<hr>
<div id="entrants">
<strong>現在の参加者</strong>（自動更新されません)
$entrants
</div>
<hr style="clear:both;position:relative;top:2em;">
<ul style="position:relative;top:2em;margin:2px;">
<li>惨劇RoopeR（BakaFire Party様製作)をオンラインで遊ぶツールです。</li>
<li>使い方解説動画できました。AH対応版です。→<a href='http://www.nicovideo.jp/watch/sm22350352'>ニコニコ動画</a>。</li>
<li><a href="../rooper6/rooper.cgi">ANOTHR HORIZON・学者・幻想対応テストルーム</a></li>
<li><font color="red">new:</font>サンプルシナリオ機\能\を\追\加。あなたの脚本も追加させてください！→<a href="http://rooper.1616bbs.com/bbs/" target='_blank'>脚本置き場</a></li>
<li>各種惨劇セット追加！ テスト中です。バグがあった場合、一行掲示板のほうに報告よろしくお願いします。</li>
<li><strong>
<a href="http://asuwa.island.ac/rooper/readme/readme.htm">画面の見方</a>。　　<a href="http://asuwa.island.ac/rooper/readme/guide.htm">ゲームの進め方</a>。　　<a href="http://asuwa.island.ac/rooper/readme/readme_faq.htm">FAQ</a>。　　<a href="http://asuwa.island.ac/rooper/readme/readme_new_2.htm">脚本データ。</a>
</strong></li>
<li><a href="http://asuwa.island.ac/rooper/readme/readme_add.htm#iincho">委員長による手札回収実装</a>。</li>

<li>こちらが使用中の時にどうぞ。<a href="../rooper7/rooper.cgi">AH対応\予\備部屋1</a>。<a href="../rooper8/rooper.cgi">AH対応\予\備部屋2</a></li>
<li><a href="http://asuwa.mistysky.net/rooper/original.html">オリジナル拡張セット：Visual Novel</a>を追加。テスト中です。友好カウンターを中心に据えたセット。ご意見募集中。</li>
<li><a href="http://asuwa.island.ac/rooper/oldfasion.csv">Original Tragedyデータファイル：Old Fasion</a>。OldFasionはyukikaze様製作の非公式惨劇セットです。→<a href="http://yukikaze.otaden.jp/e242281.html">link：北へ。の国から</a></li>
<li>現在β版です。\予\告なく内容の変更・削除を行う場合があります。</li>
<li>うまく動作しないときは一旦退出し、キャッシュの削除を行ってみてください。その後、再度入室してください。</li>
<li><a href="http://bakafire.main.jp/rooper/sr_top.htm">惨劇RoopeR本家サイト</a></li>
<li>**<a href="http://dengekionline.com/elem/000/000/688/688677/">電撃オンラインで特集！</a> 必見！ 製作者との対戦リプレイ。**  **<a href="http://www.4gamer.net/games/199/G019961/20130111001/">4Gamer.netで惨劇RoopeRの紹介！</a> 短いリプレイ付きの分かりやすい解説。**</li>
<li><a href="https://docs.google.com/leaf?id=0BzGm1Adi28XLQ3gyZm1qdlJTdFdHMXEzeURZNFVudw">ひだりさんの公開・非公開シートDL</a>。<a href="http://chaos.sakuraweb.com/sc/bg/boardgame_sum.html">佐々宮智志さんのサマリー</a></li>
<li><a href="http://www.dodontof.com/">どどんとふ</a>で<a href="http://www.dodontof.com/index.php?option=com_content&view=article&id=246&Itemid=126#scenarioData">惨劇RoopeR用シナリオデータ</a>公開！ →<font color="red">new:</font><a href="http://opengameseeker.com/archives/5952">惨劇紹介＆どどんとふ導入法</a></li>
<li>ルールX、ルールY、役職、事件は主人公の書9～13頁よりの転載となります。　　非公開シート・公開シートは主人公の書２２・２３を参考としています。  手札リストは主人公の書１８・１９頁を参照です。Mystery Circleは３～９頁,HauntedStageは４～９頁からの転載となります。FirstStepsは惨劇RoopeRχ主人公の書３１～３３頁、BasicTragedyχは３４～３８頁からの転載となります。</li>
<li>惨劇コモンズ、惨劇コモンズχ作成:BakaFire様、紺ノ玲様。カードイラスト：ぐり。<a href="http://kage-design.com/wp/">シルエットデザイン</a>。</li>
<li>動作確認はfirefox26.0で行なっています。\C\hr\ome\で\もうごくようです。</li>
<li><font color="red">Internet Explorerでは動作しないことがあります</font>。動かないときは、お手数ですが<a href='http://www.google.co.jp/chrome/intl/ja/landing.html'>chrome</a>や<a href='http://mozilla.jp/firefox/'>firefox</a>をDLしてください。</li>
<li><a href="./dat/log.dat">ログファイル。</a>不定期に初期化します。</li>
<li><a href="http://asuwa.island.ac/calendar/calendar.php">惨劇用カレンダー</a>作成しました。よろしければご利用ください。</a></li>
</ul>

<hr style="position:relative;top:2em;">
<form action="$ENV{'SCRIPT_NAME'}" method="POST" name="lineboard" style="position:relative;top:2em;">
　一行掲示板
<input type="text" name="text" size="60">
<input type="submit" value="書きこむ"><br>
　部屋の予\約などにお使いください。バグ報告や要望もこちらに。
	<input type="hidden" name="board" value="write">
</form>
<hr style="position:relative;top:2em;">
<div style="position:relative;top:2em;">
END
	foreach $ln (@BOARD) {
		chomp $ln;
		my ($date,$text) = split(/\t/, $ln);
		
		print "<p>";
		print "＞$text($date)";
		print "</p>\n<hr>\n";
	}
print <<END;
</div>
<div class="footer">
当スクリプトを使用するに当たって不具合が生じても責を負いかねます。<br>
Copyright &copy; 2012-hibo
<br><a href="../index.htm">SITE-TOP</a>
	</div>
</div>
</body>
</html>
END
}
#====================== フレームセット出力new ====
sub printFramePage2
{
	my $encname = urlencode($FORM{'name'});
	
	printHttpHeader();
	
	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<title>room</title></head>
<frameset cols="25%, 75%">
<frame name="hidari"
	src="$ENV{'SCRIPT_NAME'}?mode=enter&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">
<frame name="migi"
	src="$ENV{'SCRIPT_NAME'}?frame=writer&name=$encname&entry=$FORM{'entry'}&custom=$FORM{'custom'}&hero=$FORM{'hero'}">
<noframes>
<p>フレームをサポートしたWebブラウザをお使いください。</p>
</noframes>
</frameset>
</html>
END
}

#====================== フレームセット出力しゅじんこう ====
sub printFramePageHERO
{
	my $encname = urlencode($FORM{'name'});
	
	printHttpHeader();
	
	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<title>room</title></head>
<frameset cols="25%, 75%">
<frame name="hidari"
	src="$ENV{'SCRIPT_NAME'}?mode=enter&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">
<frame name="migi"
	src="$ENV{'SCRIPT_NAME'}?frame=hero&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">
<noframes>
<p>フレームをサポートしたWebブラウザをお使いください。</p>
</noframes>
</frameset>
</html>
END
}


#====================== フレームセット出力 ====
sub printFramePage
{
	my $encname = urlencode($FORM{'name'});
	
	printHttpHeader();
	
	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<title>inroom</title></head>
<frameset rows="25%, 75%">
<frame name="head"
	src="$ENV{'SCRIPT_NAME'}?frame=input&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">
<frame name="body"
	src="$ENV{'SCRIPT_NAME'}?frame=view&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">
<noframes>
<p>フレームをサポートしたWebブラウザをお使いください。</p>
</noframes>
</frameset>
</html>
END
}


#======================== 入力フレーム出力 ====
sub printInputFrame
{
	printHttpHeader();
	
	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">

<title>ちゃっと</title></head>
<body>
<form action="$ENV{'SCRIPT_NAME'}" target="body" method="POST"
	name="box"
	onSubmit='setTimeout("{ document.box.clear.click(); document.box.text.focus(); }", 300);'>
<strong class="name$FORM{'hero'}">$FORM{'name'}</strong><br>
<input type="text" name="text" size="60">
<input type="submit" value="発言する">
<button onClick="window.open('dat/log.dat')">ログ</button>
<input type="reset" value="クリア" name="clear">

<input type="hidden" name="frame" value="view">
<input type="hidden" name="mode" value="write">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="entry" value="$FORM{'entry'}">
<input type="hidden" name="hero" value="$FORM{'hero'}">
<input type="hidden" name="custom" value="$FORM{'custom'}">
</form>
<br>
<form action="$ENV{'SCRIPT_NAME'}" target="_top" method="POST">
<input type="submit" value="退出する">
<input type="hidden" name="mode" value="exit">
<input type="hidden" name="name" value="$FORM{'name'}">
<!--<input type="hidden" name="email" value="$FORM{'email'}">-->
<input type="hidden" name="entry" value="$FORM{'entry'}">
</form>
</body></html>
END
}


#======================== 表示フレーム出力 ====
sub printViewFrame
{
	my @users = updateEntrants();
	my $entrants = join(' | ', @users);
	my $encname = urlencode($FORM{'name'});
	my $ln;
	
	printHttpHeader();
	
	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">

<title>ちゃっと</title>

<meta http-equiv="Refresh"
	content="$REFRESH; URL=$ENV{'SCRIPT_NAME'}?frame=view&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">
</head>
<body>
<div>
<a href="$ENV{'SCRIPT_NAME'}?frame=view&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">[更新]</a>
参加者：$entrants
</div>
<hr>
END
	
	foreach $ln (@DATA) {
		chomp $ln;
		my ($date, $name, $email, $text,$hero) = split(/\t/, $ln);
		
		print "<p>";
		print qq|<strong class="name$hero">|;
		if($email) {
			print "<a href=\"mailto:$email\">$name</a>";
		}
		else {
			print $name;
		}
		print "</strong>";
		print " : $text($date)";
		print "</p>\n";
	}
	print "</body></html>";
}


#======================== エラーページ出力 ====
sub printErrorPage
{
	print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<title>ちゃっと</title></head>
<body><h1>エラー</h1><p>$_[0]</p></body>
</html>
END
	
	exit;
}


#======================== HTTPヘッダー出力 ====
sub printHttpHeader
{
	# グリニッジ標準時の文字列
	my @mon_str = (
		'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
		'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
	my @wdy_str = (
		'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat');
	my ($sec, $min, $hour, $mday, $mon, $year, $wday)
		= gmtime(time + ($COOKIE_LIFE * 24 * 60 * 60));
	my $date = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
		$wdy_str[$wday], $mday, $mon_str[$mon], $year + 1900,
		$hour, $min, $sec);
	
	# ヘッダーの出力
	my ($name, $value);
	
	print "Content-type: text/html; charset=$CHARSET\n";
	foreach $name (keys %COOKIE) {
		$value = $COOKIE{$name};
		$name = "${COOKIE_PREFIX}_$name";
		$value =~ s/(\W)/sprintf("%%%02X", ord($1))/eg;
		
		print "Set-Cookie: $name=$value; expires=$date\n";
	}
	print "\n";
}


#========================== ログを読み込む ====
sub loadChatfile
{
	open(FILE, "<$CHATFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 1) };
	@DATA = <FILE>;
	close(FILE);
	open(FILE, "<$LOGFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 1) };
	@LOG = <FILE>;
	close(FILE);
}
#========================== 掲示板ログを読み込む ====
sub loadBoardfile
{
	open(FILE, "<$BOARDFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 1) };
	@BOARD = <FILE>;
	close(FILE);
}
#========================== 掲示板に発言を書き込む ====
sub writeBoard
{
	printErrorPage("内容の記入不足です。日本語を含めてください") if $FORM{'text'} !~ /[^a-zA-Z0-9\-\.\=\_\/\:\;\@\%\&\?\!\+\~\(\)\|\*\$\'\"\#\r\n\<\>\ ]/;
	printErrorPage("使用不可な文字列が含まれています.") if $FORM{'text'} =~ /(biagra)|(viagra)|(buy)|(mail)|(sex)|(nice)|(site)/;
	my ($text) = @_;
	my ($sec, $min, $hour, $mday, $mon, $year, $wday)
		= localtime(time);
	my $date = sprintf("%02d/%02d %02d:%02d",
		++$mon, $mday, $hour, $min);
if (!$text eq ''){ 
	unshift @BOARD, "$date\t$text\n";
	while(@BOARD > $MAXLINE) {
		pop @BOARD;
	}

	open(FILE, ">$BOARDFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	print FILE @BOARD;
	close(FILE);
}
}


#========================== 発言を書き込む ====
sub writeRemark
{
	my ($name, $email, $text,$hero) = @_;
	my ($sec, $min, $hour, $mday, $mon, $year, $wday)
		= localtime(time);
	my $date = sprintf("%02d/%02d %02d:%02d",
		++$mon, $mday, $hour, $min);
if (!$text eq ''){ 
	unshift @DATA, "$date\t$name\t$email\t$text\t$hero\n";
	unshift @LOG, "$date\t$name\t$email\t$text\n";
	while(@DATA > $MAXLINE) {
		pop @DATA;
	}
	
	open(FILE, ">$CHATFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	print FILE @DATA;
	close(FILE);
	open(FILE, ">$LOGFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	print FILE @LOG;
	close(FILE);
}
}


#====================== 参加者の更新・列挙 ====
sub updateEntrants
{
	my $delflag = shift @_;
	my (@lines, @users, $i);
	my $noentry = 1;
	my $now = time;
	
	open(FILE, "<$ENTRYFILE")
		or printErrorPage("参加者ファイルが開けません。");
	eval{ flock(FILE, 1) };
	@lines = <FILE>;
	close(FILE);
	
	for($i = 0 ; $i < @lines ; ) {
		my ($name, $entry, $update,$hero,$custom) = split(/:/, $lines[$i]);
		#2013.11.07.add↓↓
		my $tragedyset="";
		if($custom ==1){
			$tragedyset="Original Tragedy";
		}elsif($custom ==2){
			$tragedyset="α版ルール";
		}elsif($custom == 3){
			$tragedyset="VisualNovel";
		}elsif($custom == 4){
			$tragedyset="HauntedStage";
		}elsif($custom == 5){
			$tragedyset="MysteryCircle";
		}elsif($custom == 6){
			$tragedyset="FirstSteps";
		}elsif($custom == 7){
			$tragedyset="Basic Tragedy χ";
		}elsif($custom == 8){
			$tragedyset="Mystery Circle χ";
		}elsif($custom == 9){
			$tragedyset="Haunted Stage χ";
		}elsif($custom == 10){
			$tragedyset="Another Horizon";
		}
		else{
			$tragedyset="Basic Tragedy";
		}
	#2013.11.07.add↑↑

		if($name eq $FORM{'name'} and $entry == $FORM{'entry'}) {
			$noentry = 0;
			if(not $delflag) {
				# 自分の最終更新時間を更新
				$lines[$i] = "$name:$entry:$now:$FORM{'hero'}:$custom\n";
			}
			else {
				# 自分を参加者から削除
				splice @lines, $i, 1;
				next;
			}
		}
		elsif($now - $update > $REPLYTIME) {
			# 最終更新時間から最大反応時間以上経過したユーザを削除
			splice @lines, $i, 1;
			next;
		}
		++$i;
#		push @users, $name;
=pod 2013.11.07.cut		
		#2012.5.5追記→→
		$tmp="";
#		if($hero eq "writer"){ 2.17除外

			if($custom ==1){
				$tmp="(Original Tragedy)";
			}elsif($custom ==2){
				$tmp="(α版ルール)";
			}elsif($custom == 3){
				$tmp="(VisualNovel)";
			}elsif($custom == 4){
				$tmp="(HauntedStage)";
			}elsif($custom == 5){
				$tmp="(MysteryCircle)";
			}elsif($custom == 6){
				$tmp="(FirstSteps)";
			}elsif($custom == 7){
				$tmp="(Basic Tragedy χ)";
			}elsif($custom == 8){
				$tmp="(Mystery Circle χ)";
			}elsif($custom == 9){
				$tmp="(Haunted Stage χ)";
			}elsif($custom == 10){
				$tmp="(Another Horizon)";
			}
			else{
				$tmp="(Basic Tragedy)";
			}
=cut
#		}2.17除外
		#←←
#		push @users, qq|<span class="name$hero">$name</span>$tmp|;2013.11.07.cut
	push @users, qq|<span class="name$hero">$name</span>($tragedyset)|;#2013.11.07.add
	}
	if($noentry and $FORM{'entry'}) {
		push @lines, "$FORM{'name'}:$FORM{'entry'}:$now:$FORM{'hero'}:$FORM{'custom'}\n";
#		push @users, $FORM{'name'};
		#2012.5.5追記→→
=pod 2013.11.07.cut	
		$tmp="";
#		if($FORM{'hero'} eq "writer"){ 2/17除外
			if($FORM{'custom'} ==1){
				$tmp="(Original Tragedy)";
			}elsif($FORM{'custom'} ==2){
				$tmp="(α版ルール)";
			}elsif($custom == 3){
				$tmp="(VisualNovel)";
			}elsif($custom == 4){
				$tmp="(HauntedStage)";
			}elsif($custom == 5){
				$tmp="(MysteryCircle)";
			}elsif($custom == 6){
				$tmp="(FirstSteps)";
			}elsif($custom == 7){
				$tmp="(Basic Tragedy χ)";
			}elsif($custom == 8){
				$tmp="(Mystery Circle χ)";
			}elsif($custom == 9){
				$tmp="(Haunted Stage χ)";
			}elsif($custom == 10){
				$tmp="(Another Horizon)";
			}
			else{
				$tmp="(Basic Tragedy)";
			}
#		}2.17除外
		#←←
=cut
#		push @users, qq|<span class="name$FORM{'hero'}">$FORM{'name'}</span>$tmp|; #2013.11.07.cut
		push @users, qq|<span class="name$FORM{'hero'}">$FORM{'name'}</span>($tragedyset)|;#2013.11.07.add
	}
	
	open(FILE, ">$ENTRYFILE")
		or printErrorPage("参加者ファイルが開けません");
	eval{ flock(FILE, 2) };
	print FILE @lines;
	close(FILE);
	
	return @users;
}


#=========================== URLエンコード ====
sub urlencode
{
	my $value = shift @_;
	
	$value =~ tr/ /+/;
	$value =~ s/(\W)/sprintf("%%%02X", ord($1))/eg;
	return $value;
}


#================== クッキーデータ取り込み ====
sub loadCookie
{
	my $pair;
	
	foreach $pair (split(/;\s*/, $ENV{'HTTP_COOKIE'})) {
		my ($name, $value) = split(/=/, $pair);
		
		if(not $name =~ /${COOKIE_PREFIX}_(.+)/) {
			next;
		}
		
		$name = $1;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
		$COOKIE{$name} = $value;
	}
}


#================== フォームデータ取り込み ====
sub loadFormdata
{
	my ($query, $pair);
	
	if($ENV{'REQUEST_METHOD'} eq 'POST') {
		read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
	}
	else {
		$query = $ENV{'QUERY_STRING'};
	}
	
	foreach $pair (split(/&/, $query)) {
		my ($key, $value) = split(/=/, $pair);
		
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
		
		$value = jcode::sjis($value);
		$value =~ s/&/&amp;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ tr/\t/ /;
		
		$FORM{$key} = $value;
	}
}
#================== 脚本家頁作成 ====
sub WriterFrame
{
print "Content-type: text/html; charset=$CHARSET\n";
print "Pragma: no-cache\n";
print "Cache-Control: no-cache\n";
print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n";
print "\n";

print <<END;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
      <script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/jquery.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/rooper.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/htmlparts.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/connect.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/update.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/control.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/board.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/character.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/hand.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/phase_common.js"></script><!--#2013.11.08.add-->
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/phase.js"></script>
END
#2013.11.07.add
	if($FORM{'custom'} eq "1"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/config.js"></script>|;
	}elsif($FORM{'custom'} eq "2"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/alphaconfig.js"></script>|;
	}elsif($FORM{'custom'} >= 3){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/config$FORM{'custom'}.js"></script>|;
	}else{
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/defconfig.js"></script>|;
	}
=pod 2013.11.07
	if($_[0] eq "1"){ 
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config.js"></script>|;
	}elsif($FORM{'custom'} eq "2"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/alphaconfig.js"></script>|;
	}elsif($FORM{'custom'} eq "3"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config3.js"></script>|;
	}elsif($FORM{'custom'} eq "4"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config4.js"></script>|;
	}elsif($FORM{'custom'} eq "5"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config5.js"></script>|;
	}elsif($FORM{'custom'} eq "6"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config6.js"></script>|;
	}elsif($FORM{'custom'} eq "7"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config7.js"></script>|;
	}elsif($FORM{'custom'} eq "8"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config8.js"></script>|;
	}elsif($FORM{'custom'} eq "9"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config9.js"></script>|;
	}elsif($FORM{'custom'} eq "10"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config10.js"></script>|;
	}else{
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/defconfig.js"></script>|;
	}
=cut
print <<END;
<script language="JavaScript">
</script>
<title>惨劇RoopeR$_[0]</title>
</head>
<body>
<div id="waku">
<div id="head"><form id="headform">
	<table id="buttonTable">
	<tr id="tr1">
	<td><button type="button" name="ruledisplay" onclick=changeboard('#gameboard')>ボード表\示</button></td>
	<td><button type="button" name="ruledisplay" onclick=changeboard('#RuleList')>ルール表\示</button></td>
	<td><button type="button" name="roledisplay" onclick="changeboard('#RoleList')">役職表\示</button></td>
	<td><button type="button" name="roledisplay" onclick="changeboard('#CharList')">キャラクター</button></td>
	<td rowspan="2"><button type="button" onclick="loadData('data')" value="move" id="updatebutton">更新</button></td>
	</tr><tr>
	<td><button type="button" name="roledisplay" onclick="viewCloseSheet();" id="closesheet">非公開シート</button></td>
	<td><button type="button" name="roledisplay" onclick="viewOpenSheet();" id="opensheet">公開シート</button></td>
	<td><button type="button" name="roledisplay" onclick="OpenSheet();" style="display:none;" id="openclosesheet">非公開シートを公開</button></td>
	<td></td>
	</tr>
	<tr>
	<td><button type="button" name="save" onclick="saveCookie();" id="savecookie">セーブ</button></td>
	<td><button type="button" name="load" onclick="loadCookie();" id="loadcookie">ロード</button></td>
	<td></td>
	<td><button id="resetgame" type="button" onclick="resetphase()" value="move" style="display:none;">ゲームリセット</button></td>
	
	<td>自動更新：<select id="uptime" onchange="changeuptime(this);">
				<option value="15">15秒</option>
				<option value="30">30秒</option>
				<option value="60" selected>１分</option>
				<option value="300">５分</option>
				<option value="0">しない</option>
	</select></td>
	</tr>
	<tr>
	<td colspan="2"><button id="nextphasebutton" type="button" onclick="nextPhase()" value="move">次のフェイズ</button></td>
	</td>
	<td id="tableLeaderSkip"></td>
	<td id="tableLoopEnd"></td>
	</tr>
	</table>
</form></div>
<div id="gameboard">
	<div id="writer"></div>
	<div id="left">
		<button type="button" onclick="jQuery('#writer').toggle();" value="" id="writerbutton">表\示<br>/非表\示</button>
	</div>
	<div id="center"><div id="board"></div></div><div id="right"></div>
	<div id="bottom"></div>
</div><!--gameboard-->
</div><!--waku-->
<div id="waku2"><div id="test"></div></div>
</body>
</html>


END
}
#================== 主人公頁作成 ====
sub HeroFrame
{

print "Content-type: text/html; charset=$CHARSET\n";
print "Pragma: no-cache\n";
print "Cache-Control: no-cache\n";
print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n";
print "\n";
	
print <<END;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<!--<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT"> -->
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooperhero.css">
      <script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/jquery.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/rooper.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/htmlparts.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/connect.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/update.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/control.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/board.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/character.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/hand.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/phase_common.js"></script><!--#2013.11.08.add-->
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/herophase.js"></script>
END
#2013.11.07.add
	if($FORM{'custom'} eq "1"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/config.js"></script>|;
	}elsif($FORM{'custom'} eq "2"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/alphaconfig.js"></script>|;
	}elsif($FORM{'custom'} >= "3"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/config$FORM{'custom'}.js"></script>|;
	}else{
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/defconfig.js"></script>|;
	}
=pod 2013.11.07
	if($FORM{'custom'} eq "1"){ 
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config.js"></script>|;
	}elsif($FORM{'custom'} eq "2"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/alphaconfig.js"></script>|;
	}elsif($FORM{'custom'} eq "3"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config3.js"></script>|;
	}elsif($FORM{'custom'} eq "4"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config4.js"></script>|;
	}elsif($FORM{'custom'} eq "5"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config5.js"></script>|;
	}elsif($FORM{'custom'} eq "6"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config6.js"></script>|;
	}elsif($FORM{'custom'} eq "7"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config7.js"></script>|;
	}elsif($FORM{'custom'} eq "8"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config8.js"></script>|;
	}elsif($FORM{'custom'} eq "9"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config9.js"></script>|;
	}elsif($FORM{'custom'} eq "10"){
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/config10.js"></script>|;
	}
	
	else{
		print qq|<script type="text/javascript" charset="UTF-8" language="JavaScript" src="js/defconfig.js"></script>|;
	}
=cut
print <<END;
<script language="JavaScript">
</script>
<title>惨劇RoopeRHero0</title>
</head>
<body>
<div id="waku">
<div id="head"><form id="headform">
	<table id="buttonTable">
	<tr id="tr1">
	<td><button type="button" name="ruledisplay" onclick=changeboard('#gameboard')>ボード表\示</button></td>
	<td><button type="button" name="ruledisplay" onclick=changeboard('#RuleList')>ルール表\示</button></td>
	<td><button type="button" name="roledisplay" onclick="changeboard('#RoleList')">役職表\示</button></td>
	<td><button type="button" name="roledisplay" onclick="changeboard('#CharList')">キャラクター</button></td>
	<td rowspan="2"><button type="button" onclick="loadData('data')" value="move" id="updatebutton">更新</button></td>
	</tr><tr>
	<td><button type="button" name="roledisplay" onclick="viewCloseSheet();" id="closesheet">非公開シート</button></td>
	<td><button type="button" name="roledisplay" onclick="viewOpenSheet();" id="opensheet">公開シート</button></td>
	<td></td>
	<td></td>
	</tr><tr>
	<td colspan="2"><button id="nextphasebutton" type="button" onclick="nextPhase()" value="move">次のフェイズ</button></td>
	<td></td><td></td>
	<td>自動更新：<select id="uptime" onchange="changeuptime(this);">
				<option value="15">15秒</option>
				<option value="30">30秒</option>
				<option value="60" selected>１分</option>
				<option value="300">５分</option>
				<option value="0">しない</option>
	</select></td>
	</tr>
</table>
</form></div>
<div id="gameboard">
	<div id="writer"></div><!--toggle('writer')-->
	<div id="left"><button type="button" onclick="jQuery('#writer').toggle();" value="" id="writerbutton">表示<br>/非表示</button></div><div id="center"><div id="board"></div></div><div id="right"></div>
	<div id="bottom"></div>
</div><!--gameboard-->
</div><!--waku-->
<div id="waku2"><div id="test"></div>
<input type="hidden" id="hero" value="$FORM{'hero'}">
</div>
</body>
</html>
END
}

#================== 脚本作成頁作成 ====
sub printScenarioPage{

=pod
print "Content-type: text/html; charset=$CHARSET\n";
print "Set-Cookie: $name=$value; expires=$date\n";
print "Pragma: no-cache\n";
print "Cache-Control: no-cache\n";
print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n";
print "\n";
=cut
 printHttpHeader();
	print <<END;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<!--<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT"> -->
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/jquery.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/scenariomake.js"></script>

<script language="JavaScript">
</script>
<title>惨劇RoopeR</title>
</head>
<title>シート</title></head>
<body>
<h1>脚本</h1>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<input type="hidden" name="mode" value="resetsave">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="custom" value="$FORM{'custom'}">
<input type="submit" value="現在のゲームボードをリセット" style="font-size:200%">
<input type="hidden" name="entry" value="$FORM{'entry'}">
</form>
<hr>
END
if(	$FORM{'custom'}==0||	$FORM{'custom'}==3){
	print <<END;
<form method='post' action='./scenario.cgi' ENCTYPE='multipart/form-data'>
ファイル選択： <input type='file' name='upload_file'size='30'>
<input type='hidden' name='filetype' value='text'>
<input type="hidden" name="mode" value="loadscenario">
<input type='submit' value='アップロード'>
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="entry" value="$FORM{'entry'}">
<input type="hidden" name="hero" value="writer">
<input type="hidden" name="custom" value="$FORM{'custom'}">
</form>
<hr>
END
}
	print <<END;
<form action="$ENV{'SCRIPT_NAME'}" method="POST" id="mainform">
END
if(	$FORM{'custom'}==0||	$FORM{'custom'}==3|| $FORM{'custom'}==4 || $FORM{'custom'}==5){
	print qq|<button type="button" onclick="changeselectbox()">選択方式に変更する。</button>|;
}
	print <<END;
<table>
<tr><th>ルールY</th><td id="ruleY"><input type="text" name="ruleY" size="40"></td></tr>
<tr><th>ルールX1</th><td id="ruleX1"><input type="text" name="ruleX1" size="40"></td></tr>
<tr><th>ルールX2</th><td id="ruleX2"><input type="text" name="ruleX2" size="40"></td></tr>
<table>
<tr id="chartablehead"><th>人物</th><th>役職</th></tr>
<tr id="chartabletr0"><td>男子学生</td><td id="char0"><input type="text" name="shonen" size="30" value="パー\ソ\ン"></td></tr>
<tr id="chartabletr1"><td>女子学生</td><td id="char1" ><input type="text"name="shojo" size="30" value="パー\ソ\ン"></td></tr>
<tr id="chartabletr2"><td>お嬢様</td><td  id="char2"><input type="text"  name="ojo" size="30" value="パー\ソ\ン"></td></tr>
<tr id="chartabletr3"><td>巫女</td><td id="char3">     <input type="text" name="miko" size="30" value="パー\ソ\ン"></td></tr>
<tr id="chartabletr4"><td>刑事</td><td id="char4"><input type="text"     name="keiji" size="30" value="パー\ソ\ン"></td></tr>
<tr id="chartabletr5"><td>サラリーマン</td><td id="char5" ><input type="text" name="salary" size="30" value="パー\ソ\ン"></td></tr>
<tr id="chartabletr6"><td>情報屋</td><td id="char6"><input type="text"   name="joho" size="30" value="パー\ソ\ン"></td></tr>
<tr id="chartabletr7"><td>医者</td><td  id="char7"><input type="text"    name="isha" size="30" value="パー\ソ\ン"></td></tr>
<tr id="chartabletr8"><td>入院患者</td><td id="char8"><input type="text"   name="kanja" size="30" value="パー\ソ\ン"></td></tr>
</table>
<table>
<tr><th>日数</th><th>事件</th><th width="300px">事件効果</th><th>犯人</th></tr>
END
if($FORM{'custom'} eq "2"){
	$tmp=8;
}elsif($FORM{'custom'} eq "4" || $FORM{'custom'} eq "5"){
	$tmp=11;
}
else{
	$tmp=10;
}
for ($i=1;$i<=$tmp;$i++){
	$tmp1="day".$i;
	$tmp2="kouka".$i;
	$tmp3="han".$i;
	$sample1="";
	$sample2="";
	if($FORM{'custom'} < 4){
	if($i==1){
		$sample1="殺人事件";
		$sample2="可\能\ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。";
	}
	if($i==2){
		$sample1="不安拡大";
		$sample2="任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。";
	}
	if($i==3){
		$sample1="自殺";
		$sample2="犯人は死亡する。";
	}
	if($i==4){
		$sample1="病院の事件";
		if($FORM{'custom'} eq "2"){
			$sample2="病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。";
		}else{
			$sample2="病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。";

		}
	}
	if($i==5){
		$sample1="邪気の汚染";
		$sample2="神社に暗躍カウンターを２つ置く。";
	}
	}
	if($FORM{'custom'} eq "0"||$FORM{"custom"} == 3){
		if($i==6){
			$sample1="別離";
			$sample2="犯人を任意のボードに移動させる。";
		}
		if($i==7){
			$sample1="\暴\露";
			$sample2="どちらかを選ぶ。\n１．犯人と同じエリアにいるキャラクターから友好カウンターを２つまで取り除く（２人に割り振ってもよい）。\n２．犯人と同じエリアにいるキャラクターに友好カウンターを２つまで置く（２人に割り振ってもよい）。";
		}
	}else{}
	if($FORM{'custom'} eq "3"){
		if($i==3){
			$sample1="引越し";
			$sample2="以降、犯人を全てのボードにいないものとして扱い、カードをセットすることもできなくなる。";
		}
		if($i==4){
			$sample1="テロリズム";
			$sample2="都市に暗躍カウンターが１つ以上置かれている場合、都市にいるキャラクター全員が死亡する。さらに、都市に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。";
		}
		if($i==8){
			$sample1="ルート確定";
			$sample2="事件が起こり、かつ犯人の友好\能\力が使用できるとき、犯人の役職をキーパー\ソ\ンに変更する。";
		}
		if($i==9){
			$sample1="ときめく爆弾";
			$sample2="事件が起こり、かつ犯人に友好カウンターが１つも乗っていない場合、EXカウンターを用意する。初期値は０である。その日からターン終了フェイズごとにEXカウンターが１ずつ増加する。３になった時点で全てのキャラクターの友好カウンターが２減少する。犯人に友好カウンターを乗せるとEXカウンターの値は０になる。";
		}
	}
	if($FORM{'custom'} eq "4"){
		if($i==1){
			$sample1="連続殺人";
			$sample2="可\能\ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。\n他の連続殺人の犯人となっているキャラクターを事件の犯人とすることができる。";
		}
		if($i==2){
			$sample1="不安拡大";
			$sample2="任意のキャラクター１人に[不安カウンター]を２つ置き、任意の別のキャラクター１人に[暗躍カウンター]を１つ置く。";
		}
		if($i==3){
			$sample1="集団自殺";
			$sample2="犯人に[暗躍カウンター]が１つ以上→犯人と同じエリアにいるキャラクター全てを死亡させる。";
		}
		if($i==4){
			$sample1="代行者";
			$sample2="＜不安臨界-2＞Exゲージを１増加させ、リーダーであるプレイヤーはキャラクターを１人選ぶ。そのキャラクターを死亡させる。";
		}
		if($i==5){
			$sample1="病院の事件";
			$sample2="病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。";
		}
		if($i==6){
			$sample1="冒涜";
			$sample2="任意の死体１つに［不安カウンター］と［暗躍カウンター］を１つずつ置く。";
		}
		if($i==7){
			$sample1="魔獣の解放";
			$sample2="犯人のいるエリアに「魔獣」カードを置く。以降、そのカードは「魔獣」という名前の役職がナイトメアであるキャラクターとして扱う。";
		}
		if($i==8){
			$sample1="百鬼夜行";
			$sample2="＜死後発生＞神社に[暗躍カウンター]が１つ以上→Exゲージを４増加させる。";
		}
		if($i==9){
			$sample1="呪怨";
			$sample2="＜死後発生＞犯人と同じエリアにあるカード１つを任意の別のボードに移動させる。";
		}
		if($i==10){
			$sample1="蔓延";
			$sample2="＜死後発生＞犯人のいるボードに［暗躍カウンター］を２つ置く。";
		}
		if($i==11){
			$sample1="繰り返す悪夢";
			$sample2="＜死後発生＞Exゲージを1増加させ、犯人は蘇生する。";
		}
	}
	if($FORM{'custom'} eq "5"){
		if($i==1){
			$sample1="殺人事件";
			$sample2="可\能\ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。";
		}
		if($i==2){
			$sample1="不安拡大";
			$sample2="任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。";
		}
		if($i==3){
			$sample1="自殺";
			$sample2="犯人は死亡する。";
		}
		if($i==4){
			$sample1="病院の事件";
			$sample2="病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。";
		}
		if($i==5){
			$sample1="テロリズム";
			$sample2="都市に暗躍カウンターが１つ以上置かれている場合、都市にいるキャラクター全員が死亡する。さらに、都市に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。";
		}
		if($i==6){
			$sample1="前兆";
			$sample2="＜不安臨界-1＞犯人と同じエリアにいるキャラクター１人に不安カウンターを１つ置く。";
		}
		if($i==7){
			$sample1="猟奇殺人";
			$sample2="＜不安臨界＋１＞＜Exゲージ非増加＞「殺人事件」と「不安拡大」をこの順で発生させる。（結果、Exゲージは２増加する）";
		}
		if($i==8){
			$sample1="偽装自殺";
			$sample2="犯人にExカードAを置く。ExカードAが置かれたキャラクターに主人公はカードを置くことができない。";
		}
		if($i==9){
			$sample1="不和";
			$sample2="犯人と同じエリアにいるキャラクターのうち、友好カウンターの置かれた１人からすべての友好カウンターを取り除く";
		}
		if($i==10){
			$sample1="クローズドサークル";
			$sample2="犯人のいるボードを指定する。事件発生の日を含め３日間、そのボードからの移動とボードへの移動を禁止する。";
		}
		if($i==11){
			$sample1="銀の銃弾";
			$sample2="＜Exゲージ非増加＞このフェイズの終了時にループを終了させる。";
		}
	}
	print qq(<tr><td>$i</td><td id="$tmp1" ><input type="text"name="$tmp1" size="20" value="$sample1"></td><td id="$tmp2"><textarea name="$tmp2" rows="3" cols="40">$sample2</textarea></td><td id="$tmp3"><input type="text"  name="$tmp3" size="20"></td></tr>);
}

if($FORM{'custom'} eq "2"){
	$tmp1="4";
	$tmp2="8";
	$tmp3="ループ中の相談禁止。\n最後の戦いなし。\n時の狭間あり。マゾいプレイヤーはなしでもよい。";
}else{
	$tmp1="";
	$tmp2="";
	$tmp3="";
}
print "</table>";
if($FORM{'custom'} eq "0"){
	print qq|<input type="hidden" name="map1" value="学校"><input type="hidden" name="map2" value="神社"><input type="hidden" name="map3" value="都市"><input type="hidden" name="map4" value="病院">|;
	print qq|<input type="hidden" name="set" value="Basic Tragedy">|;
}elsif($FORM{'custom'} eq "3"){
		print qq|<input type="hidden" name="map1" value="学校"><input type="hidden" name="map2" value="神社"><input type="hidden" name="map3" value="都市"><input type="hidden" name="map4" value="病院">|;
	print qq|<input type="hidden" name="set" value="Visual Novel">|;
}	else{
}
print <<END;

<table>
<tr><th>ループ回数</th><td id="loop" ><input type="text" style="ime-mode:disabled;" name="loop" size="5" class="number" value="$tmp1"></td><th>１ループ日数</th><td id="loopday"><input type="text" class="number" name="loopday" size="10" value="$tmp2"></td></tr>
</table>
<table>
<tr><th>特別ルール</th></tr>
<tr><td><textarea cols="60" rows="5" name="text">$tmp3</textarea></td></tr>
</table>

<input type="submit" value="脚本決定" id="submitbutton" style="font-size:200%">
<input type="reset" value="リセット">
<input type="hidden" name="mode" value="enter2">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="entry" value="$FORM{'entry'}">
<input type="hidden" name="hero" value="writer">
<input type="hidden"  id="custom" name="custom" value="$FORM{'custom'}">
</form>
</body>
</html>
END
}
#==================セーブリセット ====
sub resetSave{
	open(FILE, ">$SAVEFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	print FILE "char\@0\@3,0,3,0,0,0,0,220,170,0&char\@1\@3,1,3,1,0,0,0,260,170,0&char\@2\@3,2,3,2,0,0,0,300,170,0&char\@3\@2,0,2,0,0,0,0,220,30,0&char\@4\@1,0,1,0,0,0,0,10,170,0&char\@5\@1,1,1,1,0,0,0,50,170,0&char\@6\@1,2,1,2,0,0,0,90,170,0&char\@7\@0,0,0,0,0,0,0,10,30,0&char\@8\@0,1,0,1,0,0,0,50,30,0&plhand\@0\@-1,-1,0,0,0,2,0,0,0,0&plhand\@1\@-1,-1,0,0,1,0,0,0,0,0&plhand\@2\@-1,-1,0,0,2,1,0,0,0,0&gmhand\@3\@-1,-1,0,0,0,0&gmhand\@4\@-1,-1,0,0,0,0&gmhand\@5\@-1,-1,0,0,0,0&board\@0\@0&board\@1\@0&board\@2\@0&board\@3\@0&scenario\@0&phase\@1,1,0";
		close(FILE);
}
#==================脚本データセーブ ====
sub writeScenario{	

	$FORM{'text'}=~ s/\x0D\x0A/<br>/g;
	makeOpenSheet();
	if($FORM{'custom'} eq "1"){
		makeCustomCloseSheet();
	}elsif($FORM{'custom'}>=6){
		makeFirstCloseSheet();
	}else{
		makeCloseSheet();
	}
}
#==================脚本データクローズシート====
sub makeCloseSheet{
	open(FILE, ">$CLOSESHEET")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	print FILE <<END;
<!--Content-type: text/html; charset=$CHARSET\n-->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<!--<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT"> -->
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="../rooper.css">
<style>
table {
		width:640px;
		text-align:center;
	}
th {
	background-color:#333333;
}	
td {
		font-weight:bold;
		border-width:2px;

}
p {
	text-indent:1em;
	}
</style>
<script language="JavaScript">
</script>
<title>惨劇RoopeR</title>
</head>
<title>シート</title></head>
<body>
<h1>脚本</h1>

END
#//2013/3/7追記↓↓
if($FORM{'selectedversion'} eq "selectedversion"){
for(my $i=0;$i<9;$i++){
		$FORM{'jobun'.$i} =~ s/&lt;/</g;
		$FORM{'jobun'.$i} =~ s/&gt;/>/g;
		$FORM{'skill'.$i} =~ s/&lt;/</g;
		$FORM{'skill'.$i} =~ s/&gt;/>/g;
}
		$FORM{'ruleYadd'} =~ s/&lt;/</g;
		$FORM{'ruleYadd'} =~ s/&gt;/>/g;
		$FORM{'ruleX1add'} =~ s/&lt;/</g;
		$FORM{'ruleX1add'} =~ s/&gt;/>/g;
		$FORM{'ruleX2add'} =~ s/&lt;/</g;
		$FORM{'ruleX2add'} =~ s/&gt;/>/g;
	print FILE <<END;
<table>
<tr><th></th><th>ルール名</th><th>追加ルール</th></tr>
<tr><th>ルールY</th><td>$FORM{'ruleY'}</td><td style="text-align:left">$FORM{'ruleYadd'}</td></tr>
<tr><th>ルールX1</th><td>$FORM{'ruleX1'}</td><td style="text-align:left">$FORM{'ruleX1add'}</td></tr>
<tr><th>ルールX2</th><td>$FORM{'ruleX2'}</td><td style="text-align:left">$FORM{'ruleX2add'}</td></tr>
</table>
<table>
<tr id="chartablehead"><th>人物</th><th>役職</th><th>条文\能\力</th><th>\能\力</th></tr>
<tr id="chartabletr0"><td>男子学生</td><td>$FORM{'shonen'}</td><td>$FORM{'jobun0'}</td><td style="text-align:left">$FORM{'skill0'}</td></tr>
<tr id="chartabletr1"><td>女子学生</td><td>$FORM{'shojo'}</td><td>$FORM{'jobun1'}</td><td style="text-align:left">$FORM{'skill1'}</td></tr>
<tr id="chartabletr2"><td>お嬢様</td><td>$FORM{'ojo'}</td><td>$FORM{'jobun2'}</td><td style="text-align:left">$FORM{'skill2'}</td></tr>
<tr id="chartabletr3"><td>巫女</td><td>$FORM{'miko'}</td><td>$FORM{'jobun3'}</td><td style="text-align:left">$FORM{'skill3'}</td></tr>
<tr id="chartabletr4"><td>刑事</td><td>$FORM{'keiji'}</td><td>$FORM{'jobun4'}</td><td style="text-align:left">$FORM{'skill4'}</td></tr>
<tr id="chartabletr5"><td>サラリーマン</td><td>$FORM{'salary'}</td><td>$FORM{'jobun5'}</td><td style="text-align:left">$FORM{'skill5'}</td></tr>
<tr id="chartabletr6"><td>情報屋</td><td>$FORM{'joho'}</td><td>$FORM{'jobun6'}</td><td style="text-align:left">$FORM{'skill6'}</td></tr>
<tr id="chartabletr7"><td>医者</td><td>$FORM{'isha'}</td><td>$FORM{'jobun7'}</td><td style="text-align:left">$FORM{'skill7'}</td></tr>
<tr id="chartabletr8"><td>入院患者</td><td>$FORM{'kanja'}</td><td>$FORM{'jobun8'}</td><td style="text-align:left">$FORM{'skill8'}</td></tr>
</table>
<table>
<tr><th>日数</th><th>事件</th><th>事件効果</th><th>犯人</th></tr>
END
#//2013/3/7追記↑↑
}else{
	print FILE <<END;
<table>
<tr><th>ルールY</th><td>$FORM{'ruleY'}</td></tr>
<tr><th>ルールX1</th><td>$FORM{'ruleX1'}</td></tr>
<tr><th>ルールX2</th><td>$FORM{'ruleX2'}</td></tr>
</table>
<table>
<tr id="chartablehead"><th>人物</th><th>役職</th></tr>
<tr id="chartabletr0"><td>男子学生</td><td>$FORM{'shonen'}</td></tr>
<tr id="chartabletr1"><td>女子学生</td><td>$FORM{'shojo'}</td></tr>
<tr id="chartabletr2"><td>お嬢様</td><td>$FORM{'ojo'}</td></tr>
<tr id="chartabletr3"><td>巫女</td><td>$FORM{'miko'}</td></tr>
<tr id="chartabletr4"><td>刑事</td><td>$FORM{'keiji'}</td></tr>
<tr id="chartabletr5"><td>サラリーマン</td><td>$FORM{'salary'}</td></tr>
<tr id="chartabletr6"><td>情報屋</td><td>$FORM{'joho'}</td></tr>
<tr id="chartabletr7"><td>医者</td><td>$FORM{'isha'}</td></tr>
<tr id="chartabletr8"><td>入院患者</td><td>$FORM{'kanja'}</td></tr>
</table>
<table>
<tr><th>日数</th><th>事件</th><th>事件効果</th><th>犯人</th></tr>
END
}
for($i=1;$i<=$FORM{'loopday'};$i++){
	$tmpday = "day".$i;
	$tmphan = "han".$i;
	$tmp    = "kouka".$i;
	print FILE "<tr><td>$i</td><td>$FORM{$tmpday}</td><td style='text-align:left;'>$FORM{$tmp}</td><td>$FORM{$tmphan}</td></tr>";
}

print FILE <<END;
</table>
<table>
<tr><th>ループ回数</th><td>$FORM{'loop'}</td><th>１ループ日数</th><td>$FORM{'loopday'}</td></tr>
</table>
END
if($FORM{"custom"}==0||$FORM{"custom"}==3){
print FILE "<table>";
print FILE qq|<tr><th>惨劇セット</th><td style="border-width:2px;">$FORM{'set'}</td></tr>|;
print FILE "</table>";
print FILE "<table>";
print FILE qq|<tr><th>使用マップ</th><td>$FORM{'map1'}</td><td>$FORM{'map2'}</td><td>$FORM{'map3'}</td><td>$FORM{'map4'}</td></tr>|;
print FILE "</table>";
}

if(!($FORM{'sodan'} eq "")){
	print FILE "<table>";
	print FILE qq|<tr><th>相談</th><td>$FORM{'sodan'}</td></tr>|;
	print FILE "</table>";
}

if(!($FORM{'text'} eq "")){
	print FILE <<END;
<table>
<tr><th>特別ルール</th></tr>
<tr><td>$FORM{'text'}</td></tr>
</table>
END
}
#シナリオの特徴
$FORM{'tokutyo'} =~ s/\r//; $FORM{'tokutyo'} =~ s/\n//;

if(!($FORM{'tokutyo'} eq "")){
	$FORM{'tokutyo'}=~ s|\\n|</p><p>|g;
	$FORM{'tokutyo'}=~ s|\\n|</p><p>|g;
	print FILE "<table>";
	print FILE qq|<tr><th>シナリオの特徴</th></tr><tr><td style="text-align:left;"><p>$FORM{'tokutyo'}</p></td></tr>|;
	print FILE "</table>";
}
#脚本家への指針
$FORM{'sisin'} =~ s/\r//; $FORM{'sisin'} =~ s/\n//;$FORM{'sisin'}=~ s|\\n|</p><p>|g;
if(!($FORM{'sisin'} eq "")){
#	$FORM{'sisin'}=~ s|\\n|</p><p>|g;
	print FILE "<table>";
	print FILE qq|<tr><th>脚本家への指針</th></tr><tr><td style="text-align:left;"><p>$FORM{'sisin'}</p></td></tr>|;
	print FILE "</table>";
}
	$FORM{"joken1"} =~ s/\r//;
	$FORM{"joken1"} =~ s/\n//;
if(!($FORM{"joken1"} eq "")){print FILE qq|<table><tr><th colspan="2">脚本家の勝利条件</th></tr>|;}
for($i=1;$i<=5;$i++){
	$tmp = "joken".$i;
	$FORM{$tmp} =~ s/\r//;
	$FORM{$tmp} =~ s/\n//;
	if(!($FORM{$tmp} eq "")){
		my ($_1, $_2) = split(/:/, $FORM{$tmp});
		print FILE qq|<tr><th rowspan="2">$i</th><th >$_1</th></tr>|;
		print FILE qq|<tr><td>$_2|;
		print FILE "</td></tr>";
	}
}
if(!($FORM{"joken1"} eq "")){print FILE "</table>";}

print FILE <<END;
</body>
</html>

END
	close(FILE);
}

sub makeOpenSheet{
		open(FILE, ">$OPENSHEET")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	print FILE <<END;
<!--Content-type: text/html; charset=$CHARSET\n-->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<!--<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT"> -->
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="../$CSSPATH/rooper.css">
<style>
table {
		width:640px;
		text-align:center;
	}
th {
	background-color:#333333;
}	
td {
		font-weight:bold;
		border-width:2px;

}
p {
	text-indent:1em;
	}
</style>
<script language="JavaScript">
</script>
<title>惨劇RoopeR</title>
</head>
<title>シート</title></head>
<body>
<h1>公開シート</h1>
<table>
<tr><th>ループ回数</th><td>$FORM{'loop'}</td><th>１ループ日数</th><td>$FORM{'loopday'}</td></tr>
</table>
END
#if($FORM{"custom"}==0||$FORM{"custom"}==3){
if($FORM{'custom'} eq "1"){
	$FORM{'set'}="Originail Tragedy";
}elsif($FORM{'custom'} eq "2"){
	$FORM{'set'}="惨劇RoopeRα版";
}elsif($FORM{'custom'} eq "3"){
	$FORM{'set'}="Visual Novel";
}elsif($FORM{'custom'} eq "4"){
	$FORM{'set'}="Haunted Stage";
}elsif($FORM{'custom'} eq "5"){
	$FORM{'set'}="Mystery Circle";
}elsif($FORM{'custom'} eq "6"){
	$FORM{'set'}="First Steps";
}elsif($FORM{'custom'} eq "7"){
	$FORM{'set'}="Basic Tragedy χ";
}elsif($FORM{'custom'} eq "8"){
	$FORM{'set'}="Mystery Circle χ";
}elsif($FORM{'custom'} eq "9"){
	$FORM{'set'}="Haunted Stage χ";
}elsif($FORM{'custom'} eq "10"){#2013.11.07.add
	$FORM{'set'}="Another Horizon";
}else{
	$FORM{'set'}="Basic Tragedy";
}
$FORM{'map1'}="病院";
$FORM{'map2'}="都市";
$FORM{'map3'}="神社";
$FORM{'map4'}="学校";

print FILE "<table>";
print FILE qq|<tr><th>惨劇セット</th><td style="border-width:2px;">$FORM{'set'}</td></tr>|;
print FILE "</table>";
print FILE "<table>";
print FILE qq|<tr><th>使用マップ</th><td>$FORM{'map1'}</td><td>$FORM{'map2'}</td><td>$FORM{'map3'}</td><td>$FORM{'map4'}</td></tr>|;
print FILE "</table>";
#}

if(!($FORM{'sodan'} eq "")){
	print FILE "<table>";
	print FILE qq|<tr><th>相談</th><td>$FORM{'sodan'}</td></tr>|;
	print FILE "</table>";
}
	print FILE <<END;
<table>
<tr><th>日数</th><th>事件\予\定\</th><th>事件効果</th></tr>
END

for($i=1;$i<=$FORM{'loopday'};$i++){
	$tmpday = "day".$i;
	$tmp    = "kouka".$i;
	print FILE "<tr><td>$i</td><td>$FORM{$tmpday}</td><td style='text-align:left;'>$FORM{$tmp}</td></tr>";
}

print FILE <<END;
</table>
END
$FORM{'text'} =~ s/\r//;$FORM{'text'} =~ s/\n//;
if(!($FORM{'text'} eq "")){
	print FILE <<END;
<table>
<tr><th>特別ルール</th></tr>
<tr><td>$FORM{'text'}</td></tr>
</table>
END
}
print FILE <<END;

</body>
</html>

END
	close(FILE);
}
#================== オリジナル脚本作成頁作成 ====
sub printCustomScenarioPage{

print "Content-type: text/html; charset=$CHARSET\n";
print "Pragma: no-cache\n";
print "Cache-Control: no-cache\n";
print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n";
print "\n";

	print <<END;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<!--<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT"> -->
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=$CHARSET">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/config.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/custom.js"></script>
<script language="JavaScript">
</script>
<title>惨劇RoopeR</title>
</head>
<title>シート</title></head>
<body>
<h1>脚本</h1>
<hr>
<font color="red">※リセットを忘れると動かないことがあります。</font>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<input type="hidden" name="mode" value="resetsave">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="custom" value="1">
<input type="submit" value="現在のゲームボードをリセット" style="font-size:200%">
<input type="hidden" name="entry" value="$FORM{'entry'}">
</form>
<hr>
<button type="button" name="" onclick="customform('rule.csv','text')" style="font-size:150%">ルールのアップロード</button>
<br>
※文字コードUTF-8で20kb以下のtxtまたはcsv形式。
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<table>
<tr><th>ルールY</th><td><input type="text" name="ruleY" size="40"></td></tr>
<tr><th>ルールX1</th><td><input type="text" name="ruleX1" size="40"></td></tr>
<tr><th>ルールX2</th><td><input type="text" name="ruleX2" size="40"></td></tr>
</table>
<hr>
<button type="button" name="" onclick="customform('char.csv','text')" style="font-size:150%">キャラクターのアップロード</button>
<br>
※文字コードUTF-8で20kb以下のtxtまたはcsv形式。
<table>
<tr><th>人物</th><th>役職</th><th>画像</th><th>アップロード<br>（35×50pxのpng形式20kb以下）</th></tr>
END
my $i;
for($i=0;$i<13;$i++){
	my $j=$i+1;
	print qq|<tr id="chartr$i"><input type="hidden" name="customcharname$i" id="customcharname$i"  value="char$i"><td id="customcharnameprev$i">キャラクター$j</td><td><input type="text" name="char$i" size="30" value="パー\ソ\ン"></td><td><img id="customchar$i" alt="char$i" src="custom/img/character/char$i.png" style="width:35px;height:50px;"></td><td><button type="button" name="" onclick="customform('char$i.png','img')" style="font-size:100%">画像ファイルアップロード</button></td></tr>|;
}
	print <<END;
</table>
<input type="hidden" name="charnum" value="13" id="charnum">
<hr>
<table>
<tr><th>ボード</th><th>画像</th><th>アップロード</th><td rowspan="5"><img src="custom/img/board.png" alt="board" name="board" id="boardimg"></td><td rowspan="5"><button type="button" name="" onclick="customform('board.png','img')" style="font-size:100%">画像ファイルアップロード</button><br>(400×283pxのpng形式<br>250kb以下）</td></tr>
END
for($i=0;$i<4;$i++){
	$j=$i+1;
	print qq|<tr><input type="hidden" name="customboard$i" id="customboard$i"  value="ボード$i"><td id="customboardprev$i">ボード$j</td><td><img id="customboard$i" alt="char$i" src="custom/img/character/board$i.png" style="width:35px;height:50px;"></td><td><button type="button" name="" onclick="customform('board$i.png','img')" style="font-size:100%">画像ファイルアップロード</button></td></tr>|;
}
	print <<END;
</table>
<hr>
<table>
END
	for($i=0;$i<3;$i++){
	$j=$i+1;
	print qq|<tr><td>主人公$j</td><td><img id="customhero$i" alt="hand$i" src="custom/img/hand/hero$i.png" style="width:35px;height:50px;"></td><td><button type="button" name="" onclick="customform('hero$i.png','img')" style="font-size:100%">画像ファイルアップロード</button></td></tr>|;
}
print qq|<tr><td>脚本家</td><td><img id="customwrite" alt="writer" src="custom/img/hand/write.png" style="width:35px;height:50px;"></td><td><button type="button" name="" onclick="customform('write.png','img')" style="font-size:100%">画像ファイルアップロード</button></td></tr>|;

print <<END;
</table>
<hr>
<table>
<tr><th>日数</th><th>事件</th><th>事件効果</th><th>犯人</th></tr>
END
for ($i=1;$i<=10;$i++){
	$tmp1="day".$i;
	$tmp2="kouka".$i;
	$tmp3="han".$i;
	$sample1="";
	$sample2="";
	if($i==1){
		$sample1="殺人事件";
		$sample2="可\能\ならば犯人と同じエリアにいる犯人以外の任意のキャラクター１人を死亡させる。";
	}
	if($i==2){
		$sample1="不安拡大";
		$sample2="任意のキャラクター１人に不安カウンターを２つ置き、任意の別のキャラクター１人に暗躍カウンターを１つ置く。";
	}
	if($i==3){
		$sample1="自殺";
		$sample2="犯人は死亡する。";
	}
	if($i==4){
		$sample1="病院の事件";
		$sample2="病院に暗躍カウンターが１つ以上置かれている場合、病院にいるキャラクター全員が死亡する。さらに、病院に暗躍カウンターが２つ以上置かれている場合、主人公は死亡する。";
	}
	if($i==5){
		$sample1="邪気の汚染";
		$sample2="神社に暗躍カウンターを２つ置く。";
	}
	print qq(<tr><td>$i</td><td><input type="text" name="$tmp1" size="20" value="$sample1"></td><td><textarea name="$tmp2" rows="3" cols="40">$sample2</textarea></td><td><input type="text" name="$tmp3" size="20"></td></tr>);
}

print <<END;
</table>
<hr>
<table>
<tr><th>ループ回数</th><td><input type="text" name="loop" size="5" class="number"></td><th>１ループ日数</th><td><input type="text" class="number" name="loopday" size="10"></td></tr>
</table>
<table>
<tr><th>特別ルール</th></tr>
<tr><td><textarea cols="60" rows="5" name="text"></textarea></td></tr>
</table>

<input type="submit" value="脚本決定" style="font-size:200%">
<input type="reset" value="リセット">
<input type="hidden" name="mode" value="enter2">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="entry" value="$FORM{'entry'}">
<input type="hidden" name="custom" value="1">
<input type="hidden" name="hero" value="writer">
</form>
</body>
</html>
END
}
#===================================================================================
sub makeCustomCloseSheet{

	open(FILE, ">$CLOSESHEET")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };

	print FILE <<END;
<!--Content-type: text/html; charset=$CHARSET\n-->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<!--<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT"> -->
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="../rooper.css">

<script language="JavaScript">
</script>
<title>惨劇RoopeR</title>
</head>
<title>シート</title></head>
<body>
<h1>脚本</h1>
<table>
<tr><th>ルールY</th><td>$FORM{'ruleY'}</td></tr>
<tr><th>ルールX1</th><td>$FORM{'ruleX1'}</td></tr>
<tr><th>ルールX2</th><td>$FORM{'ruleX2'}</td></tr>
<table>
<tr><th>人物</th><th>役職</th></tr>
END
	
	$max=$FORM{"charnum"};
for($i=0;$i<$max;$i++){
	$tmp="customcharname".$i;
	$tmp1="char".$i;
	print FILE "<tr><td>$FORM{$tmp}</td><td>$FORM{$tmp1}</td></tr>";
}

	print FILE <<END;
</table>
<table>
<tr><th>日数</th><th>事件</th><th>事件効果</th><th>犯人</th></tr>
END
	
for($i=1;$i<=$FORM{'loopday'};$i++){
	$tmpday = "day".$i;
	$tmphan = "han".$i;
	$tmp    = "kouka".$i;
	print FILE "<tr><td>$i</td><td>$FORM{$tmpday}</td><td>$FORM{$tmp}</td><td>$FORM{$tmphan}</td></tr>";
}

print FILE <<END;
</table>
<table>
<tr><th>ループ回数</th><td>$FORM{'loop'}</td><th>１ループ日数</th><td>$FORM{'loopday'}</td></tr>
</table>
<table>
<tr><th>特別ルール</th></tr>
<tr><td>$FORM{'text'}</td></tr>
</table>
</body>
</html>
END
	close(FILE);

	open(FILE, ">$CHARFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	$max=$FORM{"charnum"};
	for($i=0;$i<$max;$i++){
		$tmp="customcharname".$i;
		print FILE "$FORM{$tmp}\n";
	}
	for($i=0;$i<4;$i++){
		$tmp="customboard".$i;
		print FILE "$FORM{$tmp}\n";
	}
	close(FILE);

}
#===================================================================================
#==================ルーパーχ脚本作成頁作成 ====
sub printFirstScenarioPage{
print "Content-type: text/html; charset=$CHARSET\n";
print "Pragma: no-cache\n";
print "Cache-Control: no-cache\n";
print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n";
print "\n";
	print <<END;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<!--<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT"> -->
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=$CHARSET">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/jquery.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/config.js"></script>
<script type="text/javascript" charset="UTF-8" language="JavaScript" src="$JSPATH/js/first_scenariomake.js"></script>
<script language="JavaScript">
jQuery.event.add(window, "load",function(event){
changeselectbox();
});
</script>
<title>シート</title></head>
<body>
<h1>脚本</h1>
<hr>
<strong>サンプルシナリオ</strong>：<select id="samplescenario">
<option value="-1">未選択</option>
</select>
<hr>
<form action="$ENV{'SCRIPT_NAME'}" id="mainform" method="POST">
<strong style='font-size:16pt'>タイトル</strong>：<input type='text' name='scenarioTitle' id='scenarioTitle' style='font-size:16pt' size='40'>
<hr>
<table>
<tr><th></th><th></th><th>追加役職</th><th style="width:500px;">追加ルール</th></tr>
<tr><th>ルールY</th><td id="ruleY" ><input type="text" name="ruleY" size="40"></td><td id="ruleYrole"></td><td id="ruleYskill"></td></tr>
<tr><th>ルールX1</th><td id="ruleX1"><input type="text" name="ruleX1" size="40"></td><td id="ruleX1role"></td><td id="ruleX1skill"></td></tr>
END
if($FORM{'custom'} ne '6'){
	print qq|<tr id="rule2"><th>ルールX2</th><td id="ruleX2"><input type="text" name="ruleX2" size="40"></td><td id="ruleX2role"></td><td id="ruleX2skill"></td></tr>|;
}
	print <<END;
</table>
<hr>
<table>
<tr><th>使用</th><th>画像</th><th>人物</th><th>役職</th><th>条文\能\力</th><th style="width:500px;">役職\能\力</th></tr>
END
my $i;
for($i=0;$i<20;$i++){
	my $j=$i+1;
	if($i==0||$i==1||$i==3||$i==5||$i==7||$i==8){
		print qq|<tr id="chartr$i"><input type="hidden" name="customcharname$i" id="customcharname$i"  value="char$i"><td><input type="checkbox" name="usecheck_$i" id="usecheck_$i" checked></td><td><img id="customchar$i" alt="char$i" src="$CHARIMGPATH/char$i.png" style="width:35px;height:50px;"></td><td id="customcharnameprev$i">キャラクター$j</td><td id="char$i"><input type="text" name="char$i" size="30" value="パー\ソ\ン"></td><td id="jobunbox$i"></td><td id="skillbox$i"></td></tr>|;
	}else{
		print qq|<tr id="chartr$i"><input type="hidden" name="customcharname$i" id="customcharname$i"  value="char$i"><td><input type="checkbox" name="usecheck_$i" id="usecheck_$i"></td><td><img id="customchar$i" alt="char$i" src="$CHARIMGPATH/char$i.png" style="width:35px;height:50px;"></td><td id="customcharnameprev$i">キャラクター$j</td><td id="char$i"><input type="text" name="char$i" size="30" value="パー\ソ\ン"></td><td id="jobunbox$i"></td><td id="skillbox$i"></td></tr>|;
	}
}
	print <<END;
</table>
<input type="hidden" name="charnum" value="6" id="charnum">

<hr>
<!--table-->
END

print <<END;
<!--</table>-->
<hr>
<table>
<tr><th>日数</th><th>事件</th><th style="width:500px;">事件効果</th><th>犯人</th></tr>
END
for ($i=1;$i<=10;$i++){
	$tmp1="day".$i;
	$tmp2="kouka".$i;
	$tmp3="han".$i;
	$sample1="";
	$sample2="";

	print qq(<tr id='jikentr_$i'><td>$i</td><td id="day$i"><input type="text" name="$tmp1" size="20" value="$sample1"></td><td id="kouka$i"><textarea name="$tmp2" rows="3" cols="40">$sample2</textarea></td><td id="han$i"><input type="text" name="$tmp3" size="20"></td></tr>);
}

print <<END;
</table>
<hr>
<table>
<tr><th>ループ回数</th><td id="loop"><input type="text" name="loop" size="5" class="number"></td><th>１ループ日数</th><td id="loopday"><input type="text" class="number" name="loopday" size="10"></td><th>神格登場ループ</th><td id="sinkaku_add_loop"><input type="text" class="number" name="sinkaku_loopday" size="10"></td></tr>
</table>
<table>
<tr><th>特別ルール</th></tr>
<tr><td><textarea cols="60" rows="5" name="text" id="opentext">相談不可/相談可 \n大物のテリトリー：[] \nその他特記事項を記入。\n公開シート。</textarea></td></tr>
</table>
<table>
<tr><th>脚本家メモ</th></tr>
<tr><td><textarea cols="60" rows="5" name="sisin" id="closetext">最初の手札の置き方や、勝利条件などの脚本家用メモ。\n非公開シート。主人公には公開されません。</textarea></td></tr>
</table>

<input type="submit" value="脚本決定" id="submitbutton" style="font-size:200%">
<input type="reset" value="リセット">
<input type="hidden" name="mode" value="enter2">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="entry" value="$FORM{'entry'}">
<input type="hidden" name="custom" id="custom" value="$FORM{'custom'}">
<input type="hidden" name="hero" value="writer">
</form>
</body>
</html>
END
}
#===================================================================================
sub makeFirstCloseSheet{
	open(FILE, ">$CLOSESHEET")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };

	print FILE <<END;
<!--Content-type: text/html; charset=$CHARSET\n-->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EM"
   "http://www.w3.org/TR/html4/strict.dtd">
   <!-- saved from url=(0014)about:internet-->
<html lang="ja-JP">
<head>

<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<!--<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT"> -->
<meta http-equiv="Expires" content="0"> 
<meta http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/../rooper.css">

<script language="JavaScript">
</script>
<title>惨劇RoopeRΧ</title>
</head>
<title>シート</title></head>
<body>
<h1>脚本:$FORM{'scenarioTitle'}</h1>
END
if($FORM{'custom'} eq "6"){
	$FORM{'set'}="First Steps";
}elsif($FORM{'custom'} eq "7"){
	$FORM{'set'}="Basic Tragedy χ";
}elsif($FORM{'custom'} eq "8"){
	$FORM{'set'}="Mystery Circle χ";
}elsif($FORM{'custom'} eq "9"){
	$FORM{'set'}="Haunted Stage χ";
}elsif($FORM{'custom'} eq "10"){#2013.11.07.add
	$FORM{'set'}="Another Horizon";
}else{
	$FORM{'set'}="Basic Tragedy";
}
$FORM{'map1'}="病院";
$FORM{'map2'}="都市";
$FORM{'map3'}="神社";
$FORM{'map4'}="学校";

print FILE "<table>";
print FILE qq|<tr><th>惨劇セット</th><td style="border-width:2px;">$FORM{'set'}</td></tr>|;
print FILE "</table>";
print FILE "<table>";
print FILE qq|<tr><th>使用マップ</th><td>$FORM{'map1'}</td><td>$FORM{'map2'}</td><td>$FORM{'map3'}</td><td>$FORM{'map4'}</td></tr>|;
print FILE "</table>";

	$FORM{'ruleYadd'} =~ s/&lt;/</g;
	$FORM{'ruleYadd'} =~ s/&gt;/>/g;
	$FORM{'ruleX1add'} =~ s/&lt;/</g;
	$FORM{'ruleX1add'} =~ s/&gt;/>/g;
	$FORM{'ruleX2add'} =~ s/&lt;/</g;
	$FORM{'ruleX2add'} =~ s/&gt;/>/g;
	print FILE <<END;
<table>
<tr><th></th><th></th><th style="width:500px;">追加ルール</th></tr>
<tr><th>ルールY</th><td>$FORM{'ruleY'}</td><td>$FORM{'ruleYadd'}</td></tr>
<tr><th>ルールX1</th><td>$FORM{'ruleX1'}</td><td>$FORM{'ruleX1add'}</td></tr>
END
if($FORM{'custom'} ne '6'){
	print FILE "<tr><th>ルールX2</th><td>$FORM{'ruleX2'}</td><td>$FORM{'ruleX2add'}</td></tr>";
}
print FILE "<table>";
print FILE "<tr><th>人物</th><th>役職</th><th>条文\能\力</th><th style='width:500px;'>役職\能\力</th></tr>";

	$max=20;#$FORM{"charnum"}2013.11.7.up;
for($i=0;$i<$max;$i++){
	$tmp="customcharname".$i;
	$tmp1="char".$i;
	$tmp2='jobun'.$i;
	$FORM{$tmp2} =~ s/&lt;/</g;
	$FORM{$tmp2} =~ s/&gt;/>/g;
	$tmp3='skill'.$i;
	
	$FORM{$tmp3} =~ s/&lt;/</g;
	$FORM{$tmp3} =~ s/&gt;/>/g;
	$tmp4='usecheck_'.$i;
	if($FORM{$tmp4}){
		print FILE "<tr><td>$FORM{$tmp}</td><td>$FORM{$tmp1}</td><td>$FORM{$tmp2}</td><td style='text-align:left'>$FORM{$tmp3}</td></tr>";
	}
}

	print FILE <<END;
</table>
<table>
<tr><th>日数</th><th>事件</th><th style="width:500px;">事件効果</th><th>犯人</th></tr>
END
	
for($i=1;$i<=$FORM{'loopday'};$i++){
	$tmpday = "day".$i;
	$tmphan = "han".$i;
	$tmp    = "kouka".$i;
	print FILE "<tr><td>$i</td><td>$FORM{$tmpday}</td><td>$FORM{$tmp}</td><td>$FORM{$tmphan}</td></tr>";
}

print FILE <<END;
</table>
<table>
<tr><th>ループ回数</th><td id='loop'>$FORM{'loop'}</td><th>１ループ日数</th><td id='loopday'>$FORM{'loopday'}</td>
END
if($FORM{'usecheck_12'}){
	print FILE "<th>神格登場ループ</th><td id='sinkaku_add_loop'>$FORM{'sinkaku_add_loop'}</td>";
}
print FILE <<END;
</tr>
</table>
<table>
<tr><th style="width:500px;">特別ルール</th></tr>
<tr><td>$FORM{'text'}</td></tr>
</table>
END
#脚本家への指針
$FORM{'sisin'} =~ s/\r//; $FORM{'sisin'} =~ s/\n/<br>/g;$FORM{'sisin'}=~ s|\\n|</p><p>|g;
if(!($FORM{'sisin'} eq "")){
#	$FORM{'sisin'}=~ s|\\n|</p><p>|g;
	print FILE "<table>";
	print FILE qq|<tr><th>脚本家への指針</th></tr><tr><td style="text-align:left;width:600px;"><p>$FORM{'sisin'}</p></td></tr>|;
	print FILE "</table>";
}
	$FORM{"joken1"} =~ s/\r//;
	$FORM{"joken1"} =~ s/\n//;
if(!($FORM{"joken1"} eq "")){print FILE qq|<table><tr><th colspan="2">脚本家の勝利条件</th></tr>|;}
for($i=1;$i<=5;$i++){
	$tmp = "joken".$i;
	$FORM{$tmp} =~ s/\r//;
	$FORM{$tmp} =~ s/\n//;
	if(!($FORM{$tmp} eq "")){
		my ($_1, $_2) = split(/:/, $FORM{$tmp});
		print FILE qq|<tr><th rowspan="2">$i</th><th >$_1</th></tr>|;
		print FILE qq|<tr><td>$_2|;
		print FILE "</td></tr>";
	}
}
if(!($FORM{"joken1"} eq "")){print FILE "</table>";}

print FILE <<END;
</body>
</html>
END
	close(FILE);

	open(FILE, ">$SAVEFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	if($FORM{'custom'} eq "9"){
		print FILE "char\@0\@3,0,3,0,0,0,0,220,170,0&char\@1\@3,1,3,1,0,0,0,260,170,0&char\@2\@3,2,3,2,0,0,0,300,170,0&char\@3\@2,0,2,0,0,0,0,220,30,0&char\@4\@1,0,1,0,0,0,0,10,170,0&char\@5\@1,1,1,1,0,0,0,50,170,0&char\@6\@1,2,1,2,0,0,0,90,170,0&char\@7\@0,0,0,0,0,0,0,10,30,0&char\@8\@0,1,0,1,0,0,0,50,30,0&char\@9\@3,3,3,3,0,0,0,340,170,0&char\@10\@3,4,3,4,0,0,0,220,225,0&char\@11\@2,1,2,1,0,0,0,260,30,0&char\@12\@2,2,2,2,0,0,0,300,30,0&char\@13\@1,3,1,3,0,0,0,130,170,0&char\@14\@1,4,1,4,0,0,0,10,225,0&char\@15\@1,5,1,5,0,0,0,50,225,0&char\@16\@0,2,0,2,0,0,0,90,30,0&char\@17\@2,3,2,3,0,0,0,340,30,0&char\@18\@0,3,0,3,0,0,0,130,30,0&char\@19\@2,4,2,4,0,0,0,220,85,0,0,0&char\@20\@0,0,0,0,0,0,0,0,0,0,0&char\@21\@0,0,0,0,0,0,0,0,0,0,0&char\@22\@0,0,0,0,0,0,0,0,0,0,0&plhand\@0\@-1,-1,0,0,0,2,0,0,0,0&plhand\@1\@-1,-1,0,0,1,0,0,0,0,0&plhand\@2\@-1,-1,0,0,2,1,0,0,0,0&gmhand\@3\@-1,-1,0,0,0,0&gmhand\@4\@-1,-1,0,0,0,0&gmhand\@5\@-1,-1,0,0,0,0&board\@0\@0&board\@1\@0&board\@2\@0&board\@3\@0&scenario\@0&excounter\@0&phase\@1,1,0";
	}elsif($FORM{'custom'} eq "8"){
		print FILE "char\@0\@3,0,3,0,0,0,0,220,170,0,0&char\@1\@3,1,3,1,0,0,0,260,170,0,0&char\@2\@3,2,3,2,0,0,0,300,170,0,0&char\@3\@2,0,2,0,0,0,0,220,30,0,0&char\@4\@1,0,1,0,0,0,0,10,170,0,0&char\@5\@1,1,1,1,0,0,0,50,170,0,0&char\@6\@1,2,1,2,0,0,0,90,170,0,0&char\@7\@0,0,0,0,0,0,0,10,30,0,0&char\@8\@0,1,0,1,0,0,0,50,30,0,0&char\@9\@3,3,3,3,0,0,0,340,170,0,0&char\@10\@3,4,3,4,0,0,0,220,225,0,0&char\@11\@2,1,2,1,0,0,0,260,30,0,0&char\@12\@2,2,2,2,0,0,0,300,30,0,0&char\@13\@1,3,1,3,0,0,0,130,170,0,0&char\@14\@1,4,1,4,0,0,0,10,225,0,0&char\@15\@1,5,1,5,0,0,0,50,225,0,0&char\@16\@0,2,0,2,0,0,0,90,30,0,0&char\@17\@2,3,2,3,0,0,0,340,30,0,0&char\@18\@0,3,0,3,0,0,0,130,30,0,0&char\@19\@2,4,2,4,0,0,0,220,85,0,0,0&plhand\@0\@-1,-1,0,0,0,2,0,0,0,0&plhand\@1\@-1,-1,0,0,1,0,0,0,0,0&plhand\@2\@-1,-1,0,0,2,1,0,0,0,0&gmhand\@3\@-1,-1,0,0,0,0&gmhand\@4\@-1,-1,0,0,0,0&gmhand\@5\@-1,-1,0,0,0,0&board\@0\@0&board\@1\@0&board\@2\@0&board\@3\@0&scenario\@0&excounter\@0&phase\@1,1,0";
	}else{
		print FILE "char\@0\@3,0,3,0,0,0,0,220,170,0&char\@1\@3,1,3,1,0,0,0,260,170,0&char\@2\@3,2,3,2,0,0,0,300,170,0&char\@3\@2,0,2,0,0,0,0,220,30,0&char\@4\@1,0,1,0,0,0,0,10,170,0&char\@5\@1,1,1,1,0,0,0,50,170,0&char\@6\@1,2,1,2,0,0,0,90,170,0&char\@7\@0,0,0,0,0,0,0,10,30,0&char\@8\@0,1,0,1,0,0,0,50,30,0&char\@9\@3,3,3,3,0,0,0,340,170,0&char\@10\@3,4,3,4,0,0,0,220,225,0&char\@11\@2,1,2,1,0,0,0,260,30,0&char\@12\@2,2,2,2,0,0,0,300,30,0&char\@13\@1,3,1,3,0,0,0,130,170,0&char\@14\@1,4,1,4,0,0,0,10,225,0&char\@15\@1,5,1,5,0,0,0,50,225,0&char\@16\@0,2,0,2,0,0,0,90,30,0&char\@17\@2,3,2,3,0,0,0,340,30,0&char\@18\@0,3,0,3,0,0,0,130,30,0&char\@19\@2,4,2,4,0,0,0,220,85,0,0,0&plhand\@0\@-1,-1,0,0,0,2,0,0,0,0&plhand\@1\@-1,-1,0,0,1,0,0,0,0,0&plhand\@2\@-1,-1,0,0,2,1,0,0,0,0&gmhand\@3\@-1,-1,0,0,0,0&gmhand\@4\@-1,-1,0,0,0,0&gmhand\@5\@-1,-1,0,0,0,0&board\@0\@0&board\@1\@0&board\@2\@0&board\@3\@0&scenario\@0&excounter\@0&phase\@1,1,0";
	}
		close(FILE);

	for($i=0;$i<$max;$i++){
		if($i==12){
			$kaichar=$kaichar.$FORM{"customcharname$i"}.",".$FORM{"usecheck_$i"}.",".$FORM{"sinkaku_add_loop"}."\n";
		}else{
			$kaichar=$kaichar.$FORM{"customcharname$i"}.",".$FORM{"usecheck_$i"}."\n";
		}
	}

	open(FILE, ">$KAICHARFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 2) };
	print FILE $kaichar;
		close(FILE);

}
#===================================================================================
