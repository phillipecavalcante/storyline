$(function(){

    searchKeyUp();
  
});

function searchKeyUp() {

    $("#id_search").keyup(function(){
    
        query = $("#id_search").val();
        search(query);
        
	});
    
}

function searchSuccess(data, textStatus, jqXHR){
	$("#results").html(data);
}

function searchTopic(topic){
    
    $("#id_search").val(topic);
        
    search(topic);

}

function sendPage(page){

	data = {
		"page" : page,
		"query": $("#id_search").val(),
		"csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
	}

	send("/", data, searchSuccess);

};


function search(query){

    data = {
            "query": query,
            "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
            }

    send("/", data, searchSuccess);
}