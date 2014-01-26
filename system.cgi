#!/usr/bin/perl --

require "../rooper/jcode.pl";


$CHARSET       = 'Shift_JIS';		# �����R�[�h
$CHATFILE      = './dat/chat.dat';		# �������O�t�@�C��
$LOGFILE      = './dat/log.dat';		# �������O�t�@�C��
$CHARFILE = './dat/char.dat';
$MAXLINE       = 30;			# �ő働�O�s��
my @char;
#�t�H�[���f�[�^�̎擾
loadFormdata();
loadChatfile();
if($FORM{'custom'} ==1){
	open(FILE, "<$CHARFILE")
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 1) };
	@data = <FILE>;
	close(FILE);
	foreach $ln (@data) {
		chomp $ln;
		push(@char,$ln)
	}
}elsif($FORM{'custom'} ==2){
	@char=("�j�q�w��","���q�w��","����l","�ޏ�","�Y��","�T�����[�}��","���","���","����","�_��","�w�Z","�a�@","�s�s");
}elsif($FORM{'custom'} ==4){
	@char=("�j�q�w��","���q�w��","����l","�ޏ�","�Y��","�T�����[�}��","���","���","����","���b�`","���b�a","���b�b","�a�@","�s�s","�_��","�w�Z");
}elsif($FORM{'custom'} ==9){
	@char=("�j�q�w��","���q�w��","����l","�ޏ�","�Y��","�T�����[�}��","���","���","����","�ψ���","�C���M�����[","�ِ��E�l","�_�i","�A�C�h��","�}�X�R�~","�啨","�i�[�X","���","�w��","���z","���b�`","���b�a","���b�b","�a�@","�s�s","�_��","�w�Z");
}elsif($FORM{'custom'} >=6){
	@char=("�j�q�w��","���q�w��","����l","�ޏ�","�Y��","�T�����[�}��","���","���","����","�ψ���","�C���M�����[","�ِ��E�l","�_�i","�A�C�h��","�}�X�R�~","�啨","�i�[�X","���","�w��","���z","�a�@","�s�s","�_��","�w�Z");
}else{
	@char=("�j�q�w��","���q�w��","����l","�ޏ�","�Y��","�T�����[�}��","���","���","����","�a�@","�s�s","�_��","�w�Z");
}
if($FORM{'custom'} ==2){
	@plhand=("�Ö�֎~","�F�D�{�Q","�ړ��֎~","�s���|�P","�ړ�����","�ړ�����","�F�D�{�P","�s���{�P","�s���|�P","�g��B");
}else{
	@plhand=("�Ö�֎~","�F�D�{�Q","�ړ��֎~","�s���|�P","�ړ�����","�ړ�����","�F�D�{�P","�s���{�P","�g��A","�g��B");
}
@gmhand=("�ړ��΂�","�Ö�{�Q","�ړ�����","�ړ�����","�s���{�P","�s���{�P","�s���|�P","�Ö�{�P","�F�D�֎~","�s���֎~","�g��A","�g��B");

