const express = require('express');
const bodyParser = require('body-parser');
const os = require('os');

const app = express();
const hostname = os.hostname();
const startTime = os.uptime();

const PORT = 80;


// Middleware to parse JSON bodies
app.use(bodyParser.json());

app.get("/prime/health", (req,res)=>{
    console.log("PRIME CHECKER| Recevied health check");
    res.send("OK!");
})

app.get("/prime/info", (req, res) => {
  console.log("PRIME CHECKER| Received get info request")
  const info = {
    "hostname":hostname,
    "uptime":(os.uptime() - startTime) + "s",
    "api":"primechecker"
  }
  res.send(info)
})


app.get('/prime/isprime/:number', (req, res) => {
  const number = parseInt(req.params.number);
  console.log("PRIME CHECKER| Received prime check request")
  if (isNaN(number)) {
      return res.status(400).json({ error: 'Invalid number' });
  }

  const primeCheck = isPrime(number);
  res.json({ number, isPrime: primeCheck });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });


const  isPrime = (num) => {
    if (num <= 1) return false;
    if (num <= 3) return true;
    
    if (num % 2 === 0 || num % 3 === 0) return false;

    for (let i = 5; i * i <= num; i += 6) {
        if (num % i === 0 || num % (i + 2) === 0) return false;
    }

    return true;
}
