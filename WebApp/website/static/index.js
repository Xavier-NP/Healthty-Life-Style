// Delete Note Function
function deleteNote(noteId){
    fetch('/delete-note',{
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/diary";
    });
}

// Delete Disability Function
function deleteFall(fallId){
    fetch('/delete-fall',{
        method: 'POST',
        body: JSON.stringify({ fallId: fallId }),
    }).then((_res) => {
        window.location.href = "/accidents";
    });
}
