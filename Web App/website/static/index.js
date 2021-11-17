// Delete Note Function
function deleteNote(noteId){
    fetch('/delete-note',{
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/notes";
    });
}

// Delete Disability Function
function deleteDis(disId){
    fetch('/delete-disability',{
        method: 'POST',
        body: JSON.stringify({ disId:disId }),
    }).then((_res) => {
        window.location.href = "/disabilities";
    });
}
