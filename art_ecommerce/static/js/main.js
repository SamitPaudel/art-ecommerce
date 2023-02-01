function showComment(){
    var commentArea = document.getElementById('comment-area');
    var cmtButton = document.getElementById('comment-btn')
    console.log(commentArea);
    console.log(cmtButton)
    if (commentArea.hasAttribute("hidden")) {
        cmtButton.innerHTML = 'Hide'
        commentArea.removeAttribute("hidden");
    } else {
          cmtButton.innerHTML = 'Comment'
        commentArea.setAttribute("hidden", "");
      }
}

function showReply(){
    var commentArea = document.getElementById('reply-area');
    var replyButton = document.getElementById('reply-btn')
    console.log(commentArea);
    console.log(replyButton)
    if (commentArea.hasAttribute("hidden")) {
        replyButton.innerHTML = 'Hide'
        commentArea.removeAttribute("hidden");
    } else {
        replyButton.innerHTML = 'Reply'
        commentArea.setAttribute("hidden", "");
      }
}