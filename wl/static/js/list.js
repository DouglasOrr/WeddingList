$(function() {
    $.ajax('/item')
        .done(function (items) {
            $.each(items, function(_, item) {
                var img = '<img class="img-thumbnail"' +
                    ' src="/static/lib/img/' + item.path +
                    '" />';
                var row = $('<tr>' +
                            '<td class="td-img">' + img + '</td>' +
                            '<td><h2>' + item.title + '</h2></td>' +
                            '</tr>');
                $(".listbody").append(row);
                row.click(function() {
                    window.location = '/detail/' + item.id;
                });
            });
        });
});
