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
                $('.well.scoreboard').show();
                $('.well.game').show();
            }
            else {
                $('.well.scoreboard').hide();
                $('.well.game').hide();
            }
            $('.filters button:not(.all)').each(function(index, item){
                var item = $(item);
                var type = item.data('type');
                var cls = item.data('class');
                if(item.hasClass(cls)) {
                    $('.well.game.'+type).show();
                }
            });
        };

        switch_buttons();
        filter();
    });

    var ladder = function() {
        var data = $.parseJSON($('div.hide.data').html());
        $('.ladder').bracket({
            init: data /* data to initialize the bracket with */
        });
    };
    ladder();
});
