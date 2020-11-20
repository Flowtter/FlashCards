var questions = [];
var answers = [];
var actual = 0;
var question_show_state = false;

function refresh() {
    console.log("Refreshing!");
    var loader = document.getElementById("topic-container");
    questions = [];
    answers = [];
    var container = document.getElementById("topic-container");
    container.innerHTML = "";
    container = document.getElementById("sub-topic-container");
    container.innerHTML = "";
    container = document.getElementById("game-main-container");
    container.style.display = "none";

    var loader = document.getElementById("loader");
    loader.style.display = "flex";

    axios.get("/refresh")
    .then(function (reponse){refreshed(reponse.data.payload);});
}

function refreshed(data) {
    var loader = document.getElementById("loader");
    loader.style.display = "none";
    console.log("Refreshed!");
}

function fetch_request() {
    questions = [];
    answers = [];
    var container = document.getElementById("topic-container");
    container.innerHTML = "";
    container = document.getElementById("sub-topic-container");
    container.innerHTML = "";
    container = document.getElementById("game-main-container");
    container.style.display = "none";
    axios.get("/fetch")
    .then(function (reponse){fetch(reponse.data.payload, 'topic-container');})
}

function fetch(data, container) {
    console.log(data);
    var datas = data.split('\n');
    var i;
    for (i = 1; i < datas.length; i++) {
        datas[i] = datas[i].split(",")[0];
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
    console.log("fetching subtopics!");
    console.log("/sub_topic/" + name);
    var node = document.getElementById('sub-topic-container');
    node.innerHTML = "";
    axios.get("/sub_topic/" + name)
    .then(function (reponse){fetch(reponse.data.payload, "sub-topic-container");})
}

function startGame(data) {
    //console.log(data);
    var cards = data.split('\n');
    for (i = 0; i < cards.length-1; i++) {
        split = cards[i].split(',');
        questions.push(split[0].replaceAll(';', '<br>'));
        console.log(cards[i].replaceAll(';', '<br>'));
        answers.push(split[1]);
    }
    
    new_question();
}

function fetch_subject(name) {
    var container = document.getElementById("topic-container");
    container.innerHTML = "";
    container = document.getElementById("sub-topic-container");
    container.innerHTML = "";
    container = document.getElementById("game-main-container");
    container.style.display = "flex";
    axios.get("/subject/" + name)
    .then(function (reponse){startGame(reponse.data.payload);});
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}


function new_question() {
    console.log(questions);
    console.log(answers);
    if (questions.length != 0) {
        question_show_state = false;
        actual = getRandomInt(questions.length);
        var question = document.getElementById('game-question');
        question.innerHTML = questions[actual];
    } else {
        no_more_cards();
    }
}

function display() {
    if (questions.length != 0) {
        var text = document.getElementById('game-question');
        console.log(question_show_state);
        if (question_show_state) {
            text.innerHTML = questions[actual];
            question_show_state = false;
        } else {
            text.innerHTML = answers[actual];
            question_show_state = true;
        }
    }
}

function no_more_cards() {
    var text = document.getElementById('game-question');
    text.innerHTML = "no more cards";
}

function correct() {
    answers[actual] = answers[answers.length-1];
    questions[actual] = questions[questions.length-1];
    answers.pop();
    questions.pop();
    new_question();
}