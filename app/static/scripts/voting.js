function checkStatus(response) {
    if (!response.ok) { // If the response has caused an error
        throw Error("Error in request: " + response.statusText); // Throw the error and print the description of the text 
    }
    return response; // If it was successful, it will return the response's text
}

function handleError(err) {
    console.log("Ran into error:", err);
}

function submitVote(post_id, action_vote) {
    // console.log("Submitting form")
    let url = "/_post_vote/" + post_id + "/" + action_vote
    response = fetch(url, {method: "POST"})
        .then(checkStatus) // Calls the checkStatus function, which checks whether the response is successful, throws error otherwise
        .catch(handleError)
        .then(response => response.json())  
        .then(json => {
            // Update votes count
            console.log(json);
            vote_displayer = document.getElementById(post_id + "_votes");
            current_votes = parseInt(json['votes']);
            vote_displayer.innerText = current_votes;
            
            // Update user vote visually
            upvote = document.getElementById(post_id + "_upvote_img");
            downvote = document.getElementById(post_id + "_downvote_img");
            if (action_vote == 1) {
                upvote.classList.add("vote_active");
                downvote.classList.remove("vote_active");
            }
            else if (action_vote == 0) {
                upvote.classList.remove("vote_active");
                downvote.classList.add("vote_active");
            }

        })
}