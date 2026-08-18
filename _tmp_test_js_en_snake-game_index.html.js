
let canvas, ctx, gameLoop, snake, food, direction, nextDirection, score, highScore, isRunning, isPaused, speed, boardSize, cellSize;
function startGame() {
    speed = parseInt(document.getElementById("speedSelect").value);
    boardSize = parseInt(document.getElementById("boardSize").value);
    cellSize = Math.min(420 / boardSize, 28);
    canvas = document.getElementById("gameCanvas");
    canvas.width = boardSize * cellSize;
    canvas.height = boardSize * cellSize;
    ctx = canvas.getContext("2d");
    snake = [{x: Math.floor(boardSize/2), y: Math.floor(boardSize/2)}];
    direction = "right";
    nextDirection = "right";
    score = 0;
    isRunning = true;
    isPaused = false;
    if (!highScore) highScore = parseInt(localStorage.getItem("snakeHighScoreEN") || "0");
    document.getElementById("highScore").textContent = highScore;
    spawnFood();
    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(update, speed);
    draw();
}
function spawnFood() {
    let pos;
    do {
        pos = {x: Math.floor(Math.random() * boardSize), y: Math.floor(Math.random() * boardSize)};
    } while (snake.some(s => s.x === pos.x && s.y === pos.y));
    food = pos;
}
function update() {
    if (!isRunning || isPaused) return;
    direction = nextDirection;
    const head = {...snake[0]};
    if (direction === "up") head.y--;
    else if (direction === "down") head.y++;
    else if (direction === "left") head.x--;
    else if (direction === "right") head.x++;
    if (head.x < 0 || head.x >= boardSize || head.y < 0 || head.y >= boardSize || snake.some(s => s.x === head.x && s.y === head.y)) {
        gameOver();
        return;
    }
    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        document.getElementById("score").textContent = score;
        spawnFood();
    } else {
        snake.pop();
    }
    draw();
}
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < snake.length; i++) {
        const s = snake[i];
        ctx.fillStyle = i === 0 ? "#22d3ee" : "#06b6d4";
        ctx.shadowColor = i === 0 ? "rgba(34,211,238,.5)" : "transparent";
        ctx.shadowBlur = i === 0 ? 8 : 0;
        ctx.fillRect(s.x * cellSize + 1, s.y * cellSize + 1, cellSize - 2, cellSize - 2);
        ctx.shadowBlur = 0;
    }
    ctx.fillStyle = "#ef4444";
    ctx.shadowColor = "rgba(239,68,68,.5)";
    ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.arc(food.x * cellSize + cellSize/2, food.y * cellSize + cellSize/2, cellSize/2 - 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
}
function gameOver() {
    isRunning = false;
    clearInterval(gameLoop);
    if (score > highScore) {
        highScore = score;
        localStorage.setItem("snakeHighScoreEN", highScore.toString());
        document.getElementById("highScore").textContent = highScore;
    }
    ctx.fillStyle = "rgba(0,0,0,.6)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#f87171";
    ctx.font = "bold 24px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Game Over", canvas.width/2, canvas.height/2 - 10);
    ctx.fillStyle = "#94a3b8";
    ctx.font = "16px sans-serif";
    ctx.fillText("Score: " + score, canvas.width/2, canvas.height/2 + 20);
}
function togglePause() {
    if (!isRunning) return;
    isPaused = !isPaused;
    if (isPaused) {
        ctx.fillStyle = "rgba(0,0,0,.3)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#94a3b8";
        ctx.font = "bold 20px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("Paused", canvas.width/2, canvas.height/2);
    }
}
document.addEventListener("keydown", function(e) {
    e.preventDefault();
    if (!isRunning) return;
    if (e.key === "ArrowUp" && direction !== "down") nextDirection = "up";
    else if (e.key === "ArrowDown" && direction !== "up") nextDirection = "down";
    else if (e.key === "ArrowLeft" && direction !== "right") nextDirection = "left";
    else if (e.key === "ArrowRight" && direction !== "left") nextDirection = "right";
    else if (e.key === " " || e.key === "p") togglePause();
});
startGame();
