var up_button_set = {};
var down_button_set = {};
var user_rating_changed = {};

function up_button_enter(id){
	if(document.getElementById('upButton'+id).disabled == false){
		document.getElementById('upButton'+id).className = "btn btn-xs btn-primary";
	};
};

function up_button_leave(id, user_rating){
	if ((user_rating != "True" | user_rating_changed[id] == true) & 
										up_button_set[id] == false){
		if(document.getElementById('upButton'+id).disabled == false){
			document.getElementById('upButton'+id).className = "btn btn-xs btn-secondary";
		};
	};
};

function down_button_enter(id){
	if(document.getElementById('upButton'+id).disabled == false){
		document.getElementById('downButton'+id).className = "btn btn-xs btn-danger";
	};
};

function down_button_leave(id, user_rating){
	if ((user_rating != "False"| user_rating_changed[id] == true) & 
										down_button_set[id] == false){
		if(document.getElementById('upButton'+id).disabled == false){
			document.getElementById('downButton'+id).className = "btn btn-xs btn-secondary";
		};
	};
};

function delete_review(){
	if(confirm('Are you sure you want to delete this review?')){
		document.forms["delete-form"].submit();
	};
};

function on_body_load(review_ids_list){
	var review_ids = JSON.parse(review_ids_list);
	for(var i = 0; i < review_ids.length; i++){
		var id = review_ids[i];
		$('#upButton'+id).click(generate_handler_up(id));
		$('#downButton'+id).click(generate_handler_down(id))
		up_button_set[id] = false;
		down_button_set[id] = false;
		user_rating_changed[id] = false;
	};
};

function generate_handler_up(review_id) {
    return function(event) { 
        var url = (window.location.href) + "/" + review_id + "/up";
        var newrequest = new XMLHttpRequest();
        newrequest.open("GET", url)
        newrequest.onload = function(){
        	var data = JSON.parse(newrequest.responseText)
        	if (!data['logged_in']){
        		location.replace(data['url'])
        	}
        	else{
        		user_rating_changed[review_id] = true;
        		document.getElementById('rating'+ review_id).innerHTML=data['rating'];
        		if(data['highlight_up']){
        			up_button_set[review_id] = true;
        			document.getElementById('upButton'+review_id).className = "btn btn-xs btn-primary";
        		}
        		else{
        			up_button_set[review_id] = false;
        			document.getElementById('upButton'+review_id).className = "btn btn-xs btn-secondary";
        		}
        		if(!data['highlight_down']){
        			down_button_set[review_id] = false;
        			document.getElementById('downButton'+review_id).className = "btn btn-xs btn-secondary";
        		}
        	}
        }
        newrequest.send()
    };
};

function generate_handler_down(review_id) {
    return function(event) { 
        var url = (window.location.href) + "/" + review_id + "/down";
        var newrequest = new XMLHttpRequest();
        newrequest.open("GET", url)
        newrequest.onload = function(){
        	var data = JSON.parse(newrequest.responseText)
        	if (!data['logged_in']){
        		location.replace(data['url'])
        	}
        	else{
        		user_rating_changed[review_id] = true;
        		document.getElementById('rating'+ review_id).innerHTML=data['rating'];
        		if(data['highlight_down']){
        			down_button_set[review_id] = true;
        			document.getElementById('downButton'+review_id).className = "btn btn-xs btn-danger";
        		}
        		else{
        			down_button_set[review_id] = false;
        			document.getElementById('downButton'+review_id).className = "btn btn-xs btn-secondary";
        		}
        		if(!data['highlight_up']){
        			up_button_set[review_id] = false;
        			document.getElementById('upButton'+review_id).className = "btn btn-xs btn-secondary";
        		}
        	}
        }
        newrequest.send()
    };
};

