$('.content').append('<h1>Hello stranger!</h1><h2>Please be patient and wait for our app to load</h2>');    
console.log('loading');
$( document ).ready(function(){
    // jquery datatables
    $('.datatable').DataTable({
        "scrollY":        "400px",
        "scrollCollapse": true,
        "paging":         false
    });
    // Climbing locations - show children
    let showLocations = $('.countries, .regions, .sectors');
    showLocations.on('click', function() {
        $(this).parent().next().children('li').toggle();
    });
    // Posts - show children

});
