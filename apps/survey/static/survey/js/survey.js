
$(function(){

    sortStory();

});

function sortStory(){
	$( "#storyline, #extra").sortable({
	      connectWith: ".sortable",
	      placeholder: "ui-state-highlight",
	      cancel: ".ui-state-disabled",
	      items: 'li:not(.ui-state-disabled)',
	    }).disableSelection();

}


function getUserStory(){

    
    
    sorting = $("ul#storyline").sortable("toArray").toString();
    first = $("ul#storyline li.first").attr("id");
    userstory = first + "," + sorting;
    
    data = {
            'userstory' : userstory
            }
    
    $("input[name=userstory]").val(userstory);
    
}
