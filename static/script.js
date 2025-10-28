const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username') || 'default';

document.addEventListener("DOMContentLoaded", () => {
    loadPair();
    loadRankings();
});

function loadPair() {
    fetch(`/pair?username=${username}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('course1').textContent = data.course1;
            document.getElementById('course2').textContent = data.course2;

            document.getElementById('course1').onclick = () => vote(data.course1, data.course2);
            document.getElementById('course2').onclick = () => vote(data.course2, data.course1);
        });
}

function vote(winner, loser) {
    fetch('/vote', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({winner, loser, username})
    }).then(() => {
        loadPair();
        loadRankings();
    });
}

function loadRankings() {
    fetch(`/rankings?username=${username}`)
        .then(res => res.json())
        .then(data => {
            const rankings = document.getElementById('rankings');
            rankings.innerHTML = '';
            data.forEach((course, index) => {
                rankings.innerHTML += `<li class="list-group-item">
                    ${index + 1}. ${course.name} (${course.rating})
                </li>`;
            });
        });
}

