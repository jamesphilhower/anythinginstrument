$(function() {
    $.ajax({
        url: '/info',
        success: function(data) {
            console.log('get info');
            $('#info').html(JSON.stringify(data, null, '   '));
            $('#description').html(data['description']);
        }
    });
 
    $('#calc').click(function() {
        $('#info').css('display', "none");
        $('#description').css('display', "none");
        $.ajax({
            url : '/calc?a=' + document.getElementById('a').value + '&b=' + document.getElementById('b').value,
            success: function(data) {
                $('#add').html(data['a'] + ' + ' + data['b'] + ' = ' + data['add']);
                $('#subtract').html(data['a'] + ' - ' + data['b'] + ' = ' + data['subtract']);
                $('#multiply').html(data['a'] + ' * ' + data['b'] + ' = ' + data['multiply']);
                $('#divide').html(data['a'] + ' / ' + data['b'] + ' = ' + data['divide']);
            }
        });
    });
})