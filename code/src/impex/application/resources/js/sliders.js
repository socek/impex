var Events = {
    high_scores: function() {
        var data = $.parseJSON($('div.hide.data').html());
        $('.ladder').bracket({
            init: data /* data to initialize the bracket with */
        });
    },
    finals: function() {
        this.high_scores();
    }
};
$(function(){
    slide_tab = function(name, speed, complete) {
        var tabs = $('.tab'),
            tab = $(name),
            body = $("html body");

        tabs.hide();
        tab.show();

        setTimeout(
            function() {
                var document_height = $(document).height(),
                    duration = $(document).height() * speed
                ;
                body.scrollTop(0);
                body.animate(
                    {
                        scrollTop: document_height
                    },
                    {
                        duration: duration,
                        complete: complete
                    }
                );
            },
            100
        );
    };
    var run_event = function(name) {
        if(name in Events) {
            Events[name]();
        };
    };
    var refresh = function(name, next) {
        $.ajaxQueue(
            '/sliders/' +ViewConfig.event_id+ '/refresh/' +name+ '/'
        ).done(function(data){
            var display = $('.'+name).css('display');
            $('.'+name).replaceWith(data).css('display', display);
            $('.'+name).css('display', display);
            next();
        });
    };
    var onFail = function() {
        setTimeout(onDone, 2000);
    };
    var sentAjax = function(onDone) {
        $.ajaxQueue({
            url: '/sliders/command/',
            data: {
                timestamp: ViewConfig.timestamp
            },
        }).done(onDone).fail(onFail);
    };
    var onDone = function() {
        sentAjax(function(data){
            var send_event = function() {
                slide_tab('.'+ name, data.speed, onDone);
                ViewConfig.timestamp = data.timestamp;
                run_event(name);
            };
            var name = data.name;
            var len = data.refresh.length;
            if(len) {
                $(data.refresh).each(function(index, name){
                    if(index == len - 1) {
                        var next = send_event;
                    } else {
                        var next = function(){};
                    }
                    refresh(name, next);
                });
            } else {
                send_event();
            }

        });
    };
    sentAjax(function(data){
        slide_tab('.'+ data.name, data.speed, onDone);
        run_event(data.name);
    });
});
