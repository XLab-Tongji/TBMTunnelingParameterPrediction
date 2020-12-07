function showNumberWithAnimation(i, j, randNumber) {
    var numberCell = $('#number-cell-' + i + '-' + j);
    numberCell.css('background-color', getNumberBackgroundColor(randNumber));
    numberCell.css('color', getNumberColor(randNumber));
    numberCell.css('font-size', getNumberFont(randNumber));
    numberCell.text(randNumber);

    numberCell.animate({
        width: "100px",
        height: "100px",
        top: getPosTop(i, j),
        left: getPosLeft(i, j)
    }, 50);
}

function showMoveAnimation(fromx, fromy, tox, toy) {
    var numberCell = $("#number-cell-" + fromx + "-" + fromy);
    numberCell.animate({
        top: getPosTop(tox, toy),
        left: getPosLeft(tox, toy)
    }, 200);
}

//更新分数
function updateScore(score) {
    $("#score").text(score);
}

//提交分数
function AutoSubmit() {
    var all_price = $("#score_submit").val(),
        now_score = $("#score").text(),
        score_num = $("#score_num");

    if (isgameover() || parseFloat(now_score) >= parseFloat(all_price)) {
        score_num.val(parseFloat(now_score)); 
        if (parseFloat(now_score) >= parseFloat(all_price)) {
            $("#alert_message_failure").hide();
            $("#alert_message_success").fadeIn("fast");
            setTimeout(function () { $("#alert_message_success").fadeOut("slow"); }, 600)
        }        
        if (parseFloat(now_score) < parseFloat(all_price)) {
            $("#alert_message_success").hide();
            $("#alert_message_failure").fadeIn("fast");
            setTimeout(function () { $("#alert_message_failure").fadeOut("slow"); }, 600)
        }       
        setTimeout(function () { $("#score_form").submit(); }, 1500);   
    }

}