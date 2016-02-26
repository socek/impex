var Events = {
    high_scores: function() {
        var data = $.parseJSON($('div.hide.data').html());
        $('.ladder').bracket({
            init: data /* data to initialize the bracket with */
        });
    },
    finals: function() {
        this.high_scores();
        $('.tab.finals .game:first').css('margin-top', '260px');
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
    var refresh = function(name) {
        $.ajax(
            '/sliders/' +ViewConfig.event_id+ '/refresh/' +name+ '/'
        ).done(function(data){
            var display = $('.'+name).css('display');
            $('.'+name).replaceWith(data).css('display', display);
            $('.'+name).css('display', display);
        });
    };
    var onFail = function() {
        setTimeout(onDone, 2000);
    };
    var sentAjax = function(onDone) {
        $.ajax({
            url: '/sliders/command/',
            data: {
                timestamp: ViewConfig.timestamp
            },
        }).done(onDone).fail(onFail);
    };
    var onDone = function() {
        sentAjax(function(data){
            var name = data.name;
            slide_tab('.'+ name, data.speed, onDone);
            $(data.refresh).each(function(index, name){
                refresh(name);
            });
            ViewConfig.timestamp = data.timestamp;
            run_event(name);
        });
    };
    sentAjax(function(data){
        slide_tab('.'+ data.name, data.speed, onDone);
        run_event(data.name);
    });
});
