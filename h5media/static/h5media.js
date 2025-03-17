
function buttonLink(event){
	let target = $(event.target);
	let tagName = target[0].tagName;
	while( tagName !== 'BUTTON' ){
		target = target.parent();
		tagName = target[0].tagName;
		if( tagName === 'BODY' ){
			return;
		}
	}
	document.location = target.attr('data-href');
}



function documentReady()
{
    $('.button-link').click(buttonLink);
}

$(document).ready(documentReady);
