document.addEventListener('dblclick',handleDblClick);
deleteButtons.forEach(i => {i.addEventListener('click',handleDeleteClick)});

function handleDblClick(e){
    console.log(e.target.tagName)
    if(e.target.tagName=="INPUT"){e.target.disabled = !e.target.disabled}
}



{/* <label>Injuries:  <input name="injuries" class="injuries" type="text" disabled="true" value="<%= actor.injuries %>"></label> */}


<form class="actorDetails" method="POST" action="/actors/<%= actor._id %>?_method=PUT"></form>