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
    var refresh = function(name) {
        $.ajax(
            '/sliders/refresh/' +name+ '/'
        ).done(function(data){
            var display = $('.'+name).css('display');
            $('.'+name).replaceWith(data).css('display', display);
            $('.'+name).css('display', display);
        });
    };
    var sentAjax = function(onDone) {
        $.ajax(
            '/sliders/command/'
        ).done(onDone);
    };
    var onDone = function() {
        sentAjax(function(data){
            slide_tab('.'+ data.name, data.speed, onDone);
            $(data.refresh).each(function(index, name){
                refresh(name);
            });
        });
    };
    sentAjax(function(data){
        slide_tab('.'+ data.name, data.speed, onDone);
    });
});
