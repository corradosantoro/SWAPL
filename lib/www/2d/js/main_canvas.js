'use strict';

var MainCanvas = {

    image_cache : { },

    init : function() {
        var $this = this;
        this.canvas = document.createElement("canvas"); //document.getElementById("main-canvas");
        this.canvas_frame = document.getElementById("main-panel");
        this.canvas.width = this.canvas_frame.getClientRects()[0].width-30;
        this.canvas.height = this.canvas_frame.getClientRects()[0].height-30;
        this.canvas_frame.appendChild(this.canvas);

        var client = new HttpClient();
        client.get('/environment', function(response) {
            //console.log(response);
            response = JSON.parse(response);
            $this.environment = response;
        });

    },

    redraw: function() {
        var ctx = this.canvas.getContext("2d");
        ctx.globalAlpha = 1.0;
        ctx.fillStyle = "#000";
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        for (var i = 0; i < AgentView.agents.length; i++) {
            var x = AgentView.agents[i].x;
            var y = AgentView.agents[i].y;

            x = (x - this.environment.left) / (this.environment.right - this.environment.left) * this.canvas.width;
            y = (y - this.environment.top) / (this.environment.bottom - this.environment.top) * this.canvas.height;

            x = x % this.canvas.width;
            y = y % this.canvas.height;

            if (x < 0) x = this.canvas.width + x;
            if (y < 0) y = this.canvas.height + y;

            var angle = AgentView.agents[i].heading;
            var width = 16;
            var height = 16;
            var scale = 1;

            var image_name = AgentView.agents[i].image;
            var image = this.image_cache[image_name];
            if (image == undefined) {
                image = document.createElement("img");
                image.src = 'images/' + image_name;
                image.width = 16;
                image.height = 16;
                this.image_cache[image_name] = image;
            }

            //console.log(x, y, angle);
            ctx.translate(x, y);
            ctx.rotate(angle);
            ctx.drawImage(image, -width / 2, -height / 2);
            ctx.rotate(-angle);
            ctx.translate(-x, -y);

            if (AgentView.agents[i].name == AgentView.selectedAgent) {
                ctx.strokeStyle = "#fff";
                ctx.beginPath();
                ctx.arc(x, y, 32, 0, Math.PI*2);
                ctx.stroke();
            }
        }
    }

};
