var cards = ""

function fetch_request() {
    var container = document.getElementById("topic-container");
    container.innerHTML = "";
    container = document.getElementById("sub-topic-container");
    container.innerHTML = "";
    container = document.getElementById("game-main-container");
    container.style.display = "none";
    axios.get("/fetch/")
    .then(function (reponse){fetch(reponse.data.payload, 'topic-container');})
}

function fetch(data, container) {
    var datas = data.split('\n')
    var i;
    for (i = 1; i < datas.length; i++) {
        datas[i] = datas[i].split(",")[0];
        console.log(datas[i]);
        createBubble(datas[i], container);
    }
}

function createBubble(text, container) {
    var bubble = document.createElement("div");
    bubble.className = "bubble";
    if (container == 'topic-container'){
        bubble.setAttribute("onclick",`fetch_subtopic("${text}")`);
    } else {
        bubble.setAttribute("onclick",`fetch_subject("${text}")`);
    }
    var content = document.createTextNode(text);
    bubble.appendChild(content);
    var currentDiv = document.getElementById(container);
    currentDiv.appendChild(bubble);
}

function fetch_subtopic(name) {
    var node = document.getElementById('sub-topic-container');
    node.innerHTML = "";
    axios.get("/sub_topic/" + name)
    .then(function (reponse){fetch(reponse.data.payload, "sub-topic-container");})
}

function startGame(data) {
    cards = data;
}

function fetch_subject(name) {
    var container = document.getElementById("topic-container");
    container.innerHTML = "";
    container = document.getElementById("sub-topic-container");
    container.innerHTML = "";
    container = document.getElementById("game-main-container");
    container.style.display = "flex";
    axios.get("/subject/" + name)
    .then(function (reponse){startGame(reponse.data.payload);})
}