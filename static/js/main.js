function showComment(){
    var commentArea = document.getElementById("comment-area");
    commentArea.classList.remove("hide");
}

//Reply
function showReplies(id){
    var replyArea = document.getElementById(id);
    replyArea.classList.remove("hide");
}