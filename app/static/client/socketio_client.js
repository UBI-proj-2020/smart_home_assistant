//var led = document.getElementById('led');
var led_start = document.getElementById('led_start');
var led_colorshift = document.getElementById('led_colorshift');
var led_increaseBrightness = document.getElementById('led_increaseBrightness');
var led_decreaseBrightness = document.getElementById('led_decreaseBrightness');
var led_stop = document.getElementById('led_stop');
var socketio = io.connect('https://smart-home-assistant.herokuapp.com' + '/client-user');
//var socketio = io.connect('http://127.0.0.1:5000' + '/client-user');


socketio.on('connect', function()    {
});

led_start.addEventListener("click", function()  {
    socketio.emit('LED_ON');
});

led_stop.addEventListener("click", function()  {
    socketio.emit('LED_OFF');
});

led_colorshift.addEventListener("click", function()  {
    socketio.emit('START_COLORSHIFT');
});

led_increaseBrightness.addEventListener("click", function()  {
    socketio.emit('INCREASE_BRIGHTNESS');
});

led_decreaseBrightness.addEventListener("click", function()  {
    socketio.emit('DECREASE_BRIGHTNESS');
});