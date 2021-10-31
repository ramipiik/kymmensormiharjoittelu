const timer = document.getElementById('stopwatch');
const input = document.getElementById('input');
const timeUsed = document.getElementById('timeUsed');
const errors = document.getElementById('errors');
const error_rate = document.getElementById('error_rate');
const speed = document.getElementById('speed');
const errorAdjustedTime=document.getElementById('ErrorAdjustedTime')
const pauseButton=document.getElementById('pauseButton')
const resetButton=document.getElementById('resetButton')
const insructions=document.getElementById('instructions')
const scoreBoard=document.getElementById('scoreBoard')
const history=document.getElementById('history')
var test = document.getElementById('test')
var resultBox=document.getElementById('resultBox')
var date = document.getElementById('date')
var time = document.getElementById('time')

var hr = 0;
var min = 0;
var sec = 0;
var stoptime = true;

function filter(level, tried, passed) {
  // Loop through all list items, and hide those who don't match the search query

  elements = document.getElementsByName('item');
  count=0
  
  for (i = 0; i < elements.length; i++) {
    a = elements[i].getElementsByTagName("span")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue == level.toString() || level=="all") {
        elements[i].style.display = "";
        count++;
    }
    else {
        elements[i].style.display = "none";
    } 
  }
  
  document.getElementById("totalExercises").innerHTML=count
  tried_on_this_level=document.getElementById("total_tried_helper").innerHTML
  passed_on_this_level=document.getElementById("total_passed_helper").innerHTML

  if (level != 'all'){
    if (tried[level]) {
        tried_on_this_level=tried[level]
    } else {
        tried_on_this_level=0
    }
    if (passed[level]) {
        passed_on_this_level=passed[level]
    } else {
        passed_on_this_level=0
    }
  }
  document.getElementById("tried").innerHTML=tried_on_this_level
  document.getElementById("passed").innerHTML=passed_on_this_level
}

function startTimer() {
  console.log("start timer")
  if (stoptime == true) {
        stoptime = false;
        timerCycle();
    }
}

function goBack() {
  window.history.back();
}

function refreshPage() {
  window.reload();
}

function delete_exercise(id) {
  confirm("Are you sure that you want to delete exercise "+id+"?");
  data = {
    id: id
  }
  URL= '/delete'
  postRequest(data, URL)
}

function toggleHistory() {
  if (history.style.display == 'none') {
    history.style.display = 'block'
    document.getElementById('toggleHistoryButton').innerHTML='Hide'
  } else {
    history.style.display = 'none'
    document.getElementById('toggleHistoryButton').innerHTML='Show'
  }
}

function toggleSignup() {
  signup=document.getElementById("signup")
  if (signup.style.display == 'none') {
    signup.style.display = 'block'
    document.getElementById('toggleSignupButton').innerHTML='Hide'
  } else {
    signup.style.display = 'none'
    document.getElementById('toggleSignupButton').innerHTML='Show'
  }
}

function toggleInstructions() {
  if (instructions.style.display == 'none') {
    instructions.style.display = 'block'
    document.getElementById('toggleInstructionsButton').innerHTML='Hide'
  } else {
    instructions.style.display = 'none'
    document.getElementById('toggleInstructionsButton').innerHTML='Show'
  } 
  input.disabled = false;
  input.style.backgroundColor = "white";
  input.focus();
}

function toggleScoreBoard() {
  if (scoreBoard.style.display == 'none') {
    scoreBoard.style.display = 'block'
    document.getElementById('toggleScoreBoardButton').innerHTML='Hide'
  } else {
    scoreBoard.style.display = 'none'
    document.getElementById('toggleScoreBoardButton').innerHTML='Show'
  } 
  input.disabled = false;
  input.style.backgroundColor = "white";
  input.focus();
}

function secondsToTime(seconds) {
  seconds=parseInt(seconds)
  minutes=0
  hours=0
  if (seconds>=60) {
    minutes=Math.floor(seconds/60)
    seconds-=minutes*60
    if (minutes>=60) {
      hours=Math.floor(minutes/60)
      minutes-=hours*60
    }
  } 

  if (seconds < 10 || seconds == 0) {
    seconds = '0' + seconds;
  }
  if (minutes < 10 || minutes == 0) {
    minutes = '0' + minutes;
  }
  if (hours < 10 || hours == 0) {
    hours = '0' + hours;
  }

  var result = hours + ':' + minutes + ':' + seconds;
  return result

}

// Code of the stopwatch adapted from https://dev.to/gspteck/create-a-stopwatch-in-javascript-2mak
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
    if (resultBox.style.display != "none") resultBox.style.display="none"
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
  if (sim<1) sim-=0.075
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


function postRequest(data, URL) {
  fetch(URL, {
    method: "POST",
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify(data)
  }).then(res => {
    console.log("Request complete! response:", res);
    window.location.reload();
  });
}


function submit(){
  if (stoptime == false) {
    stoptime = true;
  }
  input.style.backgroundColor = "whiteSmoke";
  input.disabled = true;
  var totalSeconds=parseInt(hr)*3600+parseInt(min)*60+parseInt(sec)
  if (totalSeconds==0) {
    return
  }
  timeUsed.innerHTML=secondsToTime(totalSeconds)
  var textInput=input.value
  var err;
  var penalty;
  const text_to_write=document.getElementById('textToWrite').innerHTML
  sim=similarity(text_to_write, textInput)
  err=sim[0]
  penalty=sim[1]
  
  err=parseInt(err)
  var adjustedSeconds=parseInt(totalSeconds/penalty);
  if (adjustedSeconds>359999) {
    adjustedSeconds=359999
  }
  ErrorAdjustedTime.innerHTML=secondsToTime(adjustedSeconds);
  errors.innerHTML=err;

  a=Math.round(text_to_write.length/totalSeconds*60,0)
  b=err/text_to_write.length*100
  b=b.toFixed(1)

  speed.innerHTML=a
  error_rate.innerHTML=b
  
  resultBox.style.display="block";
  document.getElementById('id_truebtn').style.display="block"
  document.getElementById('id_truebtn').focus()

  document.getElementById('id_truebtn').onclick = function(){
      var exercise_id=document.getElementById('exerciseId').innerHTML
      console.log("exercise_id", exercise_id)
      exercise_id=parseInt(exercise_id)
      console.log("exercise_id", exercise_id)
      data = {
        exercise_id: exercise_id,
        used_time: totalSeconds,
        adjusted_time: adjustedSeconds,
        errors: err
      }
      postRequest(data, "/new_result")      
  };
}
