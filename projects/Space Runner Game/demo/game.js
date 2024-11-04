
const runner = document.querySelector("#runner")
const block = document.querySelector("#block")

window.addEventListener('keydown', (event) => {
    console.log(event)

    if (event.code == "Space") {
        console.log('Jump triggered!');
        runner.classList.add("jumpClass")

        setTimeout(() => {
            runner.classList.remove("jumpClass")
        }, 500);
    }
})

setInterval(() => {
    const runnerBottom = parseFloat(
        getComputedStyle(runner).getPropertyValue("bottom")
    );
    
    const blockLeft = parseFloat(
        getComputedStyle(block).getPropertyValue("left")
    );

    if ((blockLeft > -20 && blockLeft < 20) && (runnerBottom <= 40)) {
        console.log("Game Over")
    }
}, 10)