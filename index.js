const express = require('express');
const moment = require('moment');
const cors = require('cors');
const bodyparser = require('body-parser');

const {giveData} = require('./utils/giveSingleData');
const {giveStocks} = require('./utils/getStockData');
const {giveAnalysis} = require('./utils/getAnalysis');
const {giveNews} = require('./utils/getNews');
const datafile = require('./datafile.json');
const tableData = require('./tableData.json');

const app = express();
const PORT = process.env.PORT || 8081;

app.use(cors());
app.use(bodyparser.json());

app.post('/', (req, res)=>{
    const {time} = req.body;
    console.log(time);
    let date = moment().add(parseInt(time), 'days').format("DD-MM-YYYY");
    let dataToSend = {date};
    let filtered = {};
    let maxTimeStamp;
    Object.keys(datafile).forEach((company)=>{
        let tempData = JSON.parse(datafile[company])["Open"];
        let companyTempData = {};
        Object.keys(tempData).forEach((timeStamp, index)=>{
            companyTempData[moment.unix(parseInt(timeStamp)/1000).format("DD-MM-YYYY")] = tempData[timeStamp];
            if (index==0) maxTimeStamp = timeStamp;
            else maxTimeStamp = Math.max(maxTimeStamp, timeStamp);
        });
        filtered[company] = companyTempData;
    })
    let lastDate = moment.unix(parseInt(maxTimeStamp)/1000).format("DD-MM-YYYY");
    let dataList = {};
    Object.keys(filtered).forEach((company)=>{
        let companyData = filtered[company];
        let res = !!companyData[date] ? companyData[date] : companyData[lastDate];
        dataList[company] = res;
    });
    dataToSend["data"] = dataList;
    res.json(dataToSend);
});

app.get('/search/:company', (req, res)=>{
    let {company} = req.params;
    company = company.toUpperCase();
    company = company+".NS";
    let filtered = {};
    Object.keys(tableData).forEach((company)=>{
        let tempData = JSON.parse(tableData[company])["Open"];
        let companyTempData = {};
        Object.keys(tempData).forEach((timeStamp, index)=>{
            companyTempData[moment.unix(parseInt(timeStamp)/1000).format("DD-MM-YYYY")] = tempData[timeStamp];
        });
        filtered[company] = companyTempData;
    })
    res.json(filtered[company]);
});


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