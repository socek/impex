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
    var sentAjax = function(onDone) {
        $.ajax(
            '/sliders/command/'
        ).done(onDone);
    };
    var onDone = function(data) {
        sentAjax(function(data){
            slide_tab('.'+ data.name, data.speed, onDone);
        });
    };
    sentAjax(function(data){
        slide_tab('.'+ data.name, data.speed, onDone);
    });
});
