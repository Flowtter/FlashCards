var questions = [];
var answers = [];
var actual = 0;
var question_show_state = false;
var refreshing = false;
var size_deck;
var points;

function refresh() {
    document.getElementById("intro").style.display ="none";
    console.log("Refreshing!");
    refreshing = true;
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
    refreshing = false;
    console.log("Refreshed!");
}

function fetch_request() {
    document.getElementById("intro").style.display ="none";
    if (refreshing){
        console.log("still refreshing");
        return;
    }
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
    for (i = 0; i < datas.length; i++) {
        if (data[i]){
            createBubble(datas[i], container);
        }
    }
}

function createBubble(text, container) {
    var bubble = document.createElement("button");
    if (container == 'topic-container'){
        bubble.className = "bubble";
        bubble.setAttribute("onclick",`fetch_subtopic("${text}")`);
    } else {
        bubble.className = "bubble sub";
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
    size_deck = cards.length;
    points = 0;
    for (i = 0; i < cards.length; i++) {
        split = cards[i].split(',');
        var q = split[0].replaceAll(';', '<br>').replaceAll('§', ',').replaceAll('µ', ';');
        var a = split[1].replaceAll(';', '<br>').replaceAll('§', ',').replaceAll('µ', ';');
        if (q[0] == "*") {
            q = q.slice(1, q.length-1);
        }
        //q = exponent(q);
        //a = exponent(a);
        questions.push(q);
        answers.push(a);
    }
    new_question();
}

//function exponent(str) {
//    while (str.includes("^")) {
//        var i = str.indexOf("^");
//        var value = str[i+1]
//        str = str.replace("^", `<sup>${value}</sup>`);
//        return str;
//    }
//    return str;
//}

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
    text.innerHTML = "  Félicitation!";
}

function correct() {
    points++;
    console.log(points, size_deck);
    answers[actual] = answers[answers.length-1];
    questions[actual] = questions[questions.length-1];
    answers.pop();
    questions.pop();
    new_question();
}

function contact() {
    windowObjectReference = window.open("https://flowtter.netlify.app/english/main");
  }
