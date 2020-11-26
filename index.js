const express = require('express');
const {spawn} = require('child_process');
const {giveData} = require('./utils/giveSingleData');
const {giveStocks} = require('./utils/getStockData');
const {giveAnalysis} = require('./utils/getAnalysis');
const {giveNews} = require('./utils/getNews');
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
});

app.get('/getStockData', async (req, res)=>{
    let data = await giveStocks();
    res.json(data);
});

app.get('/getAnalysis/:company/:code', async (req, res)=>{
    let data = await giveAnalysis(`https://www.moneycontrol.com/swot-analysis/${req.params.company}/${req.params.code}/`);
    res.json(data);
})

app.get('/getNews', async (req, res)=>{
    let news = await giveNews();
    res.json({news});
})

app.listen(PORT, ()=>{
    console.log(`The app is running on PORT: ${PORT}`);
})