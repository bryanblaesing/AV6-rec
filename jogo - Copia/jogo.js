document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    const nave = new Image();
    nave.src = "caminho-para-nave.png"; // Substitua pelo caminho real da imagem da nave
    const naveWidth = 60;
    const naveHeight = 60;
    let naveX = 200;
    let naveY = 300;
    let naveSpeed = 5;

    const alien = new Image();
    alien.src = "caminho-para-alien.png"; // Substitua pelo caminho real da imagem do alienígena
    const alienWidth = 70;
    const alienHeight = 70;
    let alienX = canvas.width;
    let alienY = Math.random() * (canvas.height - alienHeight);

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Desenhar nave
        ctx.drawImage(nave, naveX, naveY, naveWidth, naveHeight);

        // Desenhar alienígena
        ctx.drawImage(alien, alienX, alienY, alienWidth, alienHeight);

        requestAnimationFrame(draw);
    }

    function gameLoop() {
        // Atualizar posição do alienígena
        alienX -= 4;

        // Verificar colisão
        if (naveX + naveWidth > alienX && naveX < alienX + alienWidth &&
            naveY + naveHeight > alienY && naveY < alienY + alienHeight) {
            alert("Você perdeu!");
            window.location.reload();
        }

        // Repetir o loop do jogo
        requestAnimationFrame(gameLoop);
    }

    // Capturar teclas pressionadas
    window.addEventListener("keydown", function (event) {
        switch (event.key) {
            case "ArrowUp":
                if (naveY > 0) naveY -= naveSpeed;
                break;
            case "ArrowDown":
                if (naveY < canvas.height - naveHeight) naveY += naveSpeed;
                break;
            case " ":
                // Implementar disparo do míssil
                break;
        }
    });

    nave.onload = function () {
        draw();
        gameLoop();
    };
});
