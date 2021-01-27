
function loadEventListeners() {
    const myModal = document.querySelector("#myModal");
    const modalBtn = document.querySelector("#myModalBtn");
    if(myModal && modalBtn) {
        
        myModal.addEventListener("click", (e) => {
            if(e.target == myModal || e.target.classList.contains("closeBtn")) {
                myModal.classList.add("inactive");
                setTimeout(() => {
                    document.body.style.overflow = "auto";
                    document.body.style.height = "auto";
                }, 200);
            }
        });
        
        modalBtn.addEventListener("click", (e) => {
            e.preventDefault();
            myModal.style.top = document.documentElement.scrollTop + "px";
            setTimeout(() => {
                myModal.classList.remove("inactive");
                document.body.style.overflowY = "hidden";
                document.body.style.height = "100%";
            }, 200);
        });
    }
}

loadEventListeners();