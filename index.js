const express = require('express');
const {spawn} = require('child_process');
const app = express();
const PORT = process.env.PORT || 8081;

var allowCrossDomain = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', "*");
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
}

app.use(allowCrossDomain);

app.get('/', (req, res)=>{
    const python = spawn('python', ['sample.py', "shriyam", 'tripathi']);
    python.stdout.on('data', (data)=>{
        console.log('Data from python:: ');
        console.log(data.toString());
        res.json({
            body: data.toString()
        })
    });
})

app.listen(PORT, ()=>{
    console.log(`The app is running on PORT: ${PORT}`);
})