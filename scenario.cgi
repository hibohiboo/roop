#!/usr/bin/perl -w
require "jcode.pl";
require './cgi-lib.pl';

$ENTRYFILE     = './dat/entry.dat';		# 参加者ファイル

&ReadParse();

	my ($error, @ext_ok,$ok,$path,$id,$script,@char,@DATA);
	$name   = $incfn{"upload_file"};
	@names = split(/\\/,$name);
	$name = $names[$#names];

		$script="";
		#受付可能な拡張子（正規表現）
@ext_ok = qw (
txt
csv
);
	if (!defined($name)){
		print "ファイルが転送できませんでした：$error\n";
		exit;
	}
	foreach (@ext_ok){
		if($name =~ /\.$_$/){
			$ok=1;
		}
	}
	if($ok != 1){
		$error = "許可されていない拡張子です".@ext_ok.$name;
		print "ファイル転送ができませんでした。: $error\n";
		exit;
	}
	foreach $pair (split(/\n/, $in{'upload_file'})) {
		my ($key, $value) = split(/=/, $pair);
		
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
		
		$value = jcode::sjis($value);
		$value =~ s/&/&amp;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ tr/\t/ /;
		chomp($value);
		$FORM{$key} = $value;
	}
	loadCookie();
	updateEntrants();
print "Content-type: text/html; charset=$CHARSET\n";
print "Pragma: no-cache\n";
print "Cache-Control: no-cache\n";
print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n";
print "\n";

	print <<END;
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
<link rel="stylesheet" type="text/css" href="./rooper.css">

<script language="JavaScript">
</script>
<title>惨劇RoopeR</title>
</head>
<title>シート</title></head>
<body>
<h1>$FORM{'タイトル'}</h1>

<form action="./rooper.cgi" method="POST">
<table>
<tr><th>ルールY</th><td>$FORM{'RuleY'}<input type="hidden" name="ruleY" value="$FORM{'RuleY'}"></td></tr>
<tr><th>ルールX1</th><td>$FORM{'RuleX1'}<input type="hidden" name="ruleX1" value="$FORM{'RuleX1'}"></td></tr>
<tr><th>ルールX2</th><td>$FORM{'RuleX2'}<input type="hidden" name="ruleX2" value="$FORM{'RuleX2'}"></td></tr>
<table>
<tr><th>人物</th><th>役職</th></tr>
<tr><td>男子学生</td><td>$FORM{'男子学生'}<input type="hidden" name="shonen" value="$FORM{'男子学生'}"></td></tr>
<tr><td>女子学生</td><td>$FORM{'女子学生'}<input type="hidden" name="shojo" value="$FORM{'女子学生'}"></td></tr>
<tr><td>お嬢様</td><td>$FORM{'お嬢様'}<input type="hidden" name="ojo" value="$FORM{'お嬢様'}"></td></tr>
<tr><td>巫女</td><td>$FORM{'巫女'}<input type="hidden" name="miko" value="$FORM{'巫女'}"></td></tr>
<tr><td>刑事</td><td>$FORM{'刑事'}<input type="hidden" name="keiji" value="$FORM{'刑事'}"></td></tr>
<tr><td>サラリーマン</td><td>$FORM{'サラリーマン'}<input type="hidden" name="salary" value="$FORM{'サラリーマン'}"></td></tr>
<tr><td>情報屋</td><td>$FORM{'情報屋'}<input type="hidden" name="joho" value="$FORM{'情報屋'}"></td></tr>
<tr><td>医者</td><td>$FORM{'医者'}<input type="hidden" name="isha" value="$FORM{'医者'}"></td></tr>
<tr><td>入院患者</td><td>$FORM{'患者'}<input type="hidden" name="kanja" value="$FORM{'患者'}"></td></tr>
</table>
<table style="width:640px;">
<tr><th>日数</th><th>事件</th><th>事件効果</th><th>犯人</th></tr>
END
$loop=($FORM{'ループ日数'}+0);
for($i=1;$i<=$loop;$i++){
	$tmpday = "日数".$i;
	$tmphan = "犯人".$i;
	$tmp    = "事件".$i;
	$FORM{$tmpday} =~ s/\r//;
	$FORM{$tmpday} =~ s/\n//;
	if(!($FORM{$tmpday} eq "")){
		print qq|<tr><td>$i</td><td>$FORM{$tmpday}<input type="hidden" name="day$i" value="$FORM{$tmpday}"></td><td style='text-align:left;'>$FORM{$tmp}<input type="hidden" name="kouka$i" value="$FORM{$tmp}"></td><td>$FORM{$tmphan}<input type="hidden" name="han$i" value="$FORM{$tmphan}"></td></tr>|;
	}
}

print <<END;
</table>
<table>
<tr><th>ループ回数</th><td style="border-width:2px;"><strong>$FORM{'ループ回数'}</strong><input type="hidden" name="loop" value="$FORM{'ループ回数'}"></td><th>１ループ日数</th><td style="border-width:2px;"><strong>$FORM{'ループ日数'}</strong><input type="hidden" name="loopday" value="$FORM{'ループ日数'}"></td></tr>
</table>
END
print "<table>";
print qq|<tr><th>惨劇セット</th><td style="border-width:2px;">$FORM{'惨劇セット'}<input type="hidden" name="set" value="$FORM{'惨劇セット'}"></td></tr>|;
print "</table>";
print qq|<input type="hidden" name="map1" value="$FORM{'使用マップ1'}"><input type="hidden" name="map2" value="$FORM{'使用マップ2'}"><input type="hidden" name="map3" value="$FORM{'使用マップ3'}"><input type="hidden" name="map4" value="$FORM{'使用マップ4'}">|;
print "<table>";
print qq|<tr><th>使用マップ</th><td>$FORM{'使用マップ1'}</td><td>$FORM{'使用マップ2'}</td><td>$FORM{'使用マップ3'}</td><td>$FORM{'使用マップ4'}</td></tr>|;
print "</table>";

$FORM{'相談'} =~ s/\r//; $FORM{'相談'} =~ s/\n//;
if(!($FORM{'相談'} eq "")){
	print qq|<input type="hidden" name="sodan" value="$FORM{'相談'}">|;
	print "<table>";
	print qq|<tr><th>相談</th><td>$FORM{'相談'}</td></tr>|;
	print "</table>";
}

$FORM{'特別ルール'} =~ s/\r//;$FORM{'特別ルール'} =~ s/\n//;
if(!($FORM{'特別ルール'} eq "")){
	print "<table>";
	print "<tr><th>特別ルール</th></tr>";
	print qq|<tr><td style="text-align:left;">$FORM{'特別ルール'}<input type="hidden" name="text" value="$FORM{'特別ルール'}"></td></tr>|;
	print "</table>";
}

$FORM{'シナリオの特徴'} =~ s/\r//; $FORM{'シナリオの特徴'} =~ s/\n//;
if(!($FORM{'シナリオの特徴'} eq "")){
	print qq|<input type="hidden" name="tokutyo" value="$FORM{'シナリオの特徴'}">|;
	$FORM{'シナリオの特徴'}=~ s|\\n|</p><p>|g;
	print "<table>";
	print qq|<tr><th>シナリオの特徴</th></tr><tr><td style="text-align:left;"><p>$FORM{'シナリオの特徴'}</p></td></tr>|;
	print "</table>";
}

$FORM{'脚本家への指針'} =~ s/\r//; $FORM{'脚本家への指針'} =~ s/\n//;
if(!($FORM{'脚本家への指針'} eq "")){
	print qq|<input type="hidden" name="sisin" value="$FORM{'脚本家への指針'}">|;
$FORM{'脚本家への指針'}=~ s|\\n|</p><p>|g;
	print "<table>";
	print qq|<tr><th>脚本家への指針</th></tr><tr><td style="text-align:left;"><p>$FORM{'脚本家への指針'}</p></td></tr>|;
	print "</table>";
}
print qq|<table><tr><th colspan="2">脚本家の勝利条件</th></tr>|;
for($i=1;$i<=5;$i++){
	$tmp = "脚本家の勝利条件".$i;
	$FORM{$tmp} =~ s/\r//;
	$FORM{$tmp} =~ s/\n//;
	my ($_1, $_2) = split(/:/, $FORM{$tmp});
	if(!($_1 eq "")){
		
		print qq|<tr><th rowspan="2">$i</th><th >$_1</th></tr>|;
		print qq|<tr><td>$_2|;
		print qq|<input type="hidden" name="joken$i" value="$_1:$_2">|;
		print "</td></tr>";
	}
}
if($FORM{'惨劇セット'} eq "Basic Tragedy"){ $custom=0;}
elsif($FORM{'惨劇セット'}  eq "Visual Novel(仮）"){$custom=3;}

print <<END;
</table>
<input type="submit" value="脚本決定" style="font-size:200%">
<input type="hidden" name="mode" value="enter2">
<input type="hidden" name="name" value="$COOKIE{'name'}">
<input type="hidden" name="entry" value="$entry">
<input type="hidden" name="hero" value="writer">
<input type="hidden" name="custom" value="$custom">
</form>
</body>
</html>

END
exit;


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

sub updateEntrants
{
if($FORM{'惨劇セット'} eq "Basic Tragedy"){ $custom=0;$FORM{'custom'} =0;}
elsif($FORM{'惨劇セット'}  eq "Visual Novel(仮）"){$custom=3;$FORM{'custom'}=3; }

	my $entry = time;
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
		
		if($name eq $COOKIE{'name'} and $entry == $FORM{'entry'}) {
			$noentry = 0;
			if(not $delflag) {
				# 自分の最終更新時間を更新
				$lines[$i] = "$name:$entry:$now:'writer':$custom\n";
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
		
		#2012.5.5追記→→
		$tmp="";
		if($hero eq "writer"){
			if($custom ==1){
				$tmp="(Original Tragedy)";
			}elsif($custom ==2){
				$tmp="(α版ルール)";
			}elsif($custom==3){
			    $tmp="(Visual Novel)";
			}
			else{
				$tmp="(Basic Tragedy)";
			}
		}
		#←←
		push @users, qq|<span class="name$hero">$name</span>$tmp|;
	}
	if($noentry and $entry) {
		push @lines, "$COOKIE{'name'}:$FORM{'entry'}:$now:$FORM{'hero'}:$FORM{'custom'}\n";
#		push @users, $FORM{'name'};
		#2012.5.5追記→→
		$tmp="";
		if($FORM{'hero'} eq "writer"){
			if($FORM{'custom'} ==1){
				$tmp="(Original Tragedy)";
			}elsif($FORM{'custom'} ==2){
				$tmp="(α版ルール)";
			}elsif($FORM{'custom'} ==3){
			    $tmp="(Visual Novel)";
			}else{
				$tmp="(Basic Tragedy)";
			}
		}
		#←←
		push @users, qq|<span class="namewriter">$COOKIE{'name'}</span>$tmp|;
	}
	
	open(FILE, ">$ENTRYFILE")
		or printErrorPage("参加者ファイルが開けません");
	eval{ flock(FILE, 2) };
	print FILE @lines;
	close(FILE);
	
	return @users;
}
