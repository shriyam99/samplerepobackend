const express = require('express');
// const {spawn} = require('child_process');
const {giveData} = require('./utils/giveSingleData');
const {giveStocks} = require('./utils/getStockData');
const {giveAnalysis} = require('./utils/getAnalysis');
const {giveNews} = require('./utils/getNews');
// const datafile = require('./datafile.json');
const cors = require('cors');
const bodyparser = require('body-parser');
const app = express();
const PORT = process.env.PORT || 8081;

app.use(cors());
app.use(bodyparser.json());

// app.post('/', (req, res)=>{
//     const {price, time} = req.body;
//     let dataToSend = {body: []}
//     let filtered = {};
//     Object.keys(datafile).forEach((company)=>{
//         let tempData = JSON.parse(datafile[company])["Open"];
//         filtered[company] = tempData;
//     })
//     res.json(dataToSend);
// })

app.get('/getCompanyData/:company/:code/daily', async (req, res)=>{
    let data = await giveData(`https://www.moneycontrol.com/technical-analysis/${req.params.company}/${req.params.code}/daily`);
    res.json({
        msg: "Data received",
        name: data.name,
        data: data.data,
        price: data.price
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
