$(document).ready(function () {
// 动态查询，并显示相近的5个批次号;
    $('input#batch').keyup(function () {
        console.log('456');
        var batch = $('input#batch').val();
        $.ajax({
            url: "/search_batch/",
            type: "GET",
            dataType: 'json',
            data: {'batch': batch},
            async: false,
            success: function (arg) {
                console.log(arg);
                $('datalist#batch_list').empty();
                for (var i = 0; i < arg.length; i++) {
                    var add_options = '<option value="' + arg[i] + '">' + arg[i] + '</option>';
                    $('datalist#batch_list').append(add_options);
                }
            }
        })
    });
})
//动态加载款式
$(document).ready(function () {
    $('input#batchs').change(function change_style() {
        var kj = $('#batch').val();
        console.log('454');
        $.ajax({
            url: "/change_style/",
            type: "GET",
            dataType: 'json',
            data: {'batch': kj},
            async: true,
            success: function (arg) {
                console.log(arg)
                if (arg['errs'] == '') {
                    $('span#batch_err').empty();
                    $('#style_coding').children().remove();
                    for (var i = 0; i < arg['style_coding_list'].length; i++) {
                        var add_options = '<option value="' + arg['style_coding_list'][i] + '">' + arg['style_coding_list'][i] + '</option>';
                        $('#style_coding').append(add_options);
                        $('#search').attr('type', 'submit');
                    }
                }
                else {
                    $('span#batch_err').empty();
                    $('span#batch_err').append(arg['errs']);
                    $('#style_coding').children().remove();
                    $('#search').attr('type', 'button');
                }
            }
        })
    });
})