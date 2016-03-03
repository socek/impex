$(function(){
    $('input[type=text].quart').change(function(){
        var count_for_quart = function (team, number) {
            var result = 0;
            for(var loop=0; loop<number; loop++) {
                var value = parseInt($('input[name='+ team +'_quart_' + (loop + 1) +']').val());
                if(isNaN(value)){
                    return null;
                }
                result += value;
            }
            if(value <= 0){
                return 0;
            }
            return result;
        };
        var set_value = function(key, value) {
            var name = 'input[name='+ key +']';
            if(value) {
                $(name).val(value);
            } else {
                $(name).val('0');
            }
        };
        set_value('left_quart_2_sum', count_for_quart('left', 2));
        set_value('left_quart_3_sum', count_for_quart('left', 3));
        set_value('left_quart_4_sum', count_for_quart('left', 4));
        set_value('right_quart_2_sum', count_for_quart('right', 2));
        set_value('right_quart_3_sum', count_for_quart('right', 3));
        set_value('right_quart_4_sum', count_for_quart('right', 4));
    });
    $('input[type=text].quart').change();
    $('input[type=text].sum').change(function(){
        var get_value_for = function(key) {
            return parseInt($('input[name='+ key + ']').val());
        };
        var set_value = function(key, value) {
            if(isNaN(value)) {
                return;
            }
            $('input[name='+ key +']').val(value);
        };
        set_value(
            'left_quart_2',
            get_value_for('left_quart_2_sum') - get_value_for('left_quart_1')
        );
        set_value(
            'left_quart_3',
            get_value_for('left_quart_3_sum') - get_value_for('left_quart_2_sum')
        );
        set_value(
            'left_quart_4',
            get_value_for('left_quart_4_sum') - get_value_for('left_quart_3_sum')
        );
        set_value(
            'right_quart_2',
            get_value_for('right_quart_2_sum') - get_value_for('right_quart_1')
        );
        set_value(
            'right_quart_3',
            get_value_for('right_quart_3_sum') - get_value_for('right_quart_2_sum')
        );
        set_value(
            'right_quart_4',
            get_value_for('right_quart_4_sum') - get_value_for('right_quart_3_sum')
        );
    });
});
