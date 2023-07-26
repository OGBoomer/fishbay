
/*
$(document).ready(function(){
    $("#btnSearch").click(function(e){
        e.preventDefault()
        $('#btnSearch').prop("disabled", true);
        $('#btnSearch').html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Gathering Data...`
        );
        $('#frmSearch').submit();
    });
});


$(document).ready(function(){
    $(".btnUpdate").click(function(e){
        $('#btnSearch').prop("disabled", true);
        $('#btnSearch').html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Gathering Data...`
      );
    });
});

$(document).ready(function(){
    sizeSelector();
    $('.sizeType').change(function(){
        sizeSelector();
    });
});

function sizeSelector(){
    var sizeType = $('.sizeType option:selected').text();
    if (sizeType == 'Big and Tall') {
            $('.size').hide().val("");
            $('.btsize').show();
        } else {
            $('.size').show();
            $('.btsize').hide().val("");
        }
};

$(document).on('show.bs.modal', '#confirmDelete', function(e){
    const myvar = $(e.relatedTarget).attr('data-bs-delete-url');
    $('#delete-button').attr('href', myvar);
});
*/
$(document).ready(function(){
    $("#id_size").focus(function(){
        $(this).select();
        $(this).css('background-color', 'yellow');
    });
});






