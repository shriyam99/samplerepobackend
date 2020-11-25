const cheerio = require('cheerio');
const axios = require('axios');

async function giveAnalysis(link){
  try {
    var res = await axios.get(link);
    const $ = cheerio.load(res.data);
    let strengthsData =[];
    let weaknessesData =[];
    let strengths = $(`#strength ul.swotfeatlist`).eq(0).find(`li`);
    let weaknesses = $(`#weakness ul.swotfeatlist`).eq(0).find(`li`);
    strengths.each((index, el)=>{
        let strength = $(el).text().trim();
        strengthsData.push(strength);
    });
    weaknesses.each((index, el)=>{
        let weakness = $(el).text().trim();
        weaknessesData.push(weakness);
    });
    return {
        strengthsData,
        weaknessesData
    };
  } catch (e) {
    return {
        msg: "Something went wrong",
        err: e
    };
  }
}

module.exports = {giveAnalysis};
