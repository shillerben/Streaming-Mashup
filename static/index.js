function buildURL(movie) {
    var searchIndex = window.location.href.search("/index.html");
    var builtURL = "/result/" + encodeURI(movie.toLowerCase());
    window.location.href = builtURL;
}

function chooseFirst(event) {
    event.preventDefault();
    var matchContainer = document.getElementById("matchButtons");
    if (matchContainer.firstChild) {
        buildURL(matchContainer.firstChild.firstChild.firstChild.firstChild.innerHTML);
    }
    else {
        var currentInput = document.getElementById("query").value;
        buildURL(currentInput);
    }
}

function addButton(movie, container) {
    var fieldElement = document.createElement("div");
    fieldElement.className = "field";
    container.appendChild(fieldElement);

    var controlElement = document.createElement("div");
    controlElement.className = "control";
    fieldElement.appendChild(controlElement);

    var formElement = document.createElement("form");
    controlElement.appendChild(formElement);

    var buttonElement = document.createElement("button");
    buttonElement.className = "input is-large is-dark";
    buttonElement.type = "button";
    buttonElement.onclick = function() {buildURL(movie);};
    buttonElement.innerHTML = movie;
    formElement.appendChild(buttonElement);
}

function getMatches(searchTerm, searchList) {
    var matches = [];
    for (var i = 0; i < searchList.length; i++) {
        if (searchList[i].toLowerCase().search(searchTerm.toLowerCase()) != -1) {
            matches.push(searchList[i]);
        }
    }
    return matches;
}

function populateMatches() {
    var matchContainer = document.getElementById("matchButtons");
    // delete all old children
    while (matchContainer.firstChild) {
        matchContainer.removeChild(matchContainer.firstChild);
    }

    var currentInput = document.getElementById("query").value;

    if (currentInput.length > 1) {
        var matches = getMatches(currentInput, movieList);

        for (var i = 0; i < matches.length; i++) {
            addButton(matches[i], matchContainer);
        }
    }
}
