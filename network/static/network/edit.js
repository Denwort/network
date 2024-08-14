document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelectorAll('.edit-post-button').forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        const postId = this.dataset.postId;
        const postDiv = document.getElementById(`post-${postId}`);
        const contentText = postDiv.querySelector('.content-text');
        const editTextarea = postDiv.querySelector('.edit-textarea');
        const saveButton = postDiv.querySelector('.save-post-button');
        const editButton = postDiv.querySelector('.edit-post-button');
        
        // Toggle visibility
        contentText.style.display = 'none';
        editTextarea.style.display = 'block';
        saveButton.style.display = 'inline';
        editButton.style.display = 'none';
      });
    });
  
    document.querySelectorAll('.save-post-button').forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        const postId = this.dataset.postId;
        const postDiv = document.getElementById(`post-${postId}`);
        const editTextarea = postDiv.querySelector('.edit-textarea');
        const contentText = postDiv.querySelector('.content-text');
        const saveButton = postDiv.querySelector('.save-post-button');
        const editButton = postDiv.querySelector('.edit-post-button');
        
        const editedContent = editTextarea.value;
        
        fetch(`/edit_post/${postId}`, {
          method: 'POST',
          body: JSON.stringify({ 
            content: editedContent 
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            contentText.textContent = editedContent;
            contentText.style.display = 'block';
            editTextarea.style.display = 'none';
            saveButton.style.display = 'none';
            editButton.style.display = 'inline';
          } else {
            alert('Failed to save the post.');
          }
        });
      });
    });

});