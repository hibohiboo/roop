#!/usr/bin/perl --
require "../rooper/jcode.pl";
require '../rooper/cgi-lib.pl';

#perl5.8�œ���B
#perl5.16�œ��삵�Ȃ��B

#============================ ���[�U�[�ݒ� ====
$CHARSET       = 'Shift_JIS';		# �����R�[�h
$ENTRYFILE     = './dat/entry.dat';		# �Q���҃t�@�C��
$CHATFILE      = './dat/chat.dat';		# �������O�t�@�C��
$LOGFILE      = './dat/log.dat';		# �������O�t�@�C��
$BOARDFILE    = './dat/board.dat';
$SAVEFILE = './dat/save.dat';
$CHARFILE = './dat/char.dat';
$KAICHARFILE = './dat/kaichar.dat';#2013.5.18.add
$SCENARIOFILE = './dat/scenario/scenario.dat';   # �r�{�ۑ��t�@�C��
$OPENSHEET = './scenario/open.htm';   # ���J�V�[�g�ۑ��t�@�C��
$CLOSESHEET = './scenario/close.htm'; #����J�V�[�g�ۑ��t�@�C��
$REFRESH       = 30;			# �����[�h���ԁi�b�j
$REPLYTIME     = 60;			# �ő剞�����ԁi�b�j
$MAXLINE       = 30;			# �ő働�O�s��
$COOKIE_PREFIX = 'simplechat';		# �N�b�L�[�v���t�B�N�X
$COOKIE_LIFE   = 10;			# �N�b�L�[�����i���j

$JSPATH=".";
$CSSPATH=".";

$CHARIMGPATH="../rooper/first/img/character";
#======================== ���C���v���O���� ====
loadFormdata();
loadCookie();

