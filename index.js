const express = require('express');
const {spawn} = require('child_process');
const {giveData} = require('./utils/giveSingleData');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 8081;

app.use(cors());

app.get('/', (req, res)=>{
    const python = spawn('python', ['sample.py', "shriyam", 'tripathi']);
    python.stdout.on('data', (data)=>{
        console.log('Data from python:: ');
        console.log(data.toString());
        res.json({
            body: data.toString()
        })
    });
});

app.get('/getCompanyData/:company/:code/daily', async (req, res)=>{
    let data = await giveData(`https://www.moneycontrol.com/technical-analysis/${req.params.company}/${req.params.code}/daily`);
    res.json({
        msg: "Data received",
        name: data.name,
        data: data.data
    })
})

app.listen(PORT, ()=>{
    console.log(`The app is running on PORT: ${PORT}`);
})