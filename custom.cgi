#!/usr/bin/perl -w
require "jcode.pl";

use CGI;
use File::Copy;
use File::Basename;

#�ѿ����
my ($error, @ext_ok,$ok,$path,$id,$script,@char,@DATA);



#ž���Ǥ���ե�����κ��祵����������
#�ʼºݤϡ�post��������륳��ƥ�Ĺ�פκ��祵������
#�����ͤϡ�CGI���֥������Ȥ����������ˤϴ���
#���ꤵ��Ƥ��ʤ���Фʤ�ʤ�
$CGI::POST_MAX = 1024 * 20; #max = 20kB

#���顼��å�����ɽ����
print "Content-Type: text/html;charset=euc-jp\r\n\r\n";

my $q = new CGI;

my $fname = basename($q->param('filename'));

if($q->param('filetype') eq "text"){
	$path = "./custom";
	$script="";
#���ղ�ǽ�ʳ�ĥ�ҡ�����ɽ����
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
	#���ղ�ǽ�ʳ�ĥ�ҡ�����ɽ����
	@ext_ok = qw (png);
}
my $newfile = "$path/$fname";

my $fh = $q->upload('upload_file');
if (!defined($fh) and $error = $q->cgi_error){
print "�ե����뤬ž���Ǥ��ޤ���Ǥ�����$error\n";
exit;
}


foreach (@ext_ok){
	if($fh =~ /\.$_$/){
		$ok=1;
	}
}
if($ok != 1){
	$error = "���Ĥ���Ƥ��ʤ���ĥ�ҤǤ�".$q->param('filetype').@ext_ok;
	print "�ե�����ž�����Ǥ��ޤ���Ǥ�����: $error\n";
	exit;
}



copy ($fh, "$newfile");
undef $q;
if($fname eq "char.csv" || $fname eq "rule.csv"){
	$script=$script.qq|loadData("$fname");|;
}


print "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EM\"   \"http://www.w3.org/TR/html4/loose.dtd\"><html LANG=\"ja-JP\"><head><meta http-equi\"Content-Type\" content=\"text/html\;charset=EUC-JP\"><meta http-equiv=\"Content-Script-Type\" content=\"text/javascript\"><meta http-equiv=\"Content-Style-Type\" content=\"text/css\"><link rel=\"stylesheet\" type=\"text/css\" href=\"rooper.css\"><script type=\"text/javascript\" charset=\"UTF-8\" language=\"JavaScript\" src=\"js/jquery.js\"></script><script type=\"text/javascript\" charset=\"UTF-8\" language=\"JavaScript\" src=\"js/custom.js\"></script><title>���ꥸ�ʥ륻�å�</title></head><body style=\"overflow-x:hidden\">";
print qq|<script language=\"JavaScript\">window.onload=function(){|;
print qq|var timerID1 = setTimeout(function(){$script},500);|;
print qq|var timerID = setTimeout(function(){window.close();},1000);}</script>|;
print "�ե�����򥢥åץ��ɤ��ޤ���<br>1�ø���Ĥ��ޤ�\n\n";

print "</body></html>";
