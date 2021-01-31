export const container = document.querySelector(".posts");
const followBtn = document.querySelectorAll("#main-btn-follow");

loadEventListeners();

// Funtion to load all eventlisteners
function loadEventListeners() {
    container.addEventListener("click", (e) => {
        manageLikes(e);
    });
    document.addEventListener("scroll", btnHandling);
    if(followBtn){
        followBtn.forEach((btn) =>{
            btn.addEventListener("click", e => {
                manageFollowers(e);
            });
        });
    }
    container.addEventListener("click", (e) => {
        showDeletePost(e);
    });
    document.body.addEventListener("click", (e) => {hideDeletePost(e);});
}

// If user want to delete the post, show the button
const showDeletePost = (e) => {
    const userID = container.dataset.profile;
    if (e.target.classList.contains("fa-ellipsis-h")) {
        const ownerID = e.target.parentElement.parentElement.parentElement.lastElementChild.dataset.owner;
        if(userID == ownerID) {
            e.target.parentElement.nextElementSibling.classList.add("show");
        }
    }
};

// Hide post delete, button
const hideDeletePost = (e) => {
    if (!e.target.classList.contains("fa-ellipsis-h")) {
        const deletePost = document.querySelector(".delete-post.show");
        if(deletePost) {
            deletePost.classList.remove("show");
        }
    }
};

// Function for managing likes, creates or deletes Like model object. Updates UI.
const manageLikes = (e) => {
    const parent = e.target.parentElement;
    const postID = parent.parentElement.dataset.id;
    const ownerID = parent.parentElement.dataset.owner;
    const profileID = container.dataset.profile;
    const numOfLikes = e.target.dataset.number ?parseInt(e.target.dataset.number) :0;
    let url;

    // Check if user is going to like his own post, prevent it if True
    if(profileID !== ownerID) {
        // Post is not liked yet, like it
        if(e.target.classList.contains("fa-heart") && e.target.classList.contains("far")) {
            e.preventDefault();
            url = "http://127.0.0.1:8000/api/likes/create/";
            createLike(url , profileID, postID)
                .then(() => {parent.innerHTML = `<i class="fas fa-heart clear flex-row liked" data-number="${numOfLikes + 1}"></i>`});
        } else if (e.target.classList.contains("fa-heart") && e.target.classList.contains("fas")) {
            // Post is liked already, unlike it
            e.preventDefault();
            url = `http://127.0.0.1:8000/api/likes/delete/${postID}`;
            deleteObject(url)
                .then(() => {parent.innerHTML = `<i class="far fa-heart clear flex-row" data-number="${numOfLikes - 1 !== 0 ?numOfLikes - 1 :""}"></i>`});
        }
    } else if(e.target.classList.contains("fa-heart")){e.preventDefault();}
};

// Function for managing followers, creates or deletes Follower model object. Updates UI.
const manageFollowers = (e) => {
    // Define variables
    const userInfo = document.querySelector(".user-info");
    const followCounter = userInfo.querySelector(".followers").firstElementChild;
    const followingCount = parseInt(followCounter.textContent);
    const userID = container.dataset.profile
    const profileID = userInfo.dataset.id;
    let url;

    // Follow user
    if(e.target.textContent === "Follow") {
        e.preventDefault();
        url = "http://127.0.0.1:8000/api/follower/create/";
        createFollower(url, userID, profileID)
            .then(() => {
                // Update UI (increase number of followed people, change text of follow button)
                followCounter.textContent = followingCount + 1;
                followBtn.forEach(btn => {btn.textContent = "Unfollow";});
            });
    } else {
        // Unfollow user
        e.preventDefault();
        url = url = `http://127.0.0.1:8000/api/follower/delete/${profileID}`;
        deleteObject(url)
            .then(() => {
                // Update UI (decrease number of followed people, change text of follow button)
                followCounter.textContent = followingCount - 1;
                followBtn.forEach(btn => {btn.textContent = "Follow";});
            });
    }
}

// Asynchronous funtion to create Like object
const createLike = async (url, owner_id, post_id) => {
    await fetch(url, {
        method: "POST",
        headers: {
            "Content-type":"application/json",
            "X-CSRFToken":getCookie('csrftoken')
        },
        body: JSON.stringify({
            owner: owner_id,
            post: post_id,
        })
    });
};

// Asynchronous funtion to create Follower object
export const createFollower = async (url, id_1, id_2) => {
    await fetch(url, {
        method: "POST",
        headers: {
            "Content-type":"application/json",
            "X-CSRFToken":getCookie('csrftoken')
        },
        body: JSON.stringify({
            owner_id: id_1,
            follower_id: id_2,
        })
    });
};

// Asynchronous funtion to delete Like object or Follower object
export const deleteObject = async (url) => {
    await fetch(url, {
        method: "DELETE",
        headers: {
            "Content-type":"application/json",
            "X-CSRFToken":getCookie('csrftoken')
        }
    });
};

// Function to hide/unhide follow/unfollow button in header section of a profile
function btnHandling() {
    // On same pages these buttons are not defined
    try {
        const userID = container.dataset.profile;
        const currentProfileID = document.querySelector(".post-actions").dataset.owner;

        if(userID !== currentProfileID) {
            const header = document.querySelector(".posts-header");
            const topBtn = document.querySelector(".btn-follow.top");
            const bottomBtn = document.querySelector(".btn-follow.bottom");
            const position = bottomBtn.getBoundingClientRect().bottom;
            const height = header.offsetHeight;

            if(position < height) {
                topBtn.classList.add("active");
            } else {
                topBtn.classList.remove("active");
            }
        }
    } catch{return}
}

// Function to get csrf_token for asynchronous tasks
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}