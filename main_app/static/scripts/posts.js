const more = function more(event) {
    $(event.target).parent().parent().children("p.description").toggle()
    $(event.target).parent().parent().children("p.description-full").toggle()
}

const modal = function modal() {
    $(".modal").toggle();
    $(".overlay").toggle();


    // console.log($(".modal").css("top"))
    // console.log($(".overlay").css("transform"))
    // if ($(".overlay").css("transform") === "matrix(0, 0, 0, 0, 0, 0)") {
    //     $(".overlay").css("transform", "scale(1)");
    // } else {
    //     $(".overlay").css("transform", "scale(0)");
    // }
}

const login = function login() {
    $(".login").toggle();
    $(".overlay").toggle();
}

const edit = function edit() {
    $(".edit").toggle();
    $(".overlay").toggle();
}

const userUpdate = function userUpdate() {
    $(".user-update").toggle();
    $(".overlay").toggle();
}

const overlay = function overlay() {
    $(".overlay").toggle();
    $(".login").hide();
    $(".modal").hide();
    $(".edit").hide();
}

const message = function message() {
    $(".message").hide();
}

const dropdown = function dropdown() {
    $(".dropdown-content").toggle()
}

$(".more").click(more)