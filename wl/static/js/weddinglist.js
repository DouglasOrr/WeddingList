$(function() {
    // Clock
    var secondsRemaining = Math.max(0, (new Date("2017-11-11T11:30") - new Date()) / 1000);
    $('.countdown').FlipClock(secondsRemaining, {
        clockFace: 'DailyCounter',
        countdown: true,
        showSeconds: false
    });

    // List of items
    function show(table, items) {
        $(table).find('tbody').empty();
        $.each(items, function(_, item) {
            var img = '<img class="img-thumbnail"' +
                ' src="/static/lib/img/' + item.id + '/thumb.jpg"'
                ' />';
            var row = $('<tr>' +
                        '<td class="td-img">' + img + '</td>' +
                        '<td><h2>' + item.title + '</h2></td>' +
                        '</tr>');
            if (table.dataset.listQuery == 'claimed-by') {
                var unclaimUrl = "/unclaim/" + encodeURIComponent(table.dataset.listQueryEmail) + "/" + item.id;
                var unclaim = $('<form action="' + unclaimUrl + '" method="POST"><button class="btn btn-danger">Unreserve!</button></form>');
                $('<td></td>').append(unclaim).appendTo(row);
            }
            row.click(function() {
                window.location = '/detail/' + item.id;
            });
            $(table).find('tbody').append(row);
        });
    }
    function filter(items, query) {
        // Empty query
        if (query.trim() === '') {
            return items;
        }
        // Build a list of patterns
        var ftokens = query.trim().split(' ');
        var fexp = [];
        $.each(ftokens, function(i, token) {
            fexp.push(new RegExp('\\b' + token + (i + 1 < ftokens.length ? '\\b' : ''), 'i'));
        });
        // Find items that match all patterns
        var fitems = [];
        $.each(items, function(_, item) {
            var match = true;
            $.each(fexp, function (_, exp) {
                match &= exp.test(item.title);
            });
            if (match) {
                fitems.push(item);
            }
        });
        return fitems;
    }
    $('.list-main').each(function (_, table) {
        var query;
        if (table.dataset.listQuery == 'unclaimed') {
            query = '/item/unclaimed';
        } else if (table.dataset.listQuery == 'claimed-by') {
            query = '/item/claimed_by/' + encodeURIComponent(table.dataset.listQueryEmail);
        }
        $.ajax(query)
            .done(function (items) {
                show(table, items);
                $('.list-filter').keyup(function (e) {
                    show(table, filter(items, e.target.value));
                });
            });
    });

    // Validation - form text & email must not be empty
    $('input:text,input[name="email"]').keyup(function() {
        $('form button').attr(
            'disabled',
            $('input:text,input[name="email"]').is(
                function (_, e) { return e.value.length == 0 }))
    });
});
