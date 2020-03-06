function up_button_enter(id){
	document.getElementById('upButton'+id).className = "btn btn-xs btn-primary";
};

function up_button_leave(id, user_rating){
	if (user_rating != "True"){
		document.getElementById('upButton'+id).className = "btn btn-xs btn-secondary";
	};
};

function down_button_enter(id){
	document.getElementById('downButton'+id).className = "btn btn-xs btn-danger";
};

function down_button_leave(id, user_rating){
	if (user_rating != "False"){
		document.getElementById('downButton'+id).className = "btn btn-xs btn-secondary";
	};
};

function delete_review(){
	if(confirm('Are you sure you want to delete this review?')){
		document.forms["delete-form"].submit();
	};
};