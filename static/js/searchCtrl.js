import { fetchPosts, buildSearchResults } from "./infiniteScroll.js"

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