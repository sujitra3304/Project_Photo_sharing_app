const likeButton = document.querySelector('#like-button');


function like() {

    const likeCount = document.querySelectorAll('#likes-count');
    // const likeButton = document.querySelectorAll('#like-button');
    locationPath = window.location.pathname.split("/");
    photoId=parseInt(locationPath[2])
    
    fetch(`/like/${photoId}`, { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];
        
        if (data["liked"] === "True") {
          likeButton.className = "fas fa-thumbs-up";
        } else {
          likeButton.className = "far fa-thumbs-up";
        }
      })
  }
 if (likeButton) {
     likeButton.addEventListener('click',like);
 }


const deletePhotoBtn = document.querySelector('#delete-photo')

function deletePhoto() {
    locationPath = window.location.pathname.split("/");
    photoId=parseInt(locationPath[2])

    fetch(`/delete_photo/${photoId}`, { method: "POST" })
      .then((response) => response.text())
      .then((data) => {
        window.location.href = "http://localhost:5000";
})
}

if (deletePhotoBtn) {
    deletePhotoBtn.addEventListener('click',deletePhoto);
} 

const deleteCommentBtns = document.querySelectorAll("[id^='delete-comment']")
for (const deleteCommentBtn of deleteCommentBtns){
    
    deleteCommentBtn.addEventListener('click', deleteComment)

}


function deleteComment(evt) {
    getCommentId = evt.target.id.split("-");
    commentId=getCommentId[2];

    fetch(`/delete_comment/${commentId}`, { method: "POST" })
      .then((response) => response.text())
      .then((data) => {
        window.location.reload() ;
})
}



function followUser (evt) {
  const followBtnsStatuses = document.querySelectorAll(".followBtnStatus")
  getFollowingUser = evt.target.id.split("-");
  FollowingUserId = getFollowingUser[2];
  
  fetch(`/follow/${FollowingUserId}`, { method: "POST" })
  .then((response) => response.json())
  .then((data) => {
       
        if (data["followed"] === true) {
          for (const followBtnStatus of followBtnsStatuses)

          followBtnStatus.className = "fa-solid fa-user-minus"          
        } 
        else 
        {
          for (const followBtnStatus of followBtnsStatuses)
          followBtnStatus.className = "fa-solid fa-user-plus";
          
        }
        
      })

}
const followBtns = document.querySelectorAll("[id^='follow-btn']")

for (const followBtn of followBtns){
    
  followBtn.addEventListener('click', followUser)

}