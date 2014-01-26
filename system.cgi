#!/usr/bin/perl --

require "../rooper/jcode.pl";


$CHARSET       = 'Shift_JIS';		# 文字コード
$CHATFILE      = './dat/chat.dat';		# 発言ログファイル
$LOGFILE      = './dat/log.dat';		# 発言ログファイル
$CHARFILE = './dat/char.dat';
$MAXLINE       = 30;			# 最大ログ行数
my @char;
#フォームデータの取得
loadFormdata();
loadChatfile();
if($FORM{'custom'} ==1){
	open(FILE, "<$CHARFILE")
		or printErrorPage("ログファイルが開けません。");
	eval{ flock(FILE, 1) };
	@data = <FILE>;
	close(FILE);
	foreach $ln (@data) {
		chomp $ln;
		push(@char,$ln)
	}
}elsif($FORM{'custom'} ==2){
	@char=("男子学生","女子学生","お嬢様","巫女","刑事","サラリーマン","情報屋","医者","患者","神社","学校","病院","都市");
}elsif($FORM{'custom'} ==4){
	@char=("男子学生","女子学生","お嬢様","巫女","刑事","サラリーマン","情報屋","医者","患者","魔獣Ａ","魔獣Ｂ","魔獣Ｃ","病院","都市","神社","学校");
}elsif($FORM{'custom'} ==9){
	@char=("男子学生","女子学生","お嬢様","巫女","刑事","サラリーマン","情報屋","医者","患者","委員長","イレギュラー","異世界人","神格","アイドル","マスコミ","大物","ナース","手先","学者","幻想","魔獣Ａ","魔獣Ｂ","魔獣Ｃ","病院","都市","神社","学校");
}elsif($FORM{'custom'} >=6){
	@char=("男子学生","女子学生","お嬢様","巫女","刑事","サラリーマン","情報屋","医者","患者","委員長","イレギュラー","異世界人","神格","アイドル","マスコミ","大物","ナース","手先","学者","幻想","病院","都市","神社","学校");
}else{
	@char=("男子学生","女子学生","お嬢様","巫女","刑事","サラリーマン","情報屋","医者","患者","病院","都市","神社","学校");
}
if($FORM{'custom'} ==2){
	@plhand=("暗躍禁止","友好＋２","移動禁止","不安－１","移動↑↓","移動←→","友好＋１","不安＋１","不安－１","拡張B");
}else{
	@plhand=("暗躍禁止","友好＋２","移動禁止","不安－１","移動↑↓","移動←→","友好＋１","不安＋１","拡張A","拡張B");
}
@gmhand=("移動斜め","暗躍＋２","移動↑↓","移動←→","不安＋１","不安＋１","不安－１","暗躍＋１","友好禁止","不安禁止","拡張A","拡張B");