if($FORM{'mode'} eq 'phase6') {
	#�r�{�ƃt�F�C�Y
	$text="�r�{�Ƃ��y$char[$FORM{'char3'}]�z�Ɓy$char[$FORM{'char4'}]�z�Ɓy$char[$FORM{'char5'}]�z�Ɏ�D���Z�b�g���܂����B";
	if($FORM{'leaderskip'}){$text=$text."<br><span class='namewriter'>���[�_�[�̍s�����X�L�b�v���܂��B</span>";}
	$logtext=$text;
}elsif($FORM{'mode'} eq 'phase7') {
	$text="��l�����y$char[$FORM{'char'}]�z�Ɏ�D���Z�b�g���܂����B";
	$logtext=$text;
}elsif($FORM{'mode'} eq 'phase8') {
	$text="��l�����y$char[$FORM{'char'}]�z�Ɏ�D���Z�b�g���܂����B";
	$logtext=$text;
}elsif($FORM{'mode'} eq 'phase9') {
	if($FORM{'char0'} eq '-1'){
		$text="��D�����J���܂����B<span class='name0'>���[�_�[�͍s���J�[�h�Z�b�g�֎~</span>�A<span class='name1'>�y$char[$FORM{'char1'}]�z�Ɂh$plhand[$FORM{'hand1'}]�h</span>�A<span class='name2'>�y$char[$FORM{'char2'}]�z�Ɂh$plhand[$FORM{'hand2'}]�h</span>�A<span class='namewriter'>�y$char[$FORM{'char3'}]�z�Ɂh$gmhand[$FORM{'hand3'}]�h</span>�A�y$char[$FORM{'char4'}]�z�Ɂh$gmhand[$FORM{'hand4'}]�h�A<span class='namewriter'>�y$char[$FORM{'char5'}]�z�Ɂh$gmhand[$FORM{'hand5'}]�h</span>�A���Z�b�g����Ă��܂��B";
		$logtext="��D�����J���܂����B���[�_�[�͍s���J�[�h�Z�b�g�֎~�B�y$char[$FORM{'char1'}]�z�Ɂh$plhand[$FORM{'hand1'}]�h�A�y$char[$FORM{'char2'}]�z�Ɂh$plhand[$FORM{'hand2'}]�h�A�y$char[$FORM{'char3'}]�z�Ɂh$gmhand[$FORM{'hand3'}]�h�A�y$char[$FORM{'char4'}]�z�Ɂh$gmhand[$FORM{'hand4'}]�h�A�y$char[$FORM{'char5'}]�z�Ɂh$gmhand[$FORM{'hand5'}]�h�A���Z�b�g����Ă��܂��B";
	}elsif($FORM{'char1'} eq '-1'){
		$text="��D�����J���܂����B<span class='name0'>�y$char[$FORM{'char0'}]�z�Ɂh$plhand[$FORM{'hand0'}]�h</span>�A<span class='name1'>���[�_�[�͍s���J�[�h�Z�b�g�֎~</span>�A<span class='name2'>�y$char[$FORM{'char2'}]�z�Ɂh$plhand[$FORM{'hand2'}]�h</span>�A<span class='namewriter'>�y$char[$FORM{'char3'}]�z�Ɂh$gmhand[$FORM{'hand3'}]�h</span>�A�y$char[$FORM{'char4'}]�z�Ɂh$gmhand[$FORM{'hand4'}]�h�A<span class='namewriter'>�y$char[$FORM{'char5'}]�z�Ɂh$gmhand[$FORM{'hand5'}]�h</span>�A���Z�b�g����Ă��܂��B";
		$logtext="��D�����J���܂����B�y$char[$FORM{'char0'}]�z�Ɂh$plhand[$FORM{'hand0'}]�h�A���[�_�[�͍s���J�[�h�Z�b�g�֎~�A�y$char[$FORM{'char2'}]�z�Ɂh$plhand[$FORM{'hand2'}]�h�A�y$char[$FORM{'char3'}]�z�Ɂh$gmhand[$FORM{'hand3'}]�h�A�y$char[$FORM{'char4'}]�z�Ɂh$gmhand[$FORM{'hand4'}]�h�A�y$char[$FORM{'char5'}]�z�Ɂh$gmhand[$FORM{'hand5'}]�h�A���Z�b�g����Ă��܂��B";

	}elsif($FORM{'char2'} eq '-1'){
		$text="��D�����J���܂����B<span class='name0'>�y$char[$FORM{'char0'}]�z�Ɂh$plhand[$FORM{'hand0'}]�h</span>�A<span class='name1'>�y$char[$FORM{'char1'}]�z�Ɂh$plhand[$FORM{'hand1'}]�h</span>�A<span class='name2'>���[�_�[�͍s���J�[�h�Z�b�g�֎~</span>�A<span class='namewriter'>�y$char[$FORM{'char3'}]�z�Ɂh$gmhand[$FORM{'hand3'}]�h</span>�A�y$char[$FORM{'char4'}]�z�Ɂh$gmhand[$FORM{'hand4'}]�h�A<span class='namewriter'>�y$char[$FORM{'char5'}]�z�Ɂh$gmhand[$FORM{'hand5'}]�h</span>�A���Z�b�g����Ă��܂��B";
		$logtext="��D�����J���܂����B�y$char[$FORM{'char0'}]�z�Ɂh$plhand[$FORM{'hand0'}]�h�A�y$char[$FORM{'char1'}]�z�Ɂh$plhand[$FORM{'hand1'}]�h�A���[�_�[�͍s���J�[�h�Z�b�g�֎~�A�y$char[$FORM{'char3'}]�z�Ɂh$gmhand[$FORM{'hand3'}]�h�A�y$char[$FORM{'char4'}]�z�Ɂh$gmhand[$FORM{'hand4'}]�h�A�y$char[$FORM{'char5'}]�z�Ɂh$gmhand[$FORM{'hand5'}]�h�A���Z�b�g����Ă��܂��B";

	}else{
		$text="��D�����J���܂����B<span class='name0'>�y$char[$FORM{'char0'}]�z�Ɂh$plhand[$FORM{'hand0'}]�h</span>�A<span class='name1'>�y$char[$FORM{'char1'}]�z�Ɂh$plhand[$FORM{'hand1'}]�h</span>�A<span class='name2'>�y$char[$FORM{'char2'}]�z�Ɂh$plhand[$FORM{'hand2'}]�h</span>�A<span class='namewriter'>�y$char[$FORM{'char3'}]�z�Ɂh$gmhand[$FORM{'hand3'}]�h</span>�A�y$char[$FORM{'char4'}]�z�Ɂh$gmhand[$FORM{'hand4'}]�h�A<span class='namewriter'>�y$char[$FORM{'char5'}]�z�Ɂh$gmhand[$FORM{'hand5'}]�h</span>�A���Z�b�g����Ă��܂��B";
		$logtext="��D�����J���܂����B�y$char[$FORM{'char0'}]�z�Ɂh$plhand[$FORM{'hand0'}]�h�A�y$char[$FORM{'char1'}]�z�Ɂh$plhand[$FORM{'hand1'}]�h�A�y$char[$FORM{'char2'}]�z�Ɂh$plhand[$FORM{'hand2'}]�h�A�y$char[$FORM{'char3'}]�z�Ɂh$gmhand[$FORM{'hand3'}]�h�A�y$char[$FORM{'char4'}]�z�Ɂh$gmhand[$FORM{'hand4'}]�h�A�y$char[$FORM{'char5'}]�z�Ɂh$gmhand[$FORM{'hand5'}]�h�A���Z�b�g����Ă��܂��B";
	}
}elsif($FORM{'mode'} eq 'phase5') {#2013.06.20.add
	$text="��$FORM{'loop'}���[�v�A$FORM{'day'}���ڂ��J�n���܂��B";
	$logtext=$text;
}elsif($FORM{'mode'} eq 'loopend') {#2013.06.20.add
	$text="��$FORM{'loop'}���[�v���I�����܂��B";
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


#======================== �G���[�y�[�W�o�� ====
sub printErrorPage
{
	print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="rooper.css">
<title>�������</title></head>
<body><h1>�G���[</h1><p>$_[0]</p></body>
</html>
END
	
	exit;
}

#========================== ���O��ǂݍ��� ====
sub loadChatfile
{
	open(FILE, "<$CHATFILE")
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 1) };
	@DATA = <FILE>;
	close(FILE);
	open(FILE, "<$LOGFILE")
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 1) };
	@LOG = <FILE>;
	close(FILE);
}


#========================== �������������� ====
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
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 2) };
	print FILE @DATA;
	close(FILE);
	open(FILE, ">$LOGFILE")
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 2) };
	print FILE @LOG;
	close(FILE);
}

#================== �t�H�[���f�[�^��荞�� ====
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
#=========================== URL�G���R�[�h ====
sub urlencode
{
	my $value = shift @_;
	
	$value =~ tr/ /+/;
	$value =~ s/(\W)/sprintf("%%%02X", ord($1))/eg;
	return $value;
}
