const cheerio = require('cheerio');
const axios = require('axios');

async function giveStocks(){
  try {
    var res = await axios.get(`https://www.moneycontrol.com/`);
    const $ = cheerio.load(res.data);
    let indianIndices = $(`#market_action .rhsglTbl`).eq(1).find("tr");
    let all = $(`.tpgls.MT20 .MT20`).eq(0).find(`.MT15`);
    let commodityandcurrency = $(`.comoCont.clearfix.MT20 .bxcom`);
    let indianIndicesData = [];
    let globalMarketData = [];
    let mostActiveData = [];
    let topGainersData = [];
    let topLosersData = [];
    let commoditiesData = [];
    let currenciesData = [];
    indianIndices.each((index, el)=>{
        let tempdata = {
            index: $(el).find("td").eq(0).text().trim(),
            price: $(el).find("td").eq(1).text().trim(),
            change: $(el).find("td").eq(2).text().trim(),
            percentageChange: $(el).find("td").eq(3).text().trim()
        };
        indianIndicesData.push(tempdata);
    });

    all.each((index, el)=>{
        let heading = $(el).find(`.tplhead a`).eq(0).text().trim();
        if(heading === "Global Markets"){
            let table = $(el).find('tbody tr');
            table.each((i, element)=>{
                let tempdata = {
                    index: $(element).find("td").eq(0).text().trim(),
                    price: $(element).find("td").eq(1).text().trim(),
                    change: $(element).find("td").eq(2).text().trim(),
                    percentageChange: $(element).find("td").eq(3).text().trim()
                };
                globalMarketData.push(tempdata);
            });
        }
        else if(heading === "Most Active"){
            let table = $(el).find(`#maNSE tbody tr`);
            table.each((i, element)=>{
                let tempdata = {
                    index: $(element).find("td").eq(0).text().trim(),
                    price: $(element).find("td").eq(1).text().trim(),
                    change: $(element).find("td").eq(2).text().trim(),
                    percentageChange: $(element).find("td").eq(3).text().trim()
                };
                mostActiveData.push(tempdata);
            });
        }
        else if(heading === "Top Gainers"){
            let table = $(el).find('#tgNifty tbody tr');
            table.each((i, element)=>{
                let tempdata = {
                    index: $(element).find("td").eq(0).text().trim(),
                    price: $(element).find("td").eq(1).text().trim(),
                    change: $(element).find("td").eq(2).text().trim(),
                    percentageChange: $(element).find("td").eq(3).text().trim()
                };
                topGainersData.push(tempdata);
            });
        }
        else if(heading === "Top Losers"){
            let table = $(el).find('#tlNifty tbody tr');
            table.each((i, element)=>{
                let tempdata = {
                    index: $(element).find("td").eq(0).text().trim(),
                    price: $(element).find("td").eq(1).text().trim(),
                    change: $(element).find("td").eq(2).text().trim(),
                    percentageChange: $(element).find("td").eq(3).text().trim()
                };
                topLosersData.push(tempdata);
            });
        }
    });
    commodityandcurrency.each((index, el)=>{
        let heading = $(el).find(`.tplhead`).eq(0).text().trim();
        if(heading==="Commodities"){
            let table = $(el).find(`#keymactb1 tbody tr`);
            table.each((i, element)=>{
                let tempdata = {
                    index: $(element).find("td").eq(0).text().trim(),
                    price: $(element).find("td").eq(1).text().trim(),
                    change: $(element).find("td").eq(3).text().trim(),
                    percentageChange: $(element).find("td").eq(4).text().trim()
                };
                commoditiesData.push(tempdata);
            });
        }
        else if(heading==="Currencies"){
            let table = $(el).find(`tbody tr`);
            table.each((i, element)=>{
                let tempdata = {
                    index: $(element).find("td").eq(0).text().trim(),
                    price: $(element).find("td").eq(1).text().trim(),
                    change: $(element).find("td").eq(2).text().trim(),
                    percentageChange: $(element).find("td").eq(3).text().trim()
                };
                currenciesData.push(tempdata);
            });
        }
    });
    return {
        indianIndicesData,
        globalMarketData,
        mostActiveData,
        topGainersData,
        topLosersData,
        commoditiesData,
        currenciesData
    };
  } catch (e) {
    return {
        msg: "Something went wrong",
        err: e
    };
  }
}

module.exports = {giveStocks};
