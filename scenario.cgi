#!/usr/bin/perl -w
require "jcode.pl";
require './cgi-lib.pl';

$ENTRYFILE     = './dat/entry.dat';		# �Q���҃t�@�C��

&ReadParse();

	my ($error, @ext_ok,$ok,$path,$id,$script,@char,@DATA);
	$name   = $incfn{"upload_file"};
	@names = split(/\\/,$name);
	$name = $names[$#names];

		$script="";
		#��t�\�Ȋg���q�i���K�\���j
@ext_ok = qw (
txt
csv
);
	if (!defined($name)){
		print "�t�@�C�����]���ł��܂���ł����F$error\n";
		exit;
	}
	foreach (@ext_ok){
		if($name =~ /\.$_$/){
			$ok=1;
		}
	}
	if($ok != 1){
		$error = "������Ă��Ȃ��g���q�ł�".@ext_ok.$name;
		print "�t�@�C���]�����ł��܂���ł����B: $error\n";
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
<title>�S��RoopeR</title>
</head>
<title>�V�[�g</title></head>
<body>
<h1>$FORM{'�^�C�g��'}</h1>

<form action="./rooper.cgi" method="POST">
<table>
<tr><th>���[��Y</th><td>$FORM{'RuleY'}<input type="hidden" name="ruleY" value="$FORM{'RuleY'}"></td></tr>
<tr><th>���[��X1</th><td>$FORM{'RuleX1'}<input type="hidden" name="ruleX1" value="$FORM{'RuleX1'}"></td></tr>
<tr><th>���[��X2</th><td>$FORM{'RuleX2'}<input type="hidden" name="ruleX2" value="$FORM{'RuleX2'}"></td></tr>
<table>
<tr><th>�l��</th><th>��E</th></tr>
<tr><td>�j�q�w��</td><td>$FORM{'�j�q�w��'}<input type="hidden" name="shonen" value="$FORM{'�j�q�w��'}"></td></tr>
<tr><td>���q�w��</td><td>$FORM{'���q�w��'}<input type="hidden" name="shojo" value="$FORM{'���q�w��'}"></td></tr>
<tr><td>����l</td><td>$FORM{'����l'}<input type="hidden" name="ojo" value="$FORM{'����l'}"></td></tr>
<tr><td>�ޏ�</td><td>$FORM{'�ޏ�'}<input type="hidden" name="miko" value="$FORM{'�ޏ�'}"></td></tr>
<tr><td>�Y��</td><td>$FORM{'�Y��'}<input type="hidden" name="keiji" value="$FORM{'�Y��'}"></td></tr>
<tr><td>�T�����[�}��</td><td>$FORM{'�T�����[�}��'}<input type="hidden" name="salary" value="$FORM{'�T�����[�}��'}"></td></tr>
<tr><td>���</td><td>$FORM{'���'}<input type="hidden" name="joho" value="$FORM{'���'}"></td></tr>
<tr><td>���</td><td>$FORM{'���'}<input type="hidden" name="isha" value="$FORM{'���'}"></td></tr>
<tr><td>���@����</td><td>$FORM{'����'}<input type="hidden" name="kanja" value="$FORM{'����'}"></td></tr>
</table>
<table style="width:640px;">
<tr><th>����</th><th>����</th><th>��������</th><th>�Ɛl</th></tr>
END
$loop=($FORM{'���[�v����'}+0);
for($i=1;$i<=$loop;$i++){
	$tmpday = "����".$i;
	$tmphan = "�Ɛl".$i;
	$tmp    = "����".$i;
	$FORM{$tmpday} =~ s/\r//;
	$FORM{$tmpday} =~ s/\n//;
	if(!($FORM{$tmpday} eq "")){
		print qq|<tr><td>$i</td><td>$FORM{$tmpday}<input type="hidden" name="day$i" value="$FORM{$tmpday}"></td><td style='text-align:left;'>$FORM{$tmp}<input type="hidden" name="kouka$i" value="$FORM{$tmp}"></td><td>$FORM{$tmphan}<input type="hidden" name="han$i" value="$FORM{$tmphan}"></td></tr>|;
	}
}

print <<END;
</table>
<table>
<tr><th>���[�v��</th><td style="border-width:2px;"><strong>$FORM{'���[�v��'}</strong><input type="hidden" name="loop" value="$FORM{'���[�v��'}"></td><th>�P���[�v����</th><td style="border-width:2px;"><strong>$FORM{'���[�v����'}</strong><input type="hidden" name="loopday" value="$FORM{'���[�v����'}"></td></tr>
</table>
END
print "<table>";
print qq|<tr><th>�S���Z�b�g</th><td style="border-width:2px;">$FORM{'�S���Z�b�g'}<input type="hidden" name="set" value="$FORM{'�S���Z�b�g'}"></td></tr>|;
print "</table>";
print qq|<input type="hidden" name="map1" value="$FORM{'�g�p�}�b�v1'}"><input type="hidden" name="map2" value="$FORM{'�g�p�}�b�v2'}"><input type="hidden" name="map3" value="$FORM{'�g�p�}�b�v3'}"><input type="hidden" name="map4" value="$FORM{'�g�p�}�b�v4'}">|;
print "<table>";
print qq|<tr><th>�g�p�}�b�v</th><td>$FORM{'�g�p�}�b�v1'}</td><td>$FORM{'�g�p�}�b�v2'}</td><td>$FORM{'�g�p�}�b�v3'}</td><td>$FORM{'�g�p�}�b�v4'}</td></tr>|;
print "</table>";

$FORM{'���k'} =~ s/\r//; $FORM{'���k'} =~ s/\n//;
if(!($FORM{'���k'} eq "")){
	print qq|<input type="hidden" name="sodan" value="$FORM{'���k'}">|;
	print "<table>";
	print qq|<tr><th>���k</th><td>$FORM{'���k'}</td></tr>|;
	print "</table>";
}

$FORM{'���ʃ��[��'} =~ s/\r//;$FORM{'���ʃ��[��'} =~ s/\n//;
if(!($FORM{'���ʃ��[��'} eq "")){
	print "<table>";
	print "<tr><th>���ʃ��[��</th></tr>";
	print qq|<tr><td style="text-align:left;">$FORM{'���ʃ��[��'}<input type="hidden" name="text" value="$FORM{'���ʃ��[��'}"></td></tr>|;
	print "</table>";
}

$FORM{'�V�i���I�̓���'} =~ s/\r//; $FORM{'�V�i���I�̓���'} =~ s/\n//;
if(!($FORM{'�V�i���I�̓���'} eq "")){
	print qq|<input type="hidden" name="tokutyo" value="$FORM{'�V�i���I�̓���'}">|;
	$FORM{'�V�i���I�̓���'}=~ s|\\n|</p><p>|g;
	print "<table>";
	print qq|<tr><th>�V�i���I�̓���</th></tr><tr><td style="text-align:left;"><p>$FORM{'�V�i���I�̓���'}</p></td></tr>|;
	print "</table>";
}

$FORM{'�r�{�Ƃւ̎w�j'} =~ s/\r//; $FORM{'�r�{�Ƃւ̎w�j'} =~ s/\n//;
if(!($FORM{'�r�{�Ƃւ̎w�j'} eq "")){
	print qq|<input type="hidden" name="sisin" value="$FORM{'�r�{�Ƃւ̎w�j'}">|;
$FORM{'�r�{�Ƃւ̎w�j'}=~ s|\\n|</p><p>|g;
	print "<table>";
	print qq|<tr><th>�r�{�Ƃւ̎w�j</th></tr><tr><td style="text-align:left;"><p>$FORM{'�r�{�Ƃւ̎w�j'}</p></td></tr>|;
	print "</table>";
}
print qq|<table><tr><th colspan="2">�r�{�Ƃ̏�������</th></tr>|;
for($i=1;$i<=5;$i++){
	$tmp = "�r�{�Ƃ̏�������".$i;
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
if($FORM{'�S���Z�b�g'} eq "Basic Tragedy"){ $custom=0;}
elsif($FORM{'�S���Z�b�g'}  eq "Visual Novel(���j"){$custom=3;}

print <<END;
</table>
<input type="submit" value="�r�{����" style="font-size:200%">
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
if($FORM{'�S���Z�b�g'} eq "Basic Tragedy"){ $custom=0;$FORM{'custom'} =0;}
elsif($FORM{'�S���Z�b�g'}  eq "Visual Novel(���j"){$custom=3;$FORM{'custom'}=3; }

	my $entry = time;
	my $delflag = shift @_;
	my (@lines, @users, $i);
	my $noentry = 1;
	my $now = time;
	
	open(FILE, "<$ENTRYFILE")
		or printErrorPage("�Q���҃t�@�C�����J���܂���B");
	eval{ flock(FILE, 1) };
	@lines = <FILE>;
	close(FILE);
	
	for($i = 0 ; $i < @lines ; ) {
		my ($name, $entry, $update,$hero,$custom) = split(/:/, $lines[$i]);
		
		if($name eq $COOKIE{'name'} and $entry == $FORM{'entry'}) {
			$noentry = 0;
			if(not $delflag) {
				# �����̍ŏI�X�V���Ԃ��X�V
				$lines[$i] = "$name:$entry:$now:'writer':$custom\n";
			}
			else {
				# �������Q���҂���폜
				splice @lines, $i, 1;
				next;
			}
		}
		elsif($now - $update > $REPLYTIME) {
			# �ŏI�X�V���Ԃ���ő唽�����Ԉȏ�o�߂������[�U���폜
			splice @lines, $i, 1;
			next;
		}
		++$i;
#		push @users, $name;
		
		#2012.5.5�ǋL����
		$tmp="";
		if($hero eq "writer"){
			if($custom ==1){
				$tmp="(Original Tragedy)";
			}elsif($custom ==2){
				$tmp="(���Ń��[��)";
			}elsif($custom==3){
			    $tmp="(Visual Novel)";
			}
			else{
				$tmp="(Basic Tragedy)";
			}
		}
		#����
		push @users, qq|<span class="name$hero">$name</span>$tmp|;
	}
	if($noentry and $entry) {
		push @lines, "$COOKIE{'name'}:$FORM{'entry'}:$now:$FORM{'hero'}:$FORM{'custom'}\n";
#		push @users, $FORM{'name'};
		#2012.5.5�ǋL����
		$tmp="";
		if($FORM{'hero'} eq "writer"){
			if($FORM{'custom'} ==1){
				$tmp="(Original Tragedy)";
			}elsif($FORM{'custom'} ==2){
				$tmp="(���Ń��[��)";
			}elsif($FORM{'custom'} ==3){
			    $tmp="(Visual Novel)";
			}else{
				$tmp="(Basic Tragedy)";
			}
		}
		#����
		push @users, qq|<span class="namewriter">$COOKIE{'name'}</span>$tmp|;
	}
	
	open(FILE, ">$ENTRYFILE")
		or printErrorPage("�Q���҃t�@�C�����J���܂���");
	eval{ flock(FILE, 2) };
	print FILE @lines;
	close(FILE);
	
	return @users;
}
