const cheerio = require('cheerio');
const axios = require('axios');

async function giveData(link){
  try {
    var res = await axios.get(link);
    const $ = cheerio.load(res.data);
    let data =[];
    let table = $(`.mtindi.FR #techindd .mt20 tbody`).eq(1).find("tr");
    let companyName = $(`h1.pcstname`).eq(0).text().trim();
    table.each((index, el)=>{
        let tempdata = {
            period: $(el).find("td").eq(0).text().trim(),
            level: $(el).find("td").eq(1).text().trim(),
            indication: $(el).find("td").eq(2).text().trim()
        };
        data.push(tempdata);
    })
    return {
      data,
      name: companyName
    };
  } catch (e) {
    return {
      msg: "Something went wrong",
      err: e
    };
  }
}

module.exports = {giveData};
