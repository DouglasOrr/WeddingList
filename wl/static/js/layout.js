$(function() {
    var secondsRemaining = Math.max(0, (new Date("2017-11-11T11:30") - new Date()) / 1000);
    $('.countdown').FlipClock(secondsRemaining, {
        clockFace: 'DailyCounter',
        countdown: true,
        showSeconds: false
    });
});
