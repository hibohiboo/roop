#!/usr/bin/perl --

$fdata = './dat/save.dat'; #�t�H�[���f�[�^�ۑ���

#�t�H�[���f�[�^�̎擾
if($ENV{'REQUEST_METHOD'} eq 'POST'){
	read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
}else {
	$query = $ENV{'QUERY_STRING'};
}
#�t�@�C���ւ̏�������
open(FILE, ">$fdata") or die("�G���[�F�t�@�C�����J���܂���");
eval { flock(FILE,2); }; #�t�@�C�����b�N
print FILE $query;
close(FILE);

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