if($FORM{'frame'} eq 'input') {
	# ���̓t���[��
	printInputFrame();
}
elsif($FORM{'frame'} eq 'view') {
	# �\���t���[��
	loadChatfile();
	if($FORM{'mode'} eq 'write') {
		writeRemark($FORM{'name'}, $FORM{'email'}, $FORM{'text'},$FORM{'hero'});
	}
	printViewFrame();
}
elsif($FORM{'frame'} eq 'hero') {
	# HERO�t���[��
	HeroFrame();
}
elsif($FORM{'frame'} eq 'writer') {
	# �r�{�ƃt���[��
	WriterFrame($FORM{'custom'});
}
else {
	# �t���[���Z�b�g
	#�r�{�Ɖ��------------------------------------------------------------------
	if($FORM{'mode'} eq 'enter2') {
		
		if($FORM{'name'} eq '') {
			printErrorPage("���O�͕K���L�����Ă��������B");
		}
		$COOKIE{'name'}  = $FORM{'name'};
		printFramePage2();
		writeScenario();
	}
	#�r�{���̓p�X���------------------------------------------------------------------
	if($FORM{'mode'} eq 'enter3') {
		
		if($FORM{'name'} eq '') {
			printErrorPage("���O�͕K���L�����Ă��������B");
		}
		$COOKIE{'name'}  = $FORM{'name'};
		printFramePage2();
	}
#------------------------------------------------------------------
	elsif($FORM{'mode'} eq 'hero') {
		if($FORM{'name'} eq '') {
			printErrorPage("���O�͕K���L�����Ă��������B");
		}
		$COOKIE{'name'}  = $FORM{'name'};
		printFramePageHERO();
	}
#�V�i���I��------------------------------------------------------------------
	elsif($FORM{'mode'} eq 'scenario') {
		if($FORM{'name'} eq '') {
			printErrorPage("���O�͕K���L�����Ă��������B");
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
#------------------------------�r�{�ǂݍ���------------------------------------
	elsif($FORM{'mode'} eq 'loadscenario') {
		#resetSave();
		loadScenario();
	}
#--------------------------------------------------------------------
	elsif($FORM{'mode'} eq 'enter') {
		if($FORM{'name'} eq '') {
			printErrorPage("���O�͕K���L�����Ă��������B");
		}
		loadChatfile();
		writeRemark("[INFO]", "",
			"�w$FORM{'name'}�x���񂪎Q������܂��B",$FORM{'hero'});
		updateEntrants();
		$COOKIE{'name'}  = $FORM{'name'};
		printFramePage();
	}
#====================================================================
	elsif($FORM{'mode'} eq 'exit') {
		loadChatfile();
		writeRemark("[INFO]", "",
			"�w$FORM{'name'}�x����͑ޏo����܂����B",$FORM{'hero'});
		updateEntrants(1);
		print "Location: $ENV{'SCRIPT_NAME'}\n\n";
	}
	else {
		printEntryPage();
	}
}
exit;


#==================== �G���g���[�y�[�W�o�� ====
sub printEntryPage
{
	loadBoardfile();
	if($FORM{'board'} eq 'write') {writeBoard($FORM{'text'});}

# ��d���e��}������
if ($FORM{'text'} ne "") {
    print "Location: http://$ENV{'HTTP_HOST'}$ENV{'SCRIPT_NAME'}\n\n";
    exit(0);
}
	
	my $entry = time;
	my @users = updateEntrants();
	my $entrants;
	
	if(@users > 0) {
		$entrants = "<ul class='float'><li>�E"
			. join('</li><li>�E', @users) . "</li></ul>";
	}
	
	printHttpHeader();

$tag_select = <<END_OF_DATA;
<select name="custom">
<option value="0">Basic Tragedy</option>
<option value="1">Original Tragedy</option>
<option value="2">���Ń��[��</option>
<option value="3">Visual Novel�i���j</option>
<option value="4">Haunted Stage</option>
<option value="5">Mystery Circle</option>
<option value="6">First Steps</option>
<option value="7" selected>Basic Tragedy ��</option>
<option value="8">Mystery Circle ��</option>
<option value="9">Haunted Stage ��</option>
<option value="10">Another Horizon</option>
</select>
END_OF_DATA

	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><title>�S��RoopeR�I�����C��Tool</title>
<meta name="description" content="BakaFire�l����̓��l�{�[�h�Q�[���S��RoopeR���u���E�U��ŗV��CGI�c�[���ł��B�N�ł��C�y�Ɏg�p�ł��܂��B���̃T�C�g�͎S���R�����Y���g�p���Ă��܂��B">
<meta name="keywords" content="�S��RoopeR,�S�����[�p�[,�I�����C���Z�b�V����,�c�[��,�x��">
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
<h1 class="namewriter">�I�����C���S���c�[��</h1>
<div id="inroom" style="position:relative; padding:5px;	margin:10px;">
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="namewriter"> �r�{��</span>�F<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="�Q������">
<!--#2013.11.07.up-->
$tag_select

<input type="checkbox" id="scenarioskip" onclick="skipmakescenario()">�r�{���͉�ʂ��΂��B
<br>

<input type="hidden" id="mode" name="mode" value="scenario">
<input type="hidden" name="entry" value="$entry">
<input type="hidden" name="hero" value="writer">
</form>
<hr>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="name0">��l��1</span>�F<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="�Q������">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="0">
<input type="hidden" name="entry" value="$entry">
</form>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="name1">��l��2</span>�F<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="�Q������">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="1">
<input type="hidden" name="entry" value="$entry">
</form>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="name2">��l��3</span>�F<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="�Q������">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="2">
<input type="hidden" name="entry" value="$entry">
</form>
<hr>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<span class="name4">��l��1��1�p</span>�F<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="�Q������">
<!--#2013.11.07.up-->
$tag_select
<br>
<input type="hidden" name="mode" value="hero">
<input type="hidden" name="hero" value="4">
<input type="hidden" name="entry" value="$entry">
</form>
<hr>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
���w�p�F<input type="text"
	name="name" size="40" value="$COOKIE{'name'}">
<input type="submit" value="�Q������">
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
<strong>���݂̎Q����</strong>�i�����X�V����܂���)
$entrants
</div>
<hr style="clear:both;position:relative;top:2em;">
<ul style="position:relative;top:2em;margin:2px;">
<li>�S��RoopeR�iBakaFire Party�l����)���I�����C���ŗV�ԃc�[���ł��B</li>
<li>�g�����������ł��܂����BAH�Ή��łł��B��<a href='http://www.nicovideo.jp/watch/sm22350352'>�j�R�j�R����</a>�B</li>
<li><a href="../rooper6/rooper.cgi">ANOTHR HORIZON�E�w�ҁE���z�Ή��e�X�g���[��</a></li>
<li><font color="red">new:</font>�T���v���V�i���I�@\�\\��\��\���B���Ȃ��̋r�{���ǉ������Ă��������I��<a href="http://rooper.1616bbs.com/bbs/" target='_blank'>�r�{�u����</a></li>
<li>�e��S���Z�b�g�ǉ��I �e�X�g���ł��B�o�O���������ꍇ�A��s�f���̂ق��ɕ񍐂�낵�����肢���܂��B</li>
<li><strong>
<a href="http://asuwa.island.ac/rooper/readme/readme.htm">��ʂ̌���</a>�B�@�@<a href="http://asuwa.island.ac/rooper/readme/guide.htm">�Q�[���̐i�ߕ�</a>�B�@�@<a href="http://asuwa.island.ac/rooper/readme/readme_faq.htm">FAQ</a>�B�@�@<a href="http://asuwa.island.ac/rooper/readme/readme_new_2.htm">�r�{�f�[�^�B</a>
</strong></li>
<li><a href="http://asuwa.island.ac/rooper/readme/readme_add.htm#iincho">�ψ����ɂ���D�������</a>�B</li>

<li>�����炪�g�p���̎��ɂǂ����B<a href="../rooper7/rooper.cgi">AH�Ή�\�\\������1</a>�B<a href="../rooper8/rooper.cgi">AH�Ή�\�\\������2</a></li>
<li><a href="http://asuwa.mistysky.net/rooper/original.html">�I���W�i���g���Z�b�g�FVisual Novel</a>��ǉ��B�e�X�g���ł��B�F�D�J�E���^�[�𒆐S�ɐ������Z�b�g�B���ӌ���W���B</li>
<li><a href="http://asuwa.island.ac/rooper/oldfasion.csv">Original Tragedy�f�[�^�t�@�C���FOld Fasion</a>�BOldFasion��yukikaze�l����̔�����S���Z�b�g�ł��B��<a href="http://yukikaze.otaden.jp/e242281.html">link�F�k�ցB�̍�����</a></li>
<li>���݃��łł��B\�\\���Ȃ����e�̕ύX�E�폜���s���ꍇ������܂��B</li>
<li>���܂����삵�Ȃ��Ƃ��͈�U�ޏo���A�L���b�V���̍폜���s���Ă݂Ă��������B���̌�A�ēx�������Ă��������B</li>
<li><a href="http://bakafire.main.jp/rooper/sr_top.htm">�S��RoopeR�{�ƃT�C�g</a></li>
<li>**<a href="http://dengekionline.com/elem/000/000/688/688677/">�d���I�����C���œ��W�I</a> �K���I ����҂Ƃ̑ΐ탊�v���C�B**  **<a href="http://www.4gamer.net/games/199/G019961/20130111001/">4Gamer.net�ŎS��RoopeR�̏Љ�I</a> �Z�����v���C�t���̕�����₷������B**</li>
<li><a href="https://docs.google.com/leaf?id=0BzGm1Adi28XLQ3gyZm1qdlJTdFdHMXEzeURZNFVudw">�Ђ��肳��̌��J�E����J�V�[�gDL</a>�B<a href="http://chaos.sakuraweb.com/sc/bg/boardgame_sum.html">���X�{�q�u����̃T�}���[</a></li>
<li><a href="http://www.dodontof.com/">�ǂǂ�Ƃ�</a>��<a href="http://www.dodontof.com/index.php?option=com_content&view=article&id=246&Itemid=126#scenarioData">�S��RoopeR�p�V�i���I�f�[�^</a>���J�I ��<font color="red">new:</font><a href="http://opengameseeker.com/archives/5952">�S���Љ�ǂǂ�Ƃӓ����@</a></li>
<li>���[��X�A���[��Y�A��E�A�����͎�l���̏�9�`13�ł��̓]�ڂƂȂ�܂��B�@�@����J�V�[�g�E���J�V�[�g�͎�l���̏��Q�Q�E�Q�R���Q�l�Ƃ��Ă��܂��B  ��D���X�g�͎�l���̏��P�W�E�P�X�ł��Q�Ƃł��BMystery Circle�͂R�`�X��,HauntedStage�͂S�`�X�ł���̓]�ڂƂȂ�܂��BFirstSteps�͎S��RoopeR�Ԏ�l���̏��R�P�`�R�R�ŁABasicTragedy�Ԃ͂R�S�`�R�W�ł���̓]�ڂƂȂ�܂��B</li>
<li>�S���R�����Y�A�S���R�����Y�ԍ쐬:BakaFire�l�A���m��l�B�J�[�h�C���X�g�F����B<a href="http://kage-design.com/wp/">�V���G�b�g�f�U�C��</a>�B</li>
<li>����m�F��firefox26.0�ōs�Ȃ��Ă��܂��B\C\hr\ome\��\���������悤�ł��B</li>
<li><font color="red">Internet Explorer�ł͓��삵�Ȃ����Ƃ�����܂�</font>�B�����Ȃ��Ƃ��́A���萔�ł���<a href='http://www.google.co.jp/chrome/intl/ja/landing.html'>chrome</a>��<a href='http://mozilla.jp/firefox/'>firefox</a>��DL���Ă��������B</li>
<li><a href="./dat/log.dat">���O�t�@�C���B</a>�s����ɏ��������܂��B</li>
<li><a href="http://asuwa.island.ac/calendar/calendar.php">�S���p�J�����_�[</a>�쐬���܂����B��낵����΂����p���������B</a></li>
</ul>

<hr style="position:relative;top:2em;">
<form action="$ENV{'SCRIPT_NAME'}" method="POST" name="lineboard" style="position:relative;top:2em;">
�@��s�f����
<input type="text" name="text" size="60">
<input type="submit" value="��������"><br>
�@�����̗\\��Ȃǂɂ��g�����������B�o�O�񍐂�v�]��������ɁB
	<input type="hidden" name="board" value="write">
</form>
<hr style="position:relative;top:2em;">
<div style="position:relative;top:2em;">
END
	foreach $ln (@BOARD) {
		chomp $ln;
		my ($date,$text) = split(/\t/, $ln);
		
		print "<p>";
		print "��$text($date)";
		print "</p>\n<hr>\n";
	}
print <<END;
</div>
<div class="footer">
���X�N���v�g���g�p����ɓ������ĕs��������Ă��ӂ𕉂����˂܂��B<br>
Copyright &copy; 2012-hibo
<br><a href="../index.htm">SITE-TOP</a>
	</div>
</div>
</body>
</html>
END
}
#====================== �t���[���Z�b�g�o��new ====
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
<p>�t���[�����T�|�[�g����Web�u���E�U�����g�����������B</p>
</noframes>
</frameset>
</html>
END
}

#====================== �t���[���Z�b�g�o�͂��ザ�񂱂� ====
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
<p>�t���[�����T�|�[�g����Web�u���E�U�����g�����������B</p>
</noframes>
</frameset>
</html>
END
}


#====================== �t���[���Z�b�g�o�� ====
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
<p>�t���[�����T�|�[�g����Web�u���E�U�����g�����������B</p>
</noframes>
</frameset>
</html>
END
}


#======================== ���̓t���[���o�� ====
sub printInputFrame
{
	printHttpHeader();
	
	print <<END;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">

<title>�������</title></head>
<body>
<form action="$ENV{'SCRIPT_NAME'}" target="body" method="POST"
	name="box"
	onSubmit='setTimeout("{ document.box.clear.click(); document.box.text.focus(); }", 300);'>
<strong class="name$FORM{'hero'}">$FORM{'name'}</strong><br>
<input type="text" name="text" size="60">
<input type="submit" value="��������">
<button onClick="window.open('dat/log.dat')">���O</button>
<input type="reset" value="�N���A" name="clear">

<input type="hidden" name="frame" value="view">
<input type="hidden" name="mode" value="write">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="entry" value="$FORM{'entry'}">
<input type="hidden" name="hero" value="$FORM{'hero'}">
<input type="hidden" name="custom" value="$FORM{'custom'}">
</form>
<br>
<form action="$ENV{'SCRIPT_NAME'}" target="_top" method="POST">
<input type="submit" value="�ޏo����">
<input type="hidden" name="mode" value="exit">
<input type="hidden" name="name" value="$FORM{'name'}">
<!--<input type="hidden" name="email" value="$FORM{'email'}">-->
<input type="hidden" name="entry" value="$FORM{'entry'}">
</form>
</body></html>
END
}


#======================== �\���t���[���o�� ====
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

<title>�������</title>

<meta http-equiv="Refresh"
	content="$REFRESH; URL=$ENV{'SCRIPT_NAME'}?frame=view&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">
</head>
<body>
<div>
<a href="$ENV{'SCRIPT_NAME'}?frame=view&name=$encname&entry=$FORM{'entry'}&hero=$FORM{'hero'}&custom=$FORM{'custom'}">[�X�V]</a>
�Q���ҁF$entrants
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


#======================== �G���[�y�[�W�o�� ====
sub printErrorPage
{
	print <<END;
Content-type: text/html; charset=$CHARSET

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CSSPATH/rooper.css">
<title>�������</title></head>
<body><h1>�G���[</h1><p>$_[0]</p></body>
</html>
END
	
	exit;
}


#======================== HTTP�w�b�_�[�o�� ====
sub printHttpHeader
{
	# �O���j�b�W�W�����̕�����
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
	
	# �w�b�_�[�̏o��
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
#========================== �f�����O��ǂݍ��� ====
sub loadBoardfile
{
	open(FILE, "<$BOARDFILE")
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 1) };
	@BOARD = <FILE>;
	close(FILE);
}
#========================== �f���ɔ������������� ====
sub writeBoard
{
	printErrorPage("���e�̋L���s���ł��B���{����܂߂Ă�������") if $FORM{'text'} !~ /[^a-zA-Z0-9\-\.\=\_\/\:\;\@\%\&\?\!\+\~\(\)\|\*\$\'\"\#\r\n\<\>\ ]/;
	printErrorPage("�g�p�s�ȕ����񂪊܂܂�Ă��܂�.") if $FORM{'text'} =~ /(biagra)|(viagra)|(buy)|(mail)|(sex)|(nice)|(site)/;
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
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 2) };
	print FILE @BOARD;
	close(FILE);
}
}


#========================== �������������� ====
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
}


#====================== �Q���҂̍X�V�E�� ====
sub updateEntrants
{
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
		#2013.11.07.add����
		my $tragedyset="";
		if($custom ==1){
			$tragedyset="Original Tragedy";
		}elsif($custom ==2){
			$tragedyset="���Ń��[��";
		}elsif($custom == 3){
			$tragedyset="VisualNovel";
		}elsif($custom == 4){
			$tragedyset="HauntedStage";
		}elsif($custom == 5){
			$tragedyset="MysteryCircle";
		}elsif($custom == 6){
			$tragedyset="FirstSteps";
		}elsif($custom == 7){
			$tragedyset="Basic Tragedy ��";
		}elsif($custom == 8){
			$tragedyset="Mystery Circle ��";
		}elsif($custom == 9){
			$tragedyset="Haunted Stage ��";
		}elsif($custom == 10){
			$tragedyset="Another Horizon";
		}
		else{
			$tragedyset="Basic Tragedy";
		}
	#2013.11.07.add����

		if($name eq $FORM{'name'} and $entry == $FORM{'entry'}) {
			$noentry = 0;
			if(not $delflag) {
				# �����̍ŏI�X�V���Ԃ��X�V
				$lines[$i] = "$name:$entry:$now:$FORM{'hero'}:$custom\n";
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
=pod 2013.11.07.cut		
		#2012.5.5�ǋL����
		$tmp="";
#		if($hero eq "writer"){ 2.17���O

			if($custom ==1){
				$tmp="(Original Tragedy)";
			}elsif($custom ==2){
				$tmp="(���Ń��[��)";
			}elsif($custom == 3){
				$tmp="(VisualNovel)";
			}elsif($custom == 4){
				$tmp="(HauntedStage)";
			}elsif($custom == 5){
				$tmp="(MysteryCircle)";
			}elsif($custom == 6){
				$tmp="(FirstSteps)";
			}elsif($custom == 7){
				$tmp="(Basic Tragedy ��)";
			}elsif($custom == 8){
				$tmp="(Mystery Circle ��)";
			}elsif($custom == 9){
				$tmp="(Haunted Stage ��)";
			}elsif($custom == 10){
				$tmp="(Another Horizon)";
			}
			else{
				$tmp="(Basic Tragedy)";
			}
=cut
#		}2.17���O
		#����
#		push @users, qq|<span class="name$hero">$name</span>$tmp|;2013.11.07.cut
	push @users, qq|<span class="name$hero">$name</span>($tragedyset)|;#2013.11.07.add
	}
	if($noentry and $FORM{'entry'}) {
		push @lines, "$FORM{'name'}:$FORM{'entry'}:$now:$FORM{'hero'}:$FORM{'custom'}\n";
#		push @users, $FORM{'name'};
		#2012.5.5�ǋL����
=pod 2013.11.07.cut	
		$tmp="";
#		if($FORM{'hero'} eq "writer"){ 2/17���O
			if($FORM{'custom'} ==1){
				$tmp="(Original Tragedy)";
			}elsif($FORM{'custom'} ==2){
				$tmp="(���Ń��[��)";
			}elsif($custom == 3){
				$tmp="(VisualNovel)";
			}elsif($custom == 4){
				$tmp="(HauntedStage)";
			}elsif($custom == 5){
				$tmp="(MysteryCircle)";
			}elsif($custom == 6){
				$tmp="(FirstSteps)";
			}elsif($custom == 7){
				$tmp="(Basic Tragedy ��)";
			}elsif($custom == 8){
				$tmp="(Mystery Circle ��)";
			}elsif($custom == 9){
				$tmp="(Haunted Stage ��)";
			}elsif($custom == 10){
				$tmp="(Another Horizon)";
			}
			else{
				$tmp="(Basic Tragedy)";
			}
#		}2.17���O
		#����
=cut
#		push @users, qq|<span class="name$FORM{'hero'}">$FORM{'name'}</span>$tmp|; #2013.11.07.cut
		push @users, qq|<span class="name$FORM{'hero'}">$FORM{'name'}</span>($tragedyset)|;#2013.11.07.add
	}
	
	open(FILE, ">$ENTRYFILE")
		or printErrorPage("�Q���҃t�@�C�����J���܂���");
	eval{ flock(FILE, 2) };
	print FILE @lines;
	close(FILE);
	
	return @users;
}


#=========================== URL�G���R�[�h ====
sub urlencode
{
	my $value = shift @_;
	
	$value =~ tr/ /+/;
	$value =~ s/(\W)/sprintf("%%%02X", ord($1))/eg;
	return $value;
}


#================== �N�b�L�[�f�[�^��荞�� ====
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
#================== �r�{�ƕō쐬 ====
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
<title>�S��RoopeR$_[0]</title>
</head>
<body>
<div id="waku">
<div id="head"><form id="headform">
	<table id="buttonTable">
	<tr id="tr1">
	<td><button type="button" name="ruledisplay" onclick=changeboard('#gameboard')>�{�[�h�\\��</button></td>
	<td><button type="button" name="ruledisplay" onclick=changeboard('#RuleList')>���[���\\��</button></td>
	<td><button type="button" name="roledisplay" onclick="changeboard('#RoleList')">��E�\\��</button></td>
	<td><button type="button" name="roledisplay" onclick="changeboard('#CharList')">�L�����N�^�[</button></td>
	<td rowspan="2"><button type="button" onclick="loadData('data')" value="move" id="updatebutton">�X�V</button></td>
	</tr><tr>
	<td><button type="button" name="roledisplay" onclick="viewCloseSheet();" id="closesheet">����J�V�[�g</button></td>
	<td><button type="button" name="roledisplay" onclick="viewOpenSheet();" id="opensheet">���J�V�[�g</button></td>
	<td><button type="button" name="roledisplay" onclick="OpenSheet();" style="display:none;" id="openclosesheet">����J�V�[�g�����J</button></td>
	<td></td>
	</tr>
	<tr>
	<td><button type="button" name="save" onclick="saveCookie();" id="savecookie">�Z�[�u</button></td>
	<td><button type="button" name="load" onclick="loadCookie();" id="loadcookie">���[�h</button></td>
	<td></td>
	<td><button id="resetgame" type="button" onclick="resetphase()" value="move" style="display:none;">�Q�[�����Z�b�g</button></td>
	
	<td>�����X�V�F<select id="uptime" onchange="changeuptime(this);">
				<option value="15">15�b</option>
				<option value="30">30�b</option>
				<option value="60" selected>�P��</option>
				<option value="300">�T��</option>
				<option value="0">���Ȃ�</option>
	</select></td>
	</tr>
	<tr>
	<td colspan="2"><button id="nextphasebutton" type="button" onclick="nextPhase()" value="move">���̃t�F�C�Y</button></td>
	</td>
	<td id="tableLeaderSkip"></td>
	<td id="tableLoopEnd"></td>
	</tr>
	</table>
</form></div>
<div id="gameboard">
	<div id="writer"></div>
	<div id="left">
		<button type="button" onclick="jQuery('#writer').toggle();" value="" id="writerbutton">�\\��<br>/��\\��</button>
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
#================== ��l���ō쐬 ====
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
<title>�S��RoopeRHero0</title>
</head>
<body>
<div id="waku">
<div id="head"><form id="headform">
	<table id="buttonTable">
	<tr id="tr1">
	<td><button type="button" name="ruledisplay" onclick=changeboard('#gameboard')>�{�[�h�\\��</button></td>
	<td><button type="button" name="ruledisplay" onclick=changeboard('#RuleList')>���[���\\��</button></td>
	<td><button type="button" name="roledisplay" onclick="changeboard('#RoleList')">��E�\\��</button></td>
	<td><button type="button" name="roledisplay" onclick="changeboard('#CharList')">�L�����N�^�[</button></td>
	<td rowspan="2"><button type="button" onclick="loadData('data')" value="move" id="updatebutton">�X�V</button></td>
	</tr><tr>
	<td><button type="button" name="roledisplay" onclick="viewCloseSheet();" id="closesheet">����J�V�[�g</button></td>
	<td><button type="button" name="roledisplay" onclick="viewOpenSheet();" id="opensheet">���J�V�[�g</button></td>
	<td></td>
	<td></td>
	</tr><tr>
	<td colspan="2"><button id="nextphasebutton" type="button" onclick="nextPhase()" value="move">���̃t�F�C�Y</button></td>
	<td></td><td></td>
	<td>�����X�V�F<select id="uptime" onchange="changeuptime(this);">
				<option value="15">15�b</option>
				<option value="30">30�b</option>
				<option value="60" selected>�P��</option>
				<option value="300">�T��</option>
				<option value="0">���Ȃ�</option>
	</select></td>
	</tr>
</table>
</form></div>
<div id="gameboard">
	<div id="writer"></div><!--toggle('writer')-->
	<div id="left"><button type="button" onclick="jQuery('#writer').toggle();" value="" id="writerbutton">�\��<br>/��\��</button></div><div id="center"><div id="board"></div></div><div id="right"></div>
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

#================== �r�{�쐬�ō쐬 ====
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
<title>�S��RoopeR</title>
</head>
<title>�V�[�g</title></head>
<body>
<h1>�r�{</h1>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<input type="hidden" name="mode" value="resetsave">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="custom" value="$FORM{'custom'}">
<input type="submit" value="���݂̃Q�[���{�[�h�����Z�b�g" style="font-size:200%">
<input type="hidden" name="entry" value="$FORM{'entry'}">
</form>
<hr>
END
if(	$FORM{'custom'}==0||	$FORM{'custom'}==3){
	print <<END;
<form method='post' action='./scenario.cgi' ENCTYPE='multipart/form-data'>
�t�@�C���I���F <input type='file' name='upload_file'size='30'>
<input type='hidden' name='filetype' value='text'>
<input type="hidden" name="mode" value="loadscenario">
<input type='submit' value='�A�b�v���[�h'>
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
	print qq|<button type="button" onclick="changeselectbox()">�I������ɕύX����B</button>|;
}
	print <<END;
<table>
<tr><th>���[��Y</th><td id="ruleY"><input type="text" name="ruleY" size="40"></td></tr>
<tr><th>���[��X1</th><td id="ruleX1"><input type="text" name="ruleX1" size="40"></td></tr>
<tr><th>���[��X2</th><td id="ruleX2"><input type="text" name="ruleX2" size="40"></td></tr>
<table>
<tr id="chartablehead"><th>�l��</th><th>��E</th></tr>
<tr id="chartabletr0"><td>�j�q�w��</td><td id="char0"><input type="text" name="shonen" size="30" value="�p�[\�\\��"></td></tr>
<tr id="chartabletr1"><td>���q�w��</td><td id="char1" ><input type="text"name="shojo" size="30" value="�p�[\�\\��"></td></tr>
<tr id="chartabletr2"><td>����l</td><td  id="char2"><input type="text"  name="ojo" size="30" value="�p�[\�\\��"></td></tr>
<tr id="chartabletr3"><td>�ޏ�</td><td id="char3">     <input type="text" name="miko" size="30" value="�p�[\�\\��"></td></tr>
<tr id="chartabletr4"><td>�Y��</td><td id="char4"><input type="text"     name="keiji" size="30" value="�p�[\�\\��"></td></tr>
<tr id="chartabletr5"><td>�T�����[�}��</td><td id="char5" ><input type="text" name="salary" size="30" value="�p�[\�\\��"></td></tr>
<tr id="chartabletr6"><td>���</td><td id="char6"><input type="text"   name="joho" size="30" value="�p�[\�\\��"></td></tr>
<tr id="chartabletr7"><td>���</td><td  id="char7"><input type="text"    name="isha" size="30" value="�p�[\�\\��"></td></tr>
<tr id="chartabletr8"><td>���@����</td><td id="char8"><input type="text"   name="kanja" size="30" value="�p�[\�\\��"></td></tr>
</table>
<table>
<tr><th>����</th><th>����</th><th width="300px">��������</th><th>�Ɛl</th></tr>
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
		$sample1="�E�l����";
		$sample2="��\�\\�Ȃ�ΔƐl�Ɠ����G���A�ɂ���Ɛl�ȊO�̔C�ӂ̃L�����N�^�[�P�l�����S������B";
	}
	if($i==2){
		$sample1="�s���g��";
		$sample2="�C�ӂ̃L�����N�^�[�P�l�ɕs���J�E���^�[���Q�u���A�C�ӂ̕ʂ̃L�����N�^�[�P�l�ɈÖ�J�E���^�[���P�u���B";
	}
	if($i==3){
		$sample1="���E";
		$sample2="�Ɛl�͎��S����B";
	}
	if($i==4){
		$sample1="�a�@�̎���";
		if($FORM{'custom'} eq "2"){
			$sample2="�a�@�ɈÖ�J�E���^�[���P�ȏ�u����Ă���ꍇ�A�a�@�ɂ���L�����N�^�[�S�������S����B";
		}else{
			$sample2="�a�@�ɈÖ�J�E���^�[���P�ȏ�u����Ă���ꍇ�A�a�@�ɂ���L�����N�^�[�S�������S����B����ɁA�a�@�ɈÖ�J�E���^�[���Q�ȏ�u����Ă���ꍇ�A��l���͎��S����B";

		}
	}
	if($i==5){
		$sample1="�׋C�̉���";
		$sample2="�_�ЂɈÖ�J�E���^�[���Q�u���B";
	}
	}
	if($FORM{'custom'} eq "0"||$FORM{"custom"} == 3){
		if($i==6){
			$sample1="�ʗ�";
			$sample2="�Ɛl��C�ӂ̃{�[�h�Ɉړ�������B";
		}
		if($i==7){
			$sample1="\�\\�I";
			$sample2="�ǂ��炩��I�ԁB\n�P�D�Ɛl�Ɠ����G���A�ɂ���L�����N�^�[����F�D�J�E���^�[���Q�܂Ŏ�菜���i�Q�l�Ɋ���U���Ă��悢�j�B\n�Q�D�Ɛl�Ɠ����G���A�ɂ���L�����N�^�[�ɗF�D�J�E���^�[���Q�܂Œu���i�Q�l�Ɋ���U���Ă��悢�j�B";
		}
	}else{}
	if($FORM{'custom'} eq "3"){
		if($i==3){
			$sample1="���z��";
			$sample2="�ȍ~�A�Ɛl��S�Ẵ{�[�h�ɂ��Ȃ����̂Ƃ��Ĉ����A�J�[�h���Z�b�g���邱�Ƃ��ł��Ȃ��Ȃ�B";
		}
		if($i==4){
			$sample1="�e�����Y��";
			$sample2="�s�s�ɈÖ�J�E���^�[���P�ȏ�u����Ă���ꍇ�A�s�s�ɂ���L�����N�^�[�S�������S����B����ɁA�s�s�ɈÖ�J�E���^�[���Q�ȏ�u����Ă���ꍇ�A��l���͎��S����B";
		}
		if($i==8){
			$sample1="���[�g�m��";
			$sample2="�������N����A���Ɛl�̗F�D\�\\�͂��g�p�ł���Ƃ��A�Ɛl�̖�E���L�[�p�[\�\\���ɕύX����B";
		}
		if($i==9){
			$sample1="�Ƃ��߂����e";
			$sample2="�������N����A���Ɛl�ɗF�D�J�E���^�[���P������Ă��Ȃ��ꍇ�AEX�J�E���^�[��p�ӂ���B�����l�͂O�ł���B���̓�����^�[���I���t�F�C�Y���Ƃ�EX�J�E���^�[���P����������B�R�ɂȂ������_�őS�ẴL�����N�^�[�̗F�D�J�E���^�[���Q��������B�Ɛl�ɗF�D�J�E���^�[���悹���EX�J�E���^�[�̒l�͂O�ɂȂ�B";
		}
	}
	if($FORM{'custom'} eq "4"){
		if($i==1){
			$sample1="�A���E�l";
			$sample2="��\�\\�Ȃ�ΔƐl�Ɠ����G���A�ɂ���Ɛl�ȊO�̔C�ӂ̃L�����N�^�[�P�l�����S������B\n���̘A���E�l�̔Ɛl�ƂȂ��Ă���L�����N�^�[�������̔Ɛl�Ƃ��邱�Ƃ��ł���B";
		}
		if($i==2){
			$sample1="�s���g��";
			$sample2="�C�ӂ̃L�����N�^�[�P�l��[�s���J�E���^�[]���Q�u���A�C�ӂ̕ʂ̃L�����N�^�[�P�l��[�Ö�J�E���^�[]���P�u���B";
		}
		if($i==3){
			$sample1="�W�c���E";
			$sample2="�Ɛl��[�Ö�J�E���^�[]���P�ȏと�Ɛl�Ɠ����G���A�ɂ���L�����N�^�[�S�Ă����S������B";
		}
		if($i==4){
			$sample1="��s��";
			$sample2="���s���ՊE-2��Ex�Q�[�W���P���������A���[�_�[�ł���v���C���[�̓L�����N�^�[���P�l�I�ԁB���̃L�����N�^�[�����S������B";
		}
		if($i==5){
			$sample1="�a�@�̎���";
			$sample2="�a�@�ɈÖ�J�E���^�[���P�ȏ�u����Ă���ꍇ�A�a�@�ɂ���L�����N�^�[�S�������S����B����ɁA�a�@�ɈÖ�J�E���^�[���Q�ȏ�u����Ă���ꍇ�A��l���͎��S����B";
		}
		if($i==6){
			$sample1="�`��";
			$sample2="�C�ӂ̎��̂P�Ɂm�s���J�E���^�[�n�Ɓm�Ö�J�E���^�[�n���P���u���B";
		}
		if($i==7){
			$sample1="���b�̉��";
			$sample2="�Ɛl�̂���G���A�Ɂu���b�v�J�[�h��u���B�ȍ~�A���̃J�[�h�́u���b�v�Ƃ������O�̖�E���i�C�g���A�ł���L�����N�^�[�Ƃ��Ĉ����B";
		}
		if($i==8){
			$sample1="�S�S��s";
			$sample2="�����㔭�����_�Ђ�[�Ö�J�E���^�[]���P�ȏとEx�Q�[�W���S����������B";
		}
		if($i==9){
			$sample1="��";
			$sample2="�����㔭�����Ɛl�Ɠ����G���A�ɂ���J�[�h�P��C�ӂ̕ʂ̃{�[�h�Ɉړ�������B";
		}
		if($i==10){
			$sample1="����";
			$sample2="�����㔭�����Ɛl�̂���{�[�h�Ɂm�Ö�J�E���^�[�n���Q�u���B";
		}
		if($i==11){
			$sample1="�J��Ԃ�����";
			$sample2="�����㔭����Ex�Q�[�W��1���������A�Ɛl�͑h������B";
		}
	}
	if($FORM{'custom'} eq "5"){
		if($i==1){
			$sample1="�E�l����";
			$sample2="��\�\\�Ȃ�ΔƐl�Ɠ����G���A�ɂ���Ɛl�ȊO�̔C�ӂ̃L�����N�^�[�P�l�����S������B";
		}
		if($i==2){
			$sample1="�s���g��";
			$sample2="�C�ӂ̃L�����N�^�[�P�l�ɕs���J�E���^�[���Q�u���A�C�ӂ̕ʂ̃L�����N�^�[�P�l�ɈÖ�J�E���^�[���P�u���B";
		}
		if($i==3){
			$sample1="���E";
			$sample2="�Ɛl�͎��S����B";
		}
		if($i==4){
			$sample1="�a�@�̎���";
			$sample2="�a�@�ɈÖ�J�E���^�[���P�ȏ�u����Ă���ꍇ�A�a�@�ɂ���L�����N�^�[�S�������S����B����ɁA�a�@�ɈÖ�J�E���^�[���Q�ȏ�u����Ă���ꍇ�A��l���͎��S����B";
		}
		if($i==5){
			$sample1="�e�����Y��";
			$sample2="�s�s�ɈÖ�J�E���^�[���P�ȏ�u����Ă���ꍇ�A�s�s�ɂ���L�����N�^�[�S�������S����B����ɁA�s�s�ɈÖ�J�E���^�[���Q�ȏ�u����Ă���ꍇ�A��l���͎��S����B";
		}
		if($i==6){
			$sample1="�O��";
			$sample2="���s���ՊE-1���Ɛl�Ɠ����G���A�ɂ���L�����N�^�[�P�l�ɕs���J�E���^�[���P�u���B";
		}
		if($i==7){
			$sample1="��E�l";
			$sample2="���s���ՊE�{�P����Ex�Q�[�W�񑝉����u�E�l�����v�Ɓu�s���g��v�����̏��Ŕ���������B�i���ʁAEx�Q�[�W�͂Q��������j";
		}
		if($i==8){
			$sample1="�U�����E";
			$sample2="�Ɛl��Ex�J�[�hA��u���BEx�J�[�hA���u���ꂽ�L�����N�^�[�Ɏ�l���̓J�[�h��u�����Ƃ��ł��Ȃ��B";
		}
		if($i==9){
			$sample1="�s�a";
			$sample2="�Ɛl�Ɠ����G���A�ɂ���L�����N�^�[�̂����A�F�D�J�E���^�[�̒u���ꂽ�P�l���炷�ׂĂ̗F�D�J�E���^�[����菜��";
		}
		if($i==10){
			$sample1="�N���[�Y�h�T�[�N��";
			$sample2="�Ɛl�̂���{�[�h���w�肷��B���������̓����܂߂R���ԁA���̃{�[�h����̈ړ��ƃ{�[�h�ւ̈ړ����֎~����B";
		}
		if($i==11){
			$sample1="��̏e�e";
			$sample2="��Ex�Q�[�W�񑝉������̃t�F�C�Y�̏I�����Ƀ��[�v���I��������B";
		}
	}
	print qq(<tr><td>$i</td><td id="$tmp1" ><input type="text"name="$tmp1" size="20" value="$sample1"></td><td id="$tmp2"><textarea name="$tmp2" rows="3" cols="40">$sample2</textarea></td><td id="$tmp3"><input type="text"  name="$tmp3" size="20"></td></tr>);
}

if($FORM{'custom'} eq "2"){
	$tmp1="4";
	$tmp2="8";
	$tmp3="���[�v���̑��k�֎~�B\n�Ō�̐킢�Ȃ��B\n���̋��Ԃ���B�}�]���v���C���[�͂Ȃ��ł��悢�B";
}else{
	$tmp1="";
	$tmp2="";
	$tmp3="";
}
print "</table>";
if($FORM{'custom'} eq "0"){
	print qq|<input type="hidden" name="map1" value="�w�Z"><input type="hidden" name="map2" value="�_��"><input type="hidden" name="map3" value="�s�s"><input type="hidden" name="map4" value="�a�@">|;
	print qq|<input type="hidden" name="set" value="Basic Tragedy">|;
}elsif($FORM{'custom'} eq "3"){
		print qq|<input type="hidden" name="map1" value="�w�Z"><input type="hidden" name="map2" value="�_��"><input type="hidden" name="map3" value="�s�s"><input type="hidden" name="map4" value="�a�@">|;
	print qq|<input type="hidden" name="set" value="Visual Novel">|;
}	else{
}
print <<END;

<table>
<tr><th>���[�v��</th><td id="loop" ><input type="text" style="ime-mode:disabled;" name="loop" size="5" class="number" value="$tmp1"></td><th>�P���[�v����</th><td id="loopday"><input type="text" class="number" name="loopday" size="10" value="$tmp2"></td></tr>
</table>
<table>
<tr><th>���ʃ��[��</th></tr>
<tr><td><textarea cols="60" rows="5" name="text">$tmp3</textarea></td></tr>
</table>

<input type="submit" value="�r�{����" id="submitbutton" style="font-size:200%">
<input type="reset" value="���Z�b�g">
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
#==================�Z�[�u���Z�b�g ====
sub resetSave{
	open(FILE, ">$SAVEFILE")
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 2) };
	print FILE "char\@0\@3,0,3,0,0,0,0,220,170,0&char\@1\@3,1,3,1,0,0,0,260,170,0&char\@2\@3,2,3,2,0,0,0,300,170,0&char\@3\@2,0,2,0,0,0,0,220,30,0&char\@4\@1,0,1,0,0,0,0,10,170,0&char\@5\@1,1,1,1,0,0,0,50,170,0&char\@6\@1,2,1,2,0,0,0,90,170,0&char\@7\@0,0,0,0,0,0,0,10,30,0&char\@8\@0,1,0,1,0,0,0,50,30,0&plhand\@0\@-1,-1,0,0,0,2,0,0,0,0&plhand\@1\@-1,-1,0,0,1,0,0,0,0,0&plhand\@2\@-1,-1,0,0,2,1,0,0,0,0&gmhand\@3\@-1,-1,0,0,0,0&gmhand\@4\@-1,-1,0,0,0,0&gmhand\@5\@-1,-1,0,0,0,0&board\@0\@0&board\@1\@0&board\@2\@0&board\@3\@0&scenario\@0&phase\@1,1,0";
		close(FILE);
}
#==================�r�{�f�[�^�Z�[�u ====
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
#==================�r�{�f�[�^�N���[�Y�V�[�g====
sub makeCloseSheet{
	open(FILE, ">$CLOSESHEET")
		or printErrorPage("���O�t�@�C�����J���܂���B");
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
<title>�S��RoopeR</title>
</head>
<title>�V�[�g</title></head>
<body>
<h1>�r�{</h1>

END
#//2013/3/7�ǋL����
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
<tr><th></th><th>���[����</th><th>�ǉ����[��</th></tr>
<tr><th>���[��Y</th><td>$FORM{'ruleY'}</td><td style="text-align:left">$FORM{'ruleYadd'}</td></tr>
<tr><th>���[��X1</th><td>$FORM{'ruleX1'}</td><td style="text-align:left">$FORM{'ruleX1add'}</td></tr>
<tr><th>���[��X2</th><td>$FORM{'ruleX2'}</td><td style="text-align:left">$FORM{'ruleX2add'}</td></tr>
</table>
<table>
<tr id="chartablehead"><th>�l��</th><th>��E</th><th>��\�\\��</th><th>\�\\��</th></tr>
<tr id="chartabletr0"><td>�j�q�w��</td><td>$FORM{'shonen'}</td><td>$FORM{'jobun0'}</td><td style="text-align:left">$FORM{'skill0'}</td></tr>
<tr id="chartabletr1"><td>���q�w��</td><td>$FORM{'shojo'}</td><td>$FORM{'jobun1'}</td><td style="text-align:left">$FORM{'skill1'}</td></tr>
<tr id="chartabletr2"><td>����l</td><td>$FORM{'ojo'}</td><td>$FORM{'jobun2'}</td><td style="text-align:left">$FORM{'skill2'}</td></tr>
<tr id="chartabletr3"><td>�ޏ�</td><td>$FORM{'miko'}</td><td>$FORM{'jobun3'}</td><td style="text-align:left">$FORM{'skill3'}</td></tr>
<tr id="chartabletr4"><td>�Y��</td><td>$FORM{'keiji'}</td><td>$FORM{'jobun4'}</td><td style="text-align:left">$FORM{'skill4'}</td></tr>
<tr id="chartabletr5"><td>�T�����[�}��</td><td>$FORM{'salary'}</td><td>$FORM{'jobun5'}</td><td style="text-align:left">$FORM{'skill5'}</td></tr>
<tr id="chartabletr6"><td>���</td><td>$FORM{'joho'}</td><td>$FORM{'jobun6'}</td><td style="text-align:left">$FORM{'skill6'}</td></tr>
<tr id="chartabletr7"><td>���</td><td>$FORM{'isha'}</td><td>$FORM{'jobun7'}</td><td style="text-align:left">$FORM{'skill7'}</td></tr>
<tr id="chartabletr8"><td>���@����</td><td>$FORM{'kanja'}</td><td>$FORM{'jobun8'}</td><td style="text-align:left">$FORM{'skill8'}</td></tr>
</table>
<table>
<tr><th>����</th><th>����</th><th>��������</th><th>�Ɛl</th></tr>
END
#//2013/3/7�ǋL����
}else{
	print FILE <<END;
<table>
<tr><th>���[��Y</th><td>$FORM{'ruleY'}</td></tr>
<tr><th>���[��X1</th><td>$FORM{'ruleX1'}</td></tr>
<tr><th>���[��X2</th><td>$FORM{'ruleX2'}</td></tr>
</table>
<table>
<tr id="chartablehead"><th>�l��</th><th>��E</th></tr>
<tr id="chartabletr0"><td>�j�q�w��</td><td>$FORM{'shonen'}</td></tr>
<tr id="chartabletr1"><td>���q�w��</td><td>$FORM{'shojo'}</td></tr>
<tr id="chartabletr2"><td>����l</td><td>$FORM{'ojo'}</td></tr>
<tr id="chartabletr3"><td>�ޏ�</td><td>$FORM{'miko'}</td></tr>
<tr id="chartabletr4"><td>�Y��</td><td>$FORM{'keiji'}</td></tr>
<tr id="chartabletr5"><td>�T�����[�}��</td><td>$FORM{'salary'}</td></tr>
<tr id="chartabletr6"><td>���</td><td>$FORM{'joho'}</td></tr>
<tr id="chartabletr7"><td>���</td><td>$FORM{'isha'}</td></tr>
<tr id="chartabletr8"><td>���@����</td><td>$FORM{'kanja'}</td></tr>
</table>
<table>
<tr><th>����</th><th>����</th><th>��������</th><th>�Ɛl</th></tr>
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
<tr><th>���[�v��</th><td>$FORM{'loop'}</td><th>�P���[�v����</th><td>$FORM{'loopday'}</td></tr>
</table>
END
if($FORM{"custom"}==0||$FORM{"custom"}==3){
print FILE "<table>";
print FILE qq|<tr><th>�S���Z�b�g</th><td style="border-width:2px;">$FORM{'set'}</td></tr>|;
print FILE "</table>";
print FILE "<table>";
print FILE qq|<tr><th>�g�p�}�b�v</th><td>$FORM{'map1'}</td><td>$FORM{'map2'}</td><td>$FORM{'map3'}</td><td>$FORM{'map4'}</td></tr>|;
print FILE "</table>";
}

if(!($FORM{'sodan'} eq "")){
	print FILE "<table>";
	print FILE qq|<tr><th>���k</th><td>$FORM{'sodan'}</td></tr>|;
	print FILE "</table>";
}

if(!($FORM{'text'} eq "")){
	print FILE <<END;
<table>
<tr><th>���ʃ��[��</th></tr>
<tr><td>$FORM{'text'}</td></tr>
</table>
END
}
#�V�i���I�̓���
$FORM{'tokutyo'} =~ s/\r//; $FORM{'tokutyo'} =~ s/\n//;

if(!($FORM{'tokutyo'} eq "")){
	$FORM{'tokutyo'}=~ s|\\n|</p><p>|g;
	$FORM{'tokutyo'}=~ s|\\n|</p><p>|g;
	print FILE "<table>";
	print FILE qq|<tr><th>�V�i���I�̓���</th></tr><tr><td style="text-align:left;"><p>$FORM{'tokutyo'}</p></td></tr>|;
	print FILE "</table>";
}
#�r�{�Ƃւ̎w�j
$FORM{'sisin'} =~ s/\r//; $FORM{'sisin'} =~ s/\n//;$FORM{'sisin'}=~ s|\\n|</p><p>|g;
if(!($FORM{'sisin'} eq "")){
#	$FORM{'sisin'}=~ s|\\n|</p><p>|g;
	print FILE "<table>";
	print FILE qq|<tr><th>�r�{�Ƃւ̎w�j</th></tr><tr><td style="text-align:left;"><p>$FORM{'sisin'}</p></td></tr>|;
	print FILE "</table>";
}
	$FORM{"joken1"} =~ s/\r//;
	$FORM{"joken1"} =~ s/\n//;
if(!($FORM{"joken1"} eq "")){print FILE qq|<table><tr><th colspan="2">�r�{�Ƃ̏�������</th></tr>|;}
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
		or printErrorPage("���O�t�@�C�����J���܂���B");
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
<title>�S��RoopeR</title>
</head>
<title>�V�[�g</title></head>
<body>
<h1>���J�V�[�g</h1>
<table>
<tr><th>���[�v��</th><td>$FORM{'loop'}</td><th>�P���[�v����</th><td>$FORM{'loopday'}</td></tr>
</table>
END
#if($FORM{"custom"}==0||$FORM{"custom"}==3){
if($FORM{'custom'} eq "1"){
	$FORM{'set'}="Originail Tragedy";
}elsif($FORM{'custom'} eq "2"){
	$FORM{'set'}="�S��RoopeR����";
}elsif($FORM{'custom'} eq "3"){
	$FORM{'set'}="Visual Novel";
}elsif($FORM{'custom'} eq "4"){
	$FORM{'set'}="Haunted Stage";
}elsif($FORM{'custom'} eq "5"){
	$FORM{'set'}="Mystery Circle";
}elsif($FORM{'custom'} eq "6"){
	$FORM{'set'}="First Steps";
}elsif($FORM{'custom'} eq "7"){
	$FORM{'set'}="Basic Tragedy ��";
}elsif($FORM{'custom'} eq "8"){
	$FORM{'set'}="Mystery Circle ��";
}elsif($FORM{'custom'} eq "9"){
	$FORM{'set'}="Haunted Stage ��";
}elsif($FORM{'custom'} eq "10"){#2013.11.07.add
	$FORM{'set'}="Another Horizon";
}else{
	$FORM{'set'}="Basic Tragedy";
}
$FORM{'map1'}="�a�@";
$FORM{'map2'}="�s�s";
$FORM{'map3'}="�_��";
$FORM{'map4'}="�w�Z";

print FILE "<table>";
print FILE qq|<tr><th>�S���Z�b�g</th><td style="border-width:2px;">$FORM{'set'}</td></tr>|;
print FILE "</table>";
print FILE "<table>";
print FILE qq|<tr><th>�g�p�}�b�v</th><td>$FORM{'map1'}</td><td>$FORM{'map2'}</td><td>$FORM{'map3'}</td><td>$FORM{'map4'}</td></tr>|;
print FILE "</table>";
#}

if(!($FORM{'sodan'} eq "")){
	print FILE "<table>";
	print FILE qq|<tr><th>���k</th><td>$FORM{'sodan'}</td></tr>|;
	print FILE "</table>";
}
	print FILE <<END;
<table>
<tr><th>����</th><th>����\�\\��\</th><th>��������</th></tr>
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
<tr><th>���ʃ��[��</th></tr>
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
#================== �I���W�i���r�{�쐬�ō쐬 ====
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
<title>�S��RoopeR</title>
</head>
<title>�V�[�g</title></head>
<body>
<h1>�r�{</h1>
<hr>
<font color="red">�����Z�b�g��Y���Ɠ����Ȃ����Ƃ�����܂��B</font>
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<input type="hidden" name="mode" value="resetsave">
<input type="hidden" name="name" value="$FORM{'name'}">
<input type="hidden" name="custom" value="1">
<input type="submit" value="���݂̃Q�[���{�[�h�����Z�b�g" style="font-size:200%">
<input type="hidden" name="entry" value="$FORM{'entry'}">
</form>
<hr>
<button type="button" name="" onclick="customform('rule.csv','text')" style="font-size:150%">���[���̃A�b�v���[�h</button>
<br>
�������R�[�hUTF-8��20kb�ȉ���txt�܂���csv�`���B
<form action="$ENV{'SCRIPT_NAME'}" method="POST">
<table>
<tr><th>���[��Y</th><td><input type="text" name="ruleY" size="40"></td></tr>
<tr><th>���[��X1</th><td><input type="text" name="ruleX1" size="40"></td></tr>
<tr><th>���[��X2</th><td><input type="text" name="ruleX2" size="40"></td></tr>
</table>
<hr>
<button type="button" name="" onclick="customform('char.csv','text')" style="font-size:150%">�L�����N�^�[�̃A�b�v���[�h</button>
<br>
�������R�[�hUTF-8��20kb�ȉ���txt�܂���csv�`���B
<table>
<tr><th>�l��</th><th>��E</th><th>�摜</th><th>�A�b�v���[�h<br>�i35�~50px��png�`��20kb�ȉ��j</th></tr>
END
my $i;
for($i=0;$i<13;$i++){
	my $j=$i+1;
	print qq|<tr id="chartr$i"><input type="hidden" name="customcharname$i" id="customcharname$i"  value="char$i"><td id="customcharnameprev$i">�L�����N�^�[$j</td><td><input type="text" name="char$i" size="30" value="�p�[\�\\��"></td><td><img id="customchar$i" alt="char$i" src="custom/img/character/char$i.png" style="width:35px;height:50px;"></td><td><button type="button" name="" onclick="customform('char$i.png','img')" style="font-size:100%">�摜�t�@�C���A�b�v���[�h</button></td></tr>|;
}
	print <<END;
</table>
<input type="hidden" name="charnum" value="13" id="charnum">
<hr>
<table>
<tr><th>�{�[�h</th><th>�摜</th><th>�A�b�v���[�h</th><td rowspan="5"><img src="custom/img/board.png" alt="board" name="board" id="boardimg"></td><td rowspan="5"><button type="button" name="" onclick="customform('board.png','img')" style="font-size:100%">�摜�t�@�C���A�b�v���[�h</button><br>(400�~283px��png�`��<br>250kb�ȉ��j</td></tr>
END
for($i=0;$i<4;$i++){
	$j=$i+1;
	print qq|<tr><input type="hidden" name="customboard$i" id="customboard$i"  value="�{�[�h$i"><td id="customboardprev$i">�{�[�h$j</td><td><img id="customboard$i" alt="char$i" src="custom/img/character/board$i.png" style="width:35px;height:50px;"></td><td><button type="button" name="" onclick="customform('board$i.png','img')" style="font-size:100%">�摜�t�@�C���A�b�v���[�h</button></td></tr>|;
}
	print <<END;
</table>
<hr>
<table>
END
	for($i=0;$i<3;$i++){
	$j=$i+1;
	print qq|<tr><td>��l��$j</td><td><img id="customhero$i" alt="hand$i" src="custom/img/hand/hero$i.png" style="width:35px;height:50px;"></td><td><button type="button" name="" onclick="customform('hero$i.png','img')" style="font-size:100%">�摜�t�@�C���A�b�v���[�h</button></td></tr>|;
}
print qq|<tr><td>�r�{��</td><td><img id="customwrite" alt="writer" src="custom/img/hand/write.png" style="width:35px;height:50px;"></td><td><button type="button" name="" onclick="customform('write.png','img')" style="font-size:100%">�摜�t�@�C���A�b�v���[�h</button></td></tr>|;

print <<END;
</table>
<hr>
<table>
<tr><th>����</th><th>����</th><th>��������</th><th>�Ɛl</th></tr>
END
for ($i=1;$i<=10;$i++){
	$tmp1="day".$i;
	$tmp2="kouka".$i;
	$tmp3="han".$i;
	$sample1="";
	$sample2="";
	if($i==1){
		$sample1="�E�l����";
		$sample2="��\�\\�Ȃ�ΔƐl�Ɠ����G���A�ɂ���Ɛl�ȊO�̔C�ӂ̃L�����N�^�[�P�l�����S������B";
	}
	if($i==2){
		$sample1="�s���g��";
		$sample2="�C�ӂ̃L�����N�^�[�P�l�ɕs���J�E���^�[���Q�u���A�C�ӂ̕ʂ̃L�����N�^�[�P�l�ɈÖ�J�E���^�[���P�u���B";
	}
	if($i==3){
		$sample1="���E";
		$sample2="�Ɛl�͎��S����B";
	}
	if($i==4){
		$sample1="�a�@�̎���";
		$sample2="�a�@�ɈÖ�J�E���^�[���P�ȏ�u����Ă���ꍇ�A�a�@�ɂ���L�����N�^�[�S�������S����B����ɁA�a�@�ɈÖ�J�E���^�[���Q�ȏ�u����Ă���ꍇ�A��l���͎��S����B";
	}
	if($i==5){
		$sample1="�׋C�̉���";
		$sample2="�_�ЂɈÖ�J�E���^�[���Q�u���B";
	}
	print qq(<tr><td>$i</td><td><input type="text" name="$tmp1" size="20" value="$sample1"></td><td><textarea name="$tmp2" rows="3" cols="40">$sample2</textarea></td><td><input type="text" name="$tmp3" size="20"></td></tr>);
}

print <<END;
</table>
<hr>
<table>
<tr><th>���[�v��</th><td><input type="text" name="loop" size="5" class="number"></td><th>�P���[�v����</th><td><input type="text" class="number" name="loopday" size="10"></td></tr>
</table>
<table>
<tr><th>���ʃ��[��</th></tr>
<tr><td><textarea cols="60" rows="5" name="text"></textarea></td></tr>
</table>

<input type="submit" value="�r�{����" style="font-size:200%">
<input type="reset" value="���Z�b�g">
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
		or printErrorPage("���O�t�@�C�����J���܂���B");
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
<title>�S��RoopeR</title>
</head>
<title>�V�[�g</title></head>
<body>
<h1>�r�{</h1>
<table>
<tr><th>���[��Y</th><td>$FORM{'ruleY'}</td></tr>
<tr><th>���[��X1</th><td>$FORM{'ruleX1'}</td></tr>
<tr><th>���[��X2</th><td>$FORM{'ruleX2'}</td></tr>
<table>
<tr><th>�l��</th><th>��E</th></tr>
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
<tr><th>����</th><th>����</th><th>��������</th><th>�Ɛl</th></tr>
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
<tr><th>���[�v��</th><td>$FORM{'loop'}</td><th>�P���[�v����</th><td>$FORM{'loopday'}</td></tr>
</table>
<table>
<tr><th>���ʃ��[��</th></tr>
<tr><td>$FORM{'text'}</td></tr>
</table>
</body>
</html>
END
	close(FILE);

	open(FILE, ">$CHARFILE")
		or printErrorPage("���O�t�@�C�����J���܂���B");
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
#==================���[�p�[�ԋr�{�쐬�ō쐬 ====
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
<title>�V�[�g</title></head>
<body>
<h1>�r�{</h1>
<hr>
<strong>�T���v���V�i���I</strong>�F<select id="samplescenario">
<option value="-1">���I��</option>
</select>
<hr>
<form action="$ENV{'SCRIPT_NAME'}" id="mainform" method="POST">
<strong style='font-size:16pt'>�^�C�g��</strong>�F<input type='text' name='scenarioTitle' id='scenarioTitle' style='font-size:16pt' size='40'>
<hr>
<table>
<tr><th></th><th></th><th>�ǉ���E</th><th style="width:500px;">�ǉ����[��</th></tr>
<tr><th>���[��Y</th><td id="ruleY" ><input type="text" name="ruleY" size="40"></td><td id="ruleYrole"></td><td id="ruleYskill"></td></tr>
<tr><th>���[��X1</th><td id="ruleX1"><input type="text" name="ruleX1" size="40"></td><td id="ruleX1role"></td><td id="ruleX1skill"></td></tr>
END
if($FORM{'custom'} ne '6'){
	print qq|<tr id="rule2"><th>���[��X2</th><td id="ruleX2"><input type="text" name="ruleX2" size="40"></td><td id="ruleX2role"></td><td id="ruleX2skill"></td></tr>|;
}
	print <<END;
</table>
<hr>
<table>
<tr><th>�g�p</th><th>�摜</th><th>�l��</th><th>��E</th><th>��\�\\��</th><th style="width:500px;">��E\�\\��</th></tr>
END
my $i;
for($i=0;$i<20;$i++){
	my $j=$i+1;
	if($i==0||$i==1||$i==3||$i==5||$i==7||$i==8){
		print qq|<tr id="chartr$i"><input type="hidden" name="customcharname$i" id="customcharname$i"  value="char$i"><td><input type="checkbox" name="usecheck_$i" id="usecheck_$i" checked></td><td><img id="customchar$i" alt="char$i" src="$CHARIMGPATH/char$i.png" style="width:35px;height:50px;"></td><td id="customcharnameprev$i">�L�����N�^�[$j</td><td id="char$i"><input type="text" name="char$i" size="30" value="�p�[\�\\��"></td><td id="jobunbox$i"></td><td id="skillbox$i"></td></tr>|;
	}else{
		print qq|<tr id="chartr$i"><input type="hidden" name="customcharname$i" id="customcharname$i"  value="char$i"><td><input type="checkbox" name="usecheck_$i" id="usecheck_$i"></td><td><img id="customchar$i" alt="char$i" src="$CHARIMGPATH/char$i.png" style="width:35px;height:50px;"></td><td id="customcharnameprev$i">�L�����N�^�[$j</td><td id="char$i"><input type="text" name="char$i" size="30" value="�p�[\�\\��"></td><td id="jobunbox$i"></td><td id="skillbox$i"></td></tr>|;
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
<tr><th>����</th><th>����</th><th style="width:500px;">��������</th><th>�Ɛl</th></tr>
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
<tr><th>���[�v��</th><td id="loop"><input type="text" name="loop" size="5" class="number"></td><th>�P���[�v����</th><td id="loopday"><input type="text" class="number" name="loopday" size="10"></td><th>�_�i�o�ꃋ�[�v</th><td id="sinkaku_add_loop"><input type="text" class="number" name="sinkaku_loopday" size="10"></td></tr>
</table>
<table>
<tr><th>���ʃ��[��</th></tr>
<tr><td><textarea cols="60" rows="5" name="text" id="opentext">���k�s��/���k�� \n�啨�̃e���g���[�F[] \n���̑����L�������L���B\n���J�V�[�g�B</textarea></td></tr>
</table>
<table>
<tr><th>�r�{�ƃ���</th></tr>
<tr><td><textarea cols="60" rows="5" name="sisin" id="closetext">�ŏ��̎�D�̒u������A���������Ȃǂ̋r�{�Ɨp�����B\n����J�V�[�g�B��l���ɂ͌��J����܂���B</textarea></td></tr>
</table>

<input type="submit" value="�r�{����" id="submitbutton" style="font-size:200%">
<input type="reset" value="���Z�b�g">
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
		or printErrorPage("���O�t�@�C�����J���܂���B");
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
<title>�S��RoopeR��</title>
</head>
<title>�V�[�g</title></head>
<body>
<h1>�r�{:$FORM{'scenarioTitle'}</h1>
END
if($FORM{'custom'} eq "6"){
	$FORM{'set'}="First Steps";
}elsif($FORM{'custom'} eq "7"){
	$FORM{'set'}="Basic Tragedy ��";
}elsif($FORM{'custom'} eq "8"){
	$FORM{'set'}="Mystery Circle ��";
}elsif($FORM{'custom'} eq "9"){
	$FORM{'set'}="Haunted Stage ��";
}elsif($FORM{'custom'} eq "10"){#2013.11.07.add
	$FORM{'set'}="Another Horizon";
}else{
	$FORM{'set'}="Basic Tragedy";
}
$FORM{'map1'}="�a�@";
$FORM{'map2'}="�s�s";
$FORM{'map3'}="�_��";
$FORM{'map4'}="�w�Z";

print FILE "<table>";
print FILE qq|<tr><th>�S���Z�b�g</th><td style="border-width:2px;">$FORM{'set'}</td></tr>|;
print FILE "</table>";
print FILE "<table>";
print FILE qq|<tr><th>�g�p�}�b�v</th><td>$FORM{'map1'}</td><td>$FORM{'map2'}</td><td>$FORM{'map3'}</td><td>$FORM{'map4'}</td></tr>|;
print FILE "</table>";

	$FORM{'ruleYadd'} =~ s/&lt;/</g;
	$FORM{'ruleYadd'} =~ s/&gt;/>/g;
	$FORM{'ruleX1add'} =~ s/&lt;/</g;
	$FORM{'ruleX1add'} =~ s/&gt;/>/g;
	$FORM{'ruleX2add'} =~ s/&lt;/</g;
	$FORM{'ruleX2add'} =~ s/&gt;/>/g;
	print FILE <<END;
<table>
<tr><th></th><th></th><th style="width:500px;">�ǉ����[��</th></tr>
<tr><th>���[��Y</th><td>$FORM{'ruleY'}</td><td>$FORM{'ruleYadd'}</td></tr>
<tr><th>���[��X1</th><td>$FORM{'ruleX1'}</td><td>$FORM{'ruleX1add'}</td></tr>
END
if($FORM{'custom'} ne '6'){
	print FILE "<tr><th>���[��X2</th><td>$FORM{'ruleX2'}</td><td>$FORM{'ruleX2add'}</td></tr>";
}
print FILE "<table>";
print FILE "<tr><th>�l��</th><th>��E</th><th>��\�\\��</th><th style='width:500px;'>��E\�\\��</th></tr>";

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
<tr><th>����</th><th>����</th><th style="width:500px;">��������</th><th>�Ɛl</th></tr>
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
<tr><th>���[�v��</th><td id='loop'>$FORM{'loop'}</td><th>�P���[�v����</th><td id='loopday'>$FORM{'loopday'}</td>
END
if($FORM{'usecheck_12'}){
	print FILE "<th>�_�i�o�ꃋ�[�v</th><td id='sinkaku_add_loop'>$FORM{'sinkaku_add_loop'}</td>";
}
print FILE <<END;
</tr>
</table>
<table>
<tr><th style="width:500px;">���ʃ��[��</th></tr>
<tr><td>$FORM{'text'}</td></tr>
</table>
END
#�r�{�Ƃւ̎w�j
$FORM{'sisin'} =~ s/\r//; $FORM{'sisin'} =~ s/\n/<br>/g;$FORM{'sisin'}=~ s|\\n|</p><p>|g;
if(!($FORM{'sisin'} eq "")){
#	$FORM{'sisin'}=~ s|\\n|</p><p>|g;
	print FILE "<table>";
	print FILE qq|<tr><th>�r�{�Ƃւ̎w�j</th></tr><tr><td style="text-align:left;width:600px;"><p>$FORM{'sisin'}</p></td></tr>|;
	print FILE "</table>";
}
	$FORM{"joken1"} =~ s/\r//;
	$FORM{"joken1"} =~ s/\n//;
if(!($FORM{"joken1"} eq "")){print FILE qq|<table><tr><th colspan="2">�r�{�Ƃ̏�������</th></tr>|;}
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
		or printErrorPage("���O�t�@�C�����J���܂���B");
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
		or printErrorPage("���O�t�@�C�����J���܂���B");
	eval{ flock(FILE, 2) };
	print FILE $kaichar;
		close(FILE);

}
#===================================================================================
