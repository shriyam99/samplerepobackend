const cheerio = require('cheerio');
const axios = require('axios');

async function giveData(link){
  try {
    var res = await axios.get(link);
    const $ = cheerio.load(res.data);
    let data =[];
    let table = $(`.mtindi.FR #techindd .mt20 tbody`).eq(1).find("tr");
    table.each((index, el)=>{
        let tempdata = {
            period: $(el).find("td").eq(0).text().trim(),
            level: $(el).find("td").eq(1).text().trim(),
            indication: $(el).find("td").eq(2).text().trim()
        };
        data.push(tempdata);
    })
    return data;
  } catch (e) {
    return null;
  }
}

module.exports = {giveData};
