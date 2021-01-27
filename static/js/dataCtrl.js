import { fetchPosts, buildPostContent } from "./infiniteScroll.js"

const postContainer = document.querySelector(".posts");
const profileID = postContainer.dataset.profile;
let range = 10;
let eventRun = false;

loadEventListeners();

function loadEventListeners() {
    document.addEventListener("scroll", () => {
        let url;
        const {clientHeight, scrollTop, scrollHeight} = document.documentElement;
        if(clientHeight + scrollTop >=  scrollHeight - 5 && !eventRun) {
            eventRun = true;
            // Check if the current page is the home page or the profile page, fetch posts accordingly
            if(document.querySelector("#myModal")) {
                url = `http://127.0.0.1:8000/api/user/${profileID}/posts/`;
            } else {
                url = `http://127.0.0.1:8000/api/user/${profileID}/followed_posts/`;
            }
            fetchPosts(url, range)
                .then((res) => {
                    buildPostContent(res, postContainer);
                    range += 10;
                    eventRun = false;
                });
        }
    });
}

