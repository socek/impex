$(function(){
    $('.filters button').click(function(event){
        var self = $(event.target),
            type = self.data('type');

        var is_active = function(item) {
            return item.hasClass(item.data('class'))
        };
        var active = function(item) {
            item.addClass(item.data('class'));
        };
        var unactive = function(item) {
            item.removeClass(item.data('class'));
        };

        var is_all = function() {
            var allbutton = $('.filters button.all');
            return is_active(allbutton);
        };
        var switch_buttons = function() {
            if(type == 'all') {
                if(is_active(self)) {
                    unactive(self);
                } else {
                    $('.filters button').each(function(index, item){
                        var item = $(item);
                        item.addClass(item.data('class'));
                    });
                }
            } else {
                if(is_active(self)) {
                    unactive(self);
                    unactive($('.filters button.all'));
                } else {
                    active(self);
                }
            }
        };
        var filter = function() {
            if(is_all()) {
                console.log('show');
                $('.well.scoreboard').show();
                $('.well.game').show();
            }
            else {
                console.log('hide');
                $('.well.scoreboard').hide();
                $('.well.game').hide();
            }
            $('.filters button:not(.all)').each(function(index, item){
                var item = $(item);
                var type = item.data('type');
                var cls = item.data('class');
                console.log('a',item);
                if(item.hasClass(cls)) {
                    console.log('.well.game.'+type);
                    $('.well.game.'+type).show();
                }
            });

        };

        switch_buttons();
        filter();
    });
});
