
$(function(){

    sortStory();
  
});

function sortStory(){
	$( "#storyline" ).sortable({
	      //connectWith: ".sortable",
	      placeholder: "ui-state-highlight",
	      cancel: ".ui-state-disabled",
	      items: 'li.media:not(.ui-state-disabled)',
	    }).disableSelection();
}
