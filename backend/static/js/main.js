document.getElementById("stressForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        age: document.getElementById("age").value,
        sleep: document.getElementById("sleep").value,
        screen: document.getElementById("screen").value,
        work: document.getElementById("work").value,
        activity: document.getElementById("activity").value
    };

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await response.json();
    alert("Your Stress Level: " + result.stress_level);
});
