var used = false

function update_games() {
    if (!used) {
        used = true
        const feedDisp = document.querySelector('#feed')
        feedDisp.insertAdjacentHTML("beforeend", "NBA Games    ")
        fetch('http://localhost:3500/nbaScores')
            .then(response => response.json())
            .then(data => {
                console.log(data)
                data.games.forEach((key) => {
                    var match = "~  " + key.away + " at " + key.home + "  "
                    feedDisp.insertAdjacentHTML("beforeend", match)
                    console.log(match)
                    console.log(key)
                    used = true
                });
            })
    }

}

function star_game() {
    fetch('http://localhost:3500/stargame')
    console.log("Now playing Star Chase")
}

function farkle() {
    fetch('http://localhost:3500/farkle')
    console.log("Now playing Farkle")
}