const express = require('express');
const bodyParser = require('body-parser');
const os = require('os');

const app = express();
const hostname = os.hostname();
const startTime = os.uptime();

const PORT = 80;

const users = [{name:"daham", age:28}, {name:"faith",age:26}];
const gifs = [
    "https://i0.wp.com/www.printmag.com/wp-content/uploads/2021/02/4cbe8d_f1ed2800a49649848102c68fc5a66e53mv2.gif?fit=476%2C280&ssl=1",
    "https://user-images.githubusercontent.com/14011726/94132137-7d4fc100-fe7c-11ea-8512-69f90cb65e48.gif",
    "https://i0.wp.com/www.galvanizeaction.org/wp-content/uploads/2022/06/Wow-gif.gif?fit=450%2C250&ssl=1",
    "https://i.pinimg.com/originals/9e/ff/42/9eff42b583de9434ac04d4cbc049a8d4.gif",
    "https://images.ctfassets.net/b4k16c7lw5ut/61X6cPeCANHior5BTSkvCQ/3499b68fa4eddd88b0b026682ed14960/Hello_GIF.gif",
];


// Middleware to parse JSON bodies
app.use(bodyParser.json());

app.get("/gifs/health", (req,res)=>{
    console.log("GIF API| Recevied health check");
    res.send("OK!");
})

app.get("/gifs/", (req,res)=>{
    console.log("GIF API| Request get gif recevied");
    const randonNumber = getRandomNumber(1,4);
    res.send(getHtml(randonNumber));
})


app.get("/gifs/info", (req, res) => {
  console.log("GIF API| Received get info request")
  const info = {
    "hostname":hostname,
    "uptime":(os.uptime() - startTime) + "s",
    "api":"gifapi"
  }
  res.send(info)
})

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });

function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

function getHtml(randonNumber){
    return `<div> <h1>Hello!!!!!</h1> <img src="${gifs[randonNumber]}"></img> </div>`
  }