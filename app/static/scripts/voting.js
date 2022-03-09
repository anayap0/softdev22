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
            console.log(json);
            // document.getElementById("demo").innerHTML = JSON.stringify(json)
            vote_displayer = document.getElementById(post_id + "_votes");
            current_votes = parseInt(json['votes']);
            vote_displayer.innerText = current_votes;
        }) 
}