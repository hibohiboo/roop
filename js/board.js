//場所設定-----------------------------------
function positionSet(board){
	for(var i=0;i<board.length;i++){
		board[i].space=new Array();
		for(var j=0;j<charlist.length;j++){
			board[i].space=0;
		}
		board[i].x=board[0].x-(-i*40);
		board[i].y=board[0].y;
		if(i>3){
			board[i].y-=(-55);
			board[i].x-=160;
		}
	}
}

