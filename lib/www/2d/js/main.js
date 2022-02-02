'use strict';

var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() {
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );
        anHttpRequest.send( null );
    }
}

var TIMEOUT = 1.0/10.0 * 1000;

function onTimer() {
    AgentView.loadAgents(function() {
        MainCanvas.redraw();
    });
    setTimeout(onTimer, TIMEOUT);
}

function startup() {
    AgentView.load();
    MainCanvas.init();
    setTimeout(onTimer, TIMEOUT);
}

window.onload = startup;

