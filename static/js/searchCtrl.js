import { fetchPosts, buildSearchResults } from "./infiniteScroll.js"
import { createFollower, deleteObject, container } from "./UIControl.js"

const searchField = document.querySelector(".search-input");

searchField.addEventListener("keyup", (e) => {
    buildContent(e.target.value)
});

function buildContent(searchInput) {
    const resultsCont = document.querySelector(".results");
    let url = "http://127.0.0.1:8000/api/user/";

    if(searchInput.replace(/\s+/g,'') != "") {
        fetchPosts(url)
        .then((result) => {
            buildSearchResults(result, resultsCont, searchInput);
        });
    } else {
        resultsCont.innerHTML = "Try searching for people.";
    }
}

const followBtn = document.querySelector(".card").querySelectorAll(".btn-follow");
const userID = container.dataset.profile;
followBtn.forEach(item => {
    item.addEventListener("click", (e) => {
        const profileID = e.target.parentElement.dataset.profile;
        let url;
        // Follow user
        if(e.target.textContent === "Follow") {
            e.preventDefault();
            url = "http://127.0.0.1:8000/api/follower/create/";
            createFollower(url, userID, profileID)
                .then(() => {
                    // Update UI (change text of follow button)
                    e.target.textContent = "Unfollow";
                });
        } else {
            // Unfollow user
            e.preventDefault();
            url = url = `http://127.0.0.1:8000/api/follower/delete/${profileID}`;
            deleteObject(url)
                .then(() => {
                    // Update UI (change text of follow button)
                    e.target.textContent = "Follow";
                });
        }
    })
});