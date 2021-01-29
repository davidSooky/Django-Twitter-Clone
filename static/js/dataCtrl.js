import { fetchPosts, buildPostContent } from "./infiniteScroll.js"

// Get current profile ID to determine, which posts to fetch for infinite scrolling
const postContainer = document.querySelector("#posts-section");
const container = document.querySelector(".posts");
const currentProfileID = postContainer.dataset.currentprofile;
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
                url = `http://127.0.0.1:8000/api/user/${currentProfileID}/posts/`;
            } else {
                url = `http://127.0.0.1:8000/api/user/${currentProfileID}/followed_posts/`;
            }
            fetchPosts(url, range)
                .then((res) => {
                    buildPostContent(res, container);
                    range += 10;
                    eventRun = false;
                });
        }
    });
}
