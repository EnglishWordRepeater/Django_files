$(document).ready(function ($) {

// ___________________________________________________________
// *** Получаю все значения атрибута name eng_word
var arr_eng_w_names = $(".word_field").map(function(indx, element){
  return $(element).attr("name");
}).get();

// Счетчик
var count = arr_eng_w_names.length;


// ___________________________________________________________
// *** Собираю все id-шники, которые есть на странице
function find_all_ids() {

    // Получаю все значения атрибута name eng_word
    var arr_eng_w_names = $(".word_field").map(function(indx, element){
        return $(element).attr("name");
    }).get();
      
    var id_arr = [];
    for (var i = 0; i < arr_eng_w_names.length; i++) {

        if (arr_eng_w_names[i].substr(0, 8) == "word_en_") {
            console.log(+arr_eng_w_names[i].substr(8));
            id_arr.push(+arr_eng_w_names[i].substr(8));
        }
    }

    return id_arr;
}


// ___________________________________________________________
// *** Генерирует уникальный id
function generate_id() {

    var new_id;
    all_ids = find_all_ids();

    do {
        check = true;
        new_id = Math.floor(Math.random() * (333 - 111)) + 111;;

        for (var i = 0; i < all_ids.length; i++) {
            if (new_id == all_ids[i]) {
                check = false;
            }
        }

    } while(!check);

    return new_id;
    
}


// ___________________________________________________________
// *** Генерирую html для элемента
function generate_elem_html(word_id) {
    var html = '<div class="block new_block">\
                        <div class="row">\
                            <div class="col-6">\
                                <div class="word word_en">\
                                    <input type="text" name="word_en_' + word_id + '" class="field word_field" placeholder="Введите слово на английском...">\
                                </div>\
                            </div>\
                            <div class="col-6 word_ru">\
                                <div class="word">\
                                    <input type="text" name="word_ru_' + word_id + '" class="field word_field" placeholder="Введите слово на русском...">\
                                </div>\
                            </div>\
                        </div>\
                    </div>';
    return html;
}


// ___________________________________________________________
// *** Отлавливаю нажатие на мышь и создаю элемент
$('#add_new_word').click(function () {
    $('.work_place .block:last').after(generate_elem_html(generate_id()));
    count++;
    $('#count').attr("value", count - 1);
});
  

// ___________________________________________________________
// *** Обработка AJAX логики
$('#main_work_form :checkbox').change(function() {

    if (this.checked) {

        // Отправляем запрос на сервер и получаем перевод
        $('.new_block').click(function() {
            $(this).find('.word_en').change(function() {

            });
        });

        // Запрещаем ввод перевода до тех пор пока не введен оригинал слова на английском
    } 

});




// ___________________________________________________________
// *** Эксперементы с AJAX 
$('#test_ajax').click(function() {

    var word = "HELLO!";

    var request = $.ajax({
        url: "script.php",
        type: "POST",
        data: {id : word},
        dataType: "html"
    });
    
    request.done(function(msg) {
        alert(msg);
    });
    
    request.fail(function(jqXHR, textStatus) {
        alert( "Request failed: " + textStatus );
    });
    

});
  
});
  
  
  