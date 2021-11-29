const more = function more(event) {
    $(event.target).parent().parent().children("p.description").toggle()
    $(event.target).parent().parent().children("p.description-full").toggle()
}

const modal = function modal() {
    $(".modal").toggle();
}

const edit = function edit() {
    $(".edit").toggle();
}

const message = function message() {
    $(".message").hide();
}

$(".more").click(more)