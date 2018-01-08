$("#lock_modal").on("shown.bs.modal", function(e) {
    var button = $(e.relatedTarget);
    var url = button.data('url');
    document.querySelector('#lock-confirm').href = `/lock/${url}`;
})


$("#unlock_modal").on("shown.bs.modal", function (e) {
    var button = $(e.relatedTarget);
    var url = button.data('url');
    document.querySelector('#unlock-confirm').href = `/unlock/${url}`;
})
