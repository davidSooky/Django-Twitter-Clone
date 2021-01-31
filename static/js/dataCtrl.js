import { fetchPosts, buildPostContent } from "./infiniteScroll.js"
import { container } from "./UICtrl.js"

// Get current profile ID to determine, which posts to fetch for infinite scrolling
const postContainer = document.querySelector("#posts-section");
const currentProfileID = postContainer.dataset.currentprofile;
let range = 10;
let eventRun = false;

loadEventListeners();

function loadEventListeners() {
    const loader = document.querySelector("#loader");
    document.addEventListener("scroll", () => {
        let url;
        const {clientHeight, scrollTop, scrollHeight} = document.documentElement;
        if(clientHeight + scrollTop >=  scrollHeight - 5 && !eventRun) {
            loader.classList.remove("inactive");
            eventRun = true;
            // Check if the current page is the comment page, home page or the profile page, fetch posts accordingly (prevent if comment page)
            if(document.querySelector("#comment-form")) {
                return;
            }
            else if(document.querySelector("#myModal")) {
                url = `http://127.0.0.1:8000/api/user/${currentProfileID}/posts/`;
            } else if(document.querySelector("#post-form")){
                url = `http://127.0.0.1:8000/api/user/${currentProfileID}/followed_posts/`;
            }
            fetchPosts(url, range)
                .then((res) => {
                    range += 10;
                    eventRun = false;
                    // Deactivate loader
                    setTimeout(() => {
                        buildPostContent(res, container);
                        loader.classList.add("inactive");
                    }, 1000);
                });
        }
    });
}

