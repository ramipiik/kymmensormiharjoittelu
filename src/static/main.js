function test() {
    alert("moi!");
  }

// Code of the stopwatch adapted from https://dev.to/gspteck/create-a-stopwatch-in-javascript-2mak
const timer = document.getElementById('stopwatch');
const input = document.getElementById('input');
const result = document.getElementById('result');
const timeUsed = document.getElementById('timeUsed');
const errors = document.getElementById('errors');
const text_to_write=document.getElementById('textToWrite').innerHTML
const errorAdjustedTime=document.getElementById('ErrorAdjustedTime')
const pauseButton=document.getElementById('pauseButton')


var hr = 0;
var min = 0;
var sec = 0;
var stoptime = true;
// var errorcount=0

function startTimer() {
  if (stoptime == true) {
        stoptime = false;
        timerCycle();
    }
  // pauseButton.style.display=""
}
// function stopTimer() {
//   result.style.display="none"
//   if (stoptime == false) {
//     stoptime = true;
//   }
  
//   input.disabled=false
//   result.style.display="none"
//   input.style.backgroundColor = "white";
//   input.focus();
// }

function timerCycle() {
    if (stoptime == false) {
      sec = parseInt(sec);
      min = parseInt(min);
      hr = parseInt(hr);

      sec = sec + 1;

      if (sec == 60) {
        min = min + 1;
        sec = 0;
      }
      if (min == 60) {
        hr = hr + 1;
        min = 0;
        sec = 0;
      }

      if (sec < 10 || sec == 0) {
        sec = '0' + sec;
      }
      if (min < 10 || min == 0) {
        min = '0' + min;
      }
      if (hr < 10 || hr == 0) {
        hr = '0' + hr;
      }

      timer.innerHTML = hr + ':' + min + ':' + sec;

      setTimeout("timerCycle()", 1000);
  }
}

function resetTimer() {
    timer.innerHTML = '00:00:00';
    input.value = ''
    if (stoptime == false) {
      stoptime = true;
    }
    hr = 0;
    min = 0;
    sec = 0;
    input.style.backgroundColor = "white";
    input.disabled = false;
    if (result.style.display != "none") result.style.display="none"
    input.focus();
}

function similarity(s1, s2) {
  var longer = s1;
  var shorter = s2;
  if (s1.length < s2.length) {
    longer = s2;
    shorter = s1;
  }
  var longerLength = longer.length;
  if (longerLength == 0) {
    return 1.0;
  }
  var nr_errors=editDistance(longer, shorter)
  sim=(longerLength - nr_errors) / parseFloat(longerLength);
  if (sim<1) sim-=0.1
  if (sim<0) sim=0.000001
  multiplier=sim*sim*sim
  return [nr_errors, multiplier];
}

// Code adapted from https://stackoverflow.com/questions/10473745/compare-strings-javascript-return-of-likely
function editDistance(s1, s2) {
  var costs = new Array();
  for (var i = 0; i <= s1.length; i++) {
    var lastValue = i;
    for (var j = 0; j <= s2.length; j++) {
      if (i == 0)
        costs[j] = j;
      else {
        if (j > 0) {
          var newValue = costs[j - 1];
          if (s1.charAt(i - 1) != s2.charAt(j - 1))
            newValue = Math.min(Math.min(newValue, lastValue),
              costs[j]) + 1;
          costs[j - 1] = lastValue;
          lastValue = newValue;
        }
      }
    }
    if (i > 0)
      costs[s2.length] = lastValue;
  }
  return costs[s2.length];
}

function ready() {
  if (stoptime == false) {
    stoptime = true;
  }
  input.style.backgroundColor = "whiteSmoke";
  input.disabled = true;
  result.style.display="block"
  var totalSeconds=parseInt(hr)*3600+parseInt(min)*60+parseInt(sec)
  timeUsed.innerHTML=totalSeconds
  var textInput=input.value
  // pauseButton.style.display='none'
  var err;
  var penalty;
  [err, penalty]=(similarity(text_to_write, textInput));
  var adjustedSeconds=parseInt(totalSeconds/penalty);
  ErrorAdjustedTime.innerHTML=adjustedSeconds;
  errors.innerHTML=err;

}