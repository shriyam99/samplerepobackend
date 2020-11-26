const cheerio = require('cheerio');
const axios = require('axios');

async function giveNews(){
  try {
    var res = await axios.get("https://economictimes.indiatimes.com/?from=mdr");
    const $ = cheerio.load(res.data);
    let data =[];
    let records = $(`li[data-ga-action="Widget Top News"] li`);
    records.each((index, el)=>{
        let text = $(el).find('a').eq(0).text().trim();
        let link = $(el).find('a').attr('href');
        if(!!text && !!link) data.push({text, link: `https://economictimes.indiatimes.com${link}`});
    })
    return data;
  } catch (e) {
    return {
      msg: "Something went wrong",
      err: e
    };
  }
}

module.exports = {giveNews};
