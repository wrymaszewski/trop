$( document ).ready(function(){
    
    // jquery datatables
    $('.datatable').DataTable({
        "scrollY":        "400px",
        "scrollCollapse": true,
        "paging":         false
    });

    // Climbing locations - show children
    let link = $('a');
    link.on('click', function() {
        $(this).parent().next().children('li').toggle();
    });    
    
});
