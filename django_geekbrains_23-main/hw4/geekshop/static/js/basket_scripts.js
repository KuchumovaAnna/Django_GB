//window.onload = function{
//    window.onload = function () {
//        $('.basket_table').on('click', 'input[type="number"]', function () {
//            var t_href = event.target;
//            $.ajax({
//                url: "/basket/update/?name=" + t_href.name + "&value=" + t_href.value,
//                success: function (data) {
//                    $('.basket_table').html(data.result);
//                },
//            });
//            event.preventDefault();
//        });
//    }
//}