#!/usr/bin/perl -w
require "jcode.pl";

use CGI;
use File::Copy;
use File::Basename;

#変数宣言
my ($error, @ext_ok,$ok,$path,$id,$script,@char,@DATA);



#転送できるファイルの最大サイズを設定
#（実際は、post送信されるコンテンツ合計の最大サイズ）
#この値は、CGIオブジェクトを作成する時には既に
#設定されていなければならない
$CGI::POST_MAX = 1024 * 20; #max = 20kB

#エラーメッセージ表示用
print "Content-Type: text/html;charset=euc-jp\r\n\r\n";

my $q = new CGI;

my $fname = basename($q->param('filename'));

if($q->param('filetype') eq "text"){
	$path = "./custom";
	$script="";
#受付可能な拡張子（正規表現）
@ext_ok = qw (
txt
csv
);
}elsif($q->param('filetype') eq 'img'){
	my ($sec, $min, $hour, $mday, $mon, $year, $wday)
		= localtime(time);
	my $date = sprintf("%02d/%02d%02d:%02d",++$mon,$mday,$hour,$min);
	$path = "./custom/img/character";
	$fname =~ /(.*)\.png$/;
	$id=$1;
	if($id =~ m/(hero|write)/){
		$path = "./custom/img/hand";
	}elsif($id =~ m/char/){
		$path = "./custom/img/character";
	}
	$script= qq|window.opener.document.getElementById("custom$id").src="$path/$fname?$date";|; 
	#受付可能な拡張子（正規表現）
	@ext_ok = qw (png);
}
my $newfile = "$path/$fname";

my $fh = $q->upload('upload_file');
if (!defined($fh) and $error = $q->cgi_error){
print "ファイルが転送できませんでした：$error\n";
exit;
}


foreach (@ext_ok){
	if($fh =~ /\.$_$/){
		$ok=1;
	}
}
if($ok != 1){
	$error = "許可されていない拡張子です".$q->param('filetype').@ext_ok;
	print "ファイル転送ができませんでした。: $error\n";
	exit;
}



copy ($fh, "$newfile");
undef $q;
if($fname eq "char.csv" || $fname eq "rule.csv"){
	$script=$script.qq|loadData("$fname");|;
}


print "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EM\"   \"http://www.w3.org/TR/html4/loose.dtd\"><html LANG=\"ja-JP\"><head><meta http-equi\"Content-Type\" content=\"text/html\;charset=EUC-JP\"><meta http-equiv=\"Content-Script-Type\" content=\"text/javascript\"><meta http-equiv=\"Content-Style-Type\" content=\"text/css\"><link rel=\"stylesheet\" type=\"text/css\" href=\"rooper.css\"><script type=\"text/javascript\" charset=\"UTF-8\" language=\"JavaScript\" src=\"js/jquery.js\"></script><script type=\"text/javascript\" charset=\"UTF-8\" language=\"JavaScript\" src=\"js/custom.js\"></script><title>オリジナルセット</title></head><body style=\"overflow-x:hidden\">";
print qq|<script language=\"JavaScript\">window.onload=function(){|;
print qq|var timerID1 = setTimeout(function(){$script},500);|;
print qq|var timerID = setTimeout(function(){window.close();},1000);}</script>|;
print "ファイルをアップロードしました<br>1秒後に閉じます\n\n";

print "</body></html>";
