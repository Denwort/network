document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.like-button').forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default button behavior

        const postId = this.dataset.postId;
        const postDiv = document.getElementById(`post-${postId}`);
        const likeCountSpan = postDiv.querySelector('.like-count');
        const buttonAction = postDiv.querySelector('svg');
        const action = buttonAction.getAttribute('fill') === '#ffffff' ? 'like' : 'unlike';

        fetch(`/like_post/${postId}/${action}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
            likeCountSpan.textContent = data.like_count;
            buttonAction.setAttribute('fill', buttonAction.getAttribute('fill')=== '#ffffff' ? '#ff0000' : '#ffffff') ;
            } else {
            alert('Failed to update like status.');
            }
        });
      });
    });

});