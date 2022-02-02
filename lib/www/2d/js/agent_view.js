'use strict';


var AgentView = {

    ItemSelected : "linear-gradient(to bottom, #434343 0%, #4e4e4e 100%)",
    ItemNotSelected : "",

    agentNames : [ ],
    agents : [ ],
    agentForName : { },

    selectedAgent : undefined,

    load : function() {
        this.agentList = document.getElementById("agents");
        var $this = this;
        var client = new HttpClient();
        client.get('/agentlist', function(response) {
            response = JSON.parse(response);
            //console.log(response);
            var html = "";
            for (var i = 0; i < response.length;i++) {
                var x = response[i];
                $this.agentNames.push(x.name);
                var htmlText = '<a href="#" id="agent-' + i + '" class="agent-list-item">' + x.name + '</a><br/>';
                html = html + htmlText;
            }
            $this.agentList.innerHTML = html;

            for (var i = 0; i < response.length;i++) {
                var e = document.getElementById('agent-' + i);
                e.data_item = response[i];
                e.array_index = i;
                e.agent_name = response[i].name;
                e.onclick =
                    function(evt) {
                        var idx = evt.target.array_index;
                        $this.selectedAgent = evt.target.agent_name;
                        for (var i = 0; ;i++) {
                            var e = document.getElementById('agent-' + i);
                            if (e == null)
                                break;
                            if (idx == i) {
                                e.style.fontWeight = "bold";
                                e.style.backgroundImage = $this.ItemSelected;
                            }
                            else {
                                e.style.fontWeight = "normal";
                                e.style.backgroundImage = $this.ItemNotSelected;
                            }
                        }
                    };
            }
        });
    },

    loadAgents : function(next) {
        var $this = this;
        this.agents = [ ];
        this.agentForName = { };
        var client = new HttpClient();
        client.get('/agentlist', function(response) {
            //console.log(response);
            response = JSON.parse(response);
            for (var i = 0; i < response.length; i++) {
                var ag = response[i];
                $this.agents.push(ag);
                $this.agentForName[ag.name] = ag;
            }
            next();
        });
    },

};
