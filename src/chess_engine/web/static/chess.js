const board = document.getElementById("board");
const statusElement = document.getElementById("status");
const movesElement = document.getElementById("moves");
const newGameButton = document.getElementById("new-game");
const capturedWhiteElement = document.getElementById("captured-white");
const capturedBlackElement = document.getElementById("captured-black");
const materialAdvantageElement =
    document.getElementById("material-advantage");
const evaluationElement = document.getElementById("evaluation");
const showEvaluationCheckbox =
    document.getElementById("show-evaluation");

let gameState = null;
let selectedSquare = null;

function renderGameInfo() {
    capturedWhiteElement.textContent =
        gameState.captured_white.join(" ") || "—";

    capturedBlackElement.textContent =
        gameState.captured_black.join(" ") || "—";

    const materialDifference =
        gameState.white_material - gameState.black_material;

    if (materialDifference === 0) {
        materialAdvantageElement.textContent = "Equal";
    } else if (materialDifference > 0) {
        materialAdvantageElement.textContent =
            `White +${materialDifference}`;
    } else {
        materialAdvantageElement.textContent =
            `Black +${Math.abs(materialDifference)}`;
    }

    const evaluation = gameState.evaluation;

    if (evaluation >= 1_000_000) {
        evaluationElement.textContent = "White is winning by checkmate";
    } else if (evaluation <= -1_000_000) {
        evaluationElement.textContent = "Black is winning by checkmate";
    } else {
        evaluationElement.textContent =
            `${evaluation >= 0 ? "+" : ""}${(evaluation / 100).toFixed(2)}`;
    }

    evaluationElement.hidden = !showEvaluationCheckbox.checked;
}

function createBoard() {
    board.innerHTML = "";

    for (let rank = 8; rank >= 1; rank--) {
        for (let file = 0; file < 8; file++) {
            const square = String.fromCharCode("a".charCodeAt(0) + file) + rank;

            const element = document.createElement("button");
            element.className = "square";
            element.dataset.square = square;

            if ((file + rank) % 2 === 0) {
                element.classList.add("light");
            } else {
                element.classList.add("dark");
            }

            element.addEventListener("click", () => handleSquareClick(square));

            board.appendChild(element);
        }
    }
}


function render() {
    const pieces = new Map(
        gameState.pieces.map(piece => [piece.square, piece])
    );

    document.querySelectorAll(".square").forEach(element => {
        const square = element.dataset.square;
        const piece = pieces.get(square);

        element.textContent = piece ? piece.symbol : "";
        element.classList.toggle(
            "selected",
            square === selectedSquare
        );
    });

    if (gameState.status === "checkmate") {
        const winner = gameState.turn === "white" ? "Black" : "White";
        statusElement.textContent = `Checkmate! ${winner} wins.`;
    } else if (gameState.status === "stalemate") {
        statusElement.textContent = "Stalemate! Draw.";
    } else if (gameState.status === "check") {
        statusElement.textContent =
            `${capitalize(gameState.turn)} is in check.`;
    } else {
        statusElement.textContent =
            `${capitalize(gameState.turn)} to move.`;
    }

    if (gameState.human_move || gameState.bot_move) {
        const parts = [];

        if (gameState.human_move) {
            parts.push(`You: ${gameState.human_move}`);
        }

        if (gameState.bot_move) {
            parts.push(`Bot: ${gameState.bot_move}`);
        }

        movesElement.textContent = parts.join("    ");
    }
    renderGameInfo();
}


function handleSquareClick(square) {
    if (!gameState || gameState.turn !== "white") {
        return;
    }

    if (gameState.status === "checkmate" || gameState.status === "stalemate") {
        return;
    }

    if (selectedSquare === null) {
        const canMove = gameState.legal_moves.some(
            move => move.slice(0, 2) === square
        );

        if (canMove) {
            selectedSquare = square;
            render();
        }

        return;
    }

    const candidates = gameState.legal_moves.filter(
        move =>
            move.slice(0, 2) === selectedSquare &&
            move.slice(2, 4) === square
    );

    if (candidates.length === 0) {
        selectedSquare = null;
        render();
        return;
    }

    let move = candidates[0];

    if (candidates.length > 1) {
        const promotion = window.prompt(
            "Promote to: q, r, b, or n",
            "q"
        );

        const promotionMove = candidates.find(
            candidate => candidate[4] === promotion?.toLowerCase()
        );

        if (!promotionMove) {
            selectedSquare = null;
            render();
            return;
        }

        move = promotionMove;
    }

    selectedSquare = null;
    sendMove(move);
}


async function sendMove(move) {
    try {
        statusElement.textContent = "Your move";

        const response = await fetch("/api/move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ move }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Move failed.");
        }

        // Immediately show the human move.
        gameState = data;
        render();

        // If the game ended with the human move, don't ask the bot to move.
        if (
            gameState.status === "checkmate" ||
            gameState.status === "stalemate"
        ) {
            return;
        }

        // Now let the bot think.
        statusElement.textContent = "Bot is thinking...";

        const botResponse = await fetch("/api/bot-move", {
            method: "POST",
        });

        const botData = await botResponse.json();

        if (!botResponse.ok) {
            throw new Error(botData.detail || "Bot move failed.");
        }

        gameState = botData;
        render();
    } catch (error) {
        statusElement.textContent = error.message;
    }
}


async function loadState() {
    const response = await fetch("/api/state");
    gameState = await response.json();

    createBoard();
    render();
}


async function newGame() {
    const response = await fetch("/api/new", {
        method: "POST",
    });

    gameState = await response.json();
    selectedSquare = null;
    render();
}


function capitalize(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
}


newGameButton.addEventListener("click", newGame);

loadState();