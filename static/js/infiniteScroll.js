import { container } from "./UIControl.js"
const profileID = container.dataset.profile;

// Function to get posts asynchronously
export async function fetchPosts(url, range = null) {
    const data = await (await fetch(url)).json();
    if(range) {
        return data.slice(range, range + 10);
    }
    return data
};

// Format posts date of creation, since Django template filters can not be passed by Javascript
function formatDate(date) {
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    const dateObj = new Date(date);
    const month = monthNames[dateObj.getUTCMonth()].slice(0, 3); 
    const day = dateObj.getUTCDate();
    const year = dateObj.getUTCFullYear();

    return month + " " + day + ", " + year;
}

// Function to rebuild the HTML of the post container
export function buildPostContent(data, container) {
    let html = "";
    // Loop through each post(returned by the API), use the data for building the UI
    data.map(item => {
        if(item) {
            html += `
            <div class="post-container">
                <div class="user-photo"><a href="${item.profile.profile_pic}"></a><img src="${item.profile.profile_pic}" alt="Not found"></a></div>
                <div class="post-card">
                <div class="post-title"><a href="${item.profile.absolute_url}"><strong>${item.profile.first_name} ${item.profile.last_name}
                </strong></a><span> @${item.profile.username} · ${formatDate(item.created_on)}<i class="fas fa-ellipsis-h flex-row"></i></span>`;
                
                if (profileID == item.owner) {
                    html += `<a href="/tweet/post/${item.id}/delete" class="delete-post">Delete post ?</a>`;
                }
                
                html += `</div>`;
                // Check if title is not null, otherwise do not show it
                if(parseInt(item.title) != 0) {
                    html += `<div class="post-title mt-1">${item.title}</div>`;
                } 

                if(item.content) {
                html += `<div class="post-content">${item.content}</div>`  
                }

                html += `<div class="post-actions" data-id="${item.id}" data-owner="${item.owner}"">`;
                // Check of number of comments is not null, otherwise do not show it
                if(item.num_of_comments) {
                    html += `<a href="${item.absolute_url}" class="social-icon"><i class="far fa-comment clear flex-row" data-number="${item.num_of_comments}"></i></a>`;
                } else {
                    html += `<a href="${item.absolute_url}" class="social-icon"><i class="far fa-comment clear flex-row"></i></a>`;
                }
                html += `<a href="#" class="social-icon"><i class="fas fa-retweet clear flex-row"></i></a>`;

                // Check of number of likes is not null and if post has been already liked by the current user
                if(item.already_liked) { 
                    html += `<a href="#" class="social-icon"><i class="fas fa-heart clear flex-row liked" data-number="${item.num_of_likes}"></i></a>`;
                } else if(item.num_of_likes) {
                    html += `<a href="#" class="social-icon"><i class="far fa-heart clear flex-row" data-number="${item.num_of_likes}"></i></a>`;
                } else {
                    html += `<a href="#" class="social-icon"><i class="far fa-heart clear flex-row"></i></a>`;
                }
                
                // Finally add the rest of the post
                html += `<a href="#" class="social-icon"><i class="fas fa-share-square flex-row"></i></a>
                        </div>
                        </div>
                    </div>`;  
        }
    });
    // Add everything to the Post container
    container.innerHTML += html;
};

// Build container for search results
export function buildSearchResults(data, container, input) {
    let html = "";
    data.map((item) => {
        let name = `${item.first_name} ${item.last_name}`;
        if (name.toLowerCase().includes(input.toLowerCase()) || item.username.toLowerCase().includes(input.toLowerCase())) {
        html +=
            `
                <li class="result-container flex-row">
                    <img src=${item.profile_pic}>
                    <div>
                        <a href="${item.absolute_url}">${name}</a>
                        <p>@${item.username}</p>
                    </div>
                </li> 
            `;
        }
    });
    html = html ? html : "No results.";
    container.innerHTML = html;
}