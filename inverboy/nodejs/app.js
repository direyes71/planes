var io = require('socket.io').listen(8008);

var querystring = require('querystring');
var http = require('http');

var cookie_reader = require('cookie');


var fs, configuration_file;
configuration_file = 'configuration.json';
fs = require('fs');
var configuration = JSON.parse(
    fs.readFileSync(configuration_file)
);

function connection_host(path, method, headers){
    var connection_host = {
        host: configuration.host,
        port: configuration.port,
        path: path,
        method: method
    };
    if (headers != '') {
        connection_host.headers = headers;
    }
    return connection_host;
}

io.sockets.on("connection", function(socket){

    socket.on("newpublishedproject", function(data){

        /*console.log(socket.manager.handshaken);
        console.log(socket.handshake.headers);
        var values_cookie = cookie_reader.parse(socket.handshake.headers.cookie);
        data.sessionid = values_cookie['sessionid'];*/

        var values = querystring.stringify(data);

        var options = connection_host('/inverboy/home/ajax/newpublishedproject/' + data.project + '/', 'POST', {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            });

        /*
        var options = {
            host: 'localhost',
            port: 8000,
            path: '/inverboy/home/ajax/newpublishedproject/' + data.project + '/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            }
        };
        */

        var req = http.request(options, function(res){
        //var req = http.get(options, function(res){
            res.setEncoding('utf8');
            res.on('data', function(data){
                io.sockets.emit('postpublicationproject', data);
            });
        });
        req.write(values);
        req.end();

    });


    socket.on("newcommentpublishedproject", function(data){

        //var values_cookie = cookie_reader.parse(socket.handshake.headers.cookie);
        //data.sessionid = values_cookie['sessionid'];
        var values = querystring.stringify(data);

        var options = connection_host('/inverboy/home/ajax/newcommentpublishedproject/' + data.published + '/' + data.project + '/', 'POST', {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            });
                
        var req = http.request(options, function(res){
            res.setEncoding('utf8');
            res.on('data', function(data){
                io.sockets.emit('postcommentpublicationproject', data);
            });
        });
        req.write(values);
        req.end();

    });
});


/*
var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');

var redis = require('socket.io/node_modules/redis');
var sub = redis.createClient();

//Subscribe to the Redis chat channel
sub.subscribe('chat');

//Configure socket.io to store cookie set by Django
io.configure(function(){
    io.set('authorization', function(data, accept){
        if(data.headers.cookie){
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return accept(null, true);
        }
        return accept('error', false);
    });
    io.set('log level', 1);
});

io.sockets.on('connection', function (socket) {

    //Grab message from Redis and send to client
    sub.on('message', function(channel, message){
        socket.send(message);
    });

    //Client is sending message through socket.io
    socket.on('send_message', function (message) {
        values = querystring.stringify({
            comment: message,
            sessionid: socket.handshake.cookie['sessionid']
        });

        var options = {
            host: 'localhost',
            port: 4000,
            path: '/node_api',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            }
        };

        //Send message to Django server
        var req = http.get(options, function(res){
            res.setEncoding('utf8');

            //Print out error message
            res.on('data', function(message){
                if(message != 'Everything worked :)'){
                    console.log('Message: ' + message);
                }
            });
        });

        req.write(values);
        req.end();
    });
});

*/