if($FORM{'mode'} eq 'phase6') {
	#脚本家フェイズ
	$text="脚本家が【$char[$FORM{'char3'}]】と【$char[$FORM{'char4'}]】と【$char[$FORM{'char5'}]】に手札をセットしました。";
	if($FORM{'leaderskip'}){$text=$text."<br><span class='namewriter'>リーダーの行動をスキップします。</span>";}
	$logtext=$text;
}elsif($FORM{'mode'} eq 'phase7') {
	$text="主人公が【$char[$FORM{'char'}]】に手札をセットしました。";
	$logtext=$text;
}elsif($FORM{'mode'} eq 'phase8') {
	$text="主人公が【$char[$FORM{'char'}]】に手札をセットしました。";
	$logtext=$text;
}elsif($FORM{'mode'} eq 'phase9') {
	if($FORM{'char0'} eq '-1'){
		$text="手札を公開しました。<span class='name0'>リーダーは行動カードセット禁止</span>、<span class='name1'>【$char[$FORM{'char1'}]】に”$plhand[$FORM{'hand1'}]”</span>、<span class='name2'>【$char[$FORM{'char2'}]】に”$plhand[$FORM{'hand2'}]”</span>、<span class='namewriter'>【$char[$FORM{'char3'}]】に”$gmhand[$FORM{'hand3'}]”</span>、【$char[$FORM{'char4'}]】に”$gmhand[$FORM{'hand4'}]”、<span class='namewriter'>【$char[$FORM{'char5'}]】に”$gmhand[$FORM{'hand5'}]”</span>、がセットされています。";
		$logtext="手札を公開しました。リーダーは行動カードセット禁止。【$char[$FORM{'char1'}]】に”$plhand[$FORM{'hand1'}]”、【$char[$FORM{'char2'}]】に”$plhand[$FORM{'hand2'}]”、【$char[$FORM{'char3'}]】に”$gmhand[$FORM{'hand3'}]”、【$char[$FORM{'char4'}]】に”$gmhand[$FORM{'hand4'}]”、【$char[$FORM{'char5'}]】に”$gmhand[$FORM{'hand5'}]”、がセットされています。";
	}elsif($FORM{'char1'} eq '-1'){
		$text="手札を公開しました。<span class='name0'>【$char[$FORM{'char0'}]】に”$plhand[$FORM{'hand0'}]”</span>、<span class='name1'>リーダーは行動カードセット禁止</span>、<span class='name2'>【$char[$FORM{'char2'}]】に”$plhand[$FORM{'hand2'}]”</span>、<span class='namewriter'>【$char[$FORM{'char3'}]】に”$gmhand[$FORM{'hand3'}]”</span>、【$char[$FORM{'char4'}]】に”$gmhand[$FORM{'hand4'}]”、<span class='namewriter'>【$char[$FORM{'char5'}]】に”$gmhand[$FORM{'hand5'}]”</span>、がセットされています。";
		$logtext="手札を公開しました。【$char[$FORM{'char0'}]】に”$plhand[$FORM{'hand0'}]”、リーダーは行動カードセット禁止、【$char[$FORM{'char2'}]】に”$plhand[$FORM{'hand2'}]”、【$char[$FORM{'char3'}]】に”$gmhand[$FORM{'hand3'}]”、【$char[$FORM{'char4'}]】に”$gmhand[$FORM{'hand4'}]”、【$char[$FORM{'char5'}]】に”$gmhand[$FORM{'hand5'}]”、がセットされています。";

	}elsif($FORM{'char2'} eq '-1'){
		$text="手札を公開しました。<span class='name0'>【$char[$FORM{'char0'}]】に”$plhand[$FORM{'hand0'}]”</span>、<span class='name1'>【$char[$FORM{'char1'}]】に”$plhand[$FORM{'hand1'}]”</span>、<span class='name2'>リーダーは行動カードセット禁止</span>、<span class='namewriter'>【$char[$FORM{'char3'}]】に”$gmhand[$FORM{'hand3'}]”</span>、【$char[$FORM{'char4'}]】に”$gmhand[$FORM{'hand4'}]”、<span class='namewriter'>【$char[$FORM{'char5'}]】に”$gmhand[$FORM{'hand5'}]”</span>、がセットされています。";
		$logtext="手札を公開しました。【$char[$FORM{'char0'}]】に”$plhand[$FORM{'hand0'}]”、【$char[$FORM{'char1'}]】に”$plhand[$FORM{'hand1'}]”、リーダーは行動カードセット禁止、【$char[$FORM{'char3'}]】に”$gmhand[$FORM{'hand3'}]”、【$char[$FORM{'char4'}]】に”$gmhand[$FORM{'hand4'}]”、【$char[$FORM{'char5'}]】に”$gmhand[$FORM{'hand5'}]”、がセットされています。";

	}else{
		$text="手札を公開しました。<span class='name0'>【$char[$FORM{'char0'}]】に”$plhand[$FORM{'hand0'}]”</span>、<span class='name1'>【$char[$FORM{'char1'}]】に”$plhand[$FORM{'hand1'}]”</span>、<span class='name2'>【$char[$FORM{'char2'}]】に”$plhand[$FORM{'hand2'}]”</span>、<span class='namewriter'>【$char[$FORM{'char3'}]】に”$gmhand[$FORM{'hand3'}]”</span>、【$char[$FORM{'char4'}]】に”$gmhand[$FORM{'hand4'}]”、<span class='namewriter'>【$char[$FORM{'char5'}]】に”$gmhand[$FORM{'hand5'}]”</span>、がセットされています。";
		$logtext="手札を公開しました。【$char[$FORM{'char0'}]】に”$plhand[$FORM{'hand0'}]”、【$char[$FORM{'char1'}]】に”$plhand[$FORM{'hand1'}]”、【$char[$FORM{'char2'}]】に”$plhand[$FORM{'hand2'}]”、【$char[$FORM{'char3'}]】に”$gmhand[$FORM{'hand3'}]”、【$char[$FORM{'char4'}]】に”$gmhand[$FORM{'hand4'}]”、【$char[$FORM{'char5'}]】に”$gmhand[$FORM{'hand5'}]”、がセットされています。";
	}
}elsif($FORM{'mode'} eq 'phase5') {#2013.06.20.add
	$text="第$FORM{'loop'}ループ、$FORM{'day'}日目を開始します。";
	$logtext=$text;
}elsif($FORM{'mode'} eq 'loopend') {#2013.06.20.add
	$text="第$FORM{'loop'}ループを終了します。";
	$logtext=$text;
}

writeRemark("[SYSTEM]", "","$text",$FORM{'hero'},"$logtext");

print "Content-type: text/html\n";
print "\n";
print "<html>\n";
print "<head>\n";
print "<title>OK</title>\n";
print "</head>\n";
print "<body bgcolor=\"#ffcccc\">\n";
print "OK.\n";
print "</body>\n";
print "</html>\n";

exit(0);


#======================== エラーページ出力 ====
sub printErrorPage
{
	print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="rooper.css">
<title>ちゃっと</title></head>
<body><h1>エラー</h1><p>$_[0]</p></body>
</html>
END
	
	exit;
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


#========================== 発言を書き込む ====
sub writeRemark
{
	my ($name, $email, $text,$hero,$logtext) = @_;
		my ($sec, $min, $hour, $mday, $mon, $year, $wday)
		= localtime(time);
	my $date = sprintf("%02d/%02d %02d:%02d",
		++$mon, $mday, $hour, $min);
	unshift @DATA, "$date\t$name\t$email\t$text\t$hero\n";
	unshift @LOG, "$date\t$name\t$email\t$logtext\n";
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
#=========================== URLエンコード ====
sub urlencode
{
	my $value = shift @_;
	
	$value =~ tr/ /+/;
	$value =~ s/(\W)/sprintf("%%%02X", ord($1))/eg;
	return $value;
}
