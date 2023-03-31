
$(document).ready(function(){
    $("#btnSearch").click(function(){
        $(this).prop("disabled", true);
        $(this).html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Gathering Data...`
      );
    });
});

$(document).ready(function(){
    $(".btnUpdate").click(function(){
        $('#btnSearch').prop("disabled", true);
        $('#btnSearch').html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Gathering Data...`
      );
    });
});

$(document).on('show.bs.modal', '#confirmDelete', function(e){
    const myvar = $(e.relatedTarget).attr('data-bs-delete-url');
    $('#delete-button').attr('href', myvar);
});



