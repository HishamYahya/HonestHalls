const answerElements = document.querySelectorAll('.answer');
var answers = [];

addToAnswers('first', ['1', '2', '3'], ['Not important', 'A bit', 'Very important']);
addToAnswers('second', ['1', '2', '3'], ['Not at all', 'A bit', 'Need complete silence']);
addToAnswers('third', ['1', '2', '3'], ['Not important', 'A bit', 'Very important']);
addToAnswers('catering', ['catered', 'self-catered', 'na'], ['Catered', 'Self-catered', 'Don\'t mind either']);
addToAnswers('bed', ['single', 'double', 'na'], ['Single', 'Double', 'Don\'t mind either']);
addToAnswers('basin_ensuite', ['ensuite', 'basin', 'na'], ['Yes', 'No', 'Doesn\'t matter']);

answers.forEach((answer, i) => {
    answerElements[i].innerText = answer;
})


function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function getUrlParam(parameter){
    var urlparameter = '';
    if(window.location.href.indexOf(parameter) > -1){
        urlparameter = getUrlVars()[parameter];
        }
    return urlparameter;
}

function addToAnswers(param, cases, options) {
    const value = getUrlParam(param);
    switch(value) {
        case cases[0]:
            answers.push(options[0])
            break;
        case cases[1]:
            answers.push(options[1])
            break;
        case cases[2]:
            answers.push(options[2])
            break;
        default:
            answers.push('Something went wrong')
}
}