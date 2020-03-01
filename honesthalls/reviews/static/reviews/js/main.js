function delete_review(){
	if(confirm('Are you sure you want to delete this review?')){
		document.forms["delete-form"].submit();
	}
}
