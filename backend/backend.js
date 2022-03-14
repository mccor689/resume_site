const PORT = 3500;
var express = require('express');
var cheerio = require('cheerio');
var axios = require('axios');
var app = express();
const {spawn} = require('child_process');
var cors = require('cors');
app.use(cors())
app.use(express.json())

var server = app.listen(PORT, function () {
    var host = server.address().address
    var port = server.address().port
    console.log("Example app listening at http://%s:%s", host, port)
 });

var games = []
const url = "https://www.cbssports.com/nba/scoreboard/"

app.get('/nbaScores', (req,res) =>
    
    axios(url)
    .then(response => {
        games = []
        const html = response.data
        const $ = cheerio.load(html)
        var teams = []
        $('a.team', html).each(function() {
            var names = $(this).text()
            teams.push(names)
        })
        for (let i = 0; i < teams.length; i+=2) {
            const away = teams[i]
            const home = teams[i+1]
            games.push({away, home})
        }
        console.log(games)
        res.json({games:games})
    })
)

app.get('/stargame', (req,res) => {
    const python = spawn('python', ['./starChase.py'])
    res.json({game:python})
})

app.get('/farkle', (req,res) => {
    const python = spawn('python', ['./farkle.py'])
    res.json({game:python})
})
