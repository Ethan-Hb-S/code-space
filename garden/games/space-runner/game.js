window.onload = function () {
    var spaceRunner = document.getElementById('space-runner');
    spaceRunner.classList.add('offline');
  
    new Runner('#space-runner');
};