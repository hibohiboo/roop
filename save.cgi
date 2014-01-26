#!/usr/bin/perl --

$fdata = './dat/save.dat'; #フォームデータ保存先

#フォームデータの取得
if($ENV{'REQUEST_METHOD'} eq 'POST'){
	read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
}else {
	$query = $ENV{'QUERY_STRING'};
}
#ファイルへの書き込み
open(FILE, ">$fdata") or die("エラー：ファイルが開けません");
eval { flock(FILE,2); }; #ファイルロック
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

