// Fetch system status every 2 seconds
setInterval(() => {
    fetch("/status")
        .then(response => response.json())
        .then(data => {
            document.getElementById("cpu").innerText = data.cpu;
            document.getElementById("ram").innerText = data.ram;
            document.getElementById("disk").innerText = data.disk;
            document.getElementById("proc").innerText = data.processes;
        });
}, 2000);
