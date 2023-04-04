function showComment(commentId) {
    var commentArea = document.querySelector('.comment-area');
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
    commentArea.classList.remove("hide");
}

function toggleComment(commentId) {
    var commentArea = document.getElementById(commentId);
    var button = document.getElementById('comment-btn');
    if (commentArea.style.display === 'none') {
        commentArea.style.display = 'block';
        button.innerHTML = 'Hide';
    } else {
        commentArea.style.display = 'none';
        button.innerHTML = 'Comment';
    }
}

//Reply
function showReply() {
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