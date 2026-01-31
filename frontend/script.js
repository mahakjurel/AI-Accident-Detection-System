/* =========================
   NAVIGATION
========================= */

document.getElementById("startBtn")?.addEventListener("click", function () {
    window.location.href = "monitor.html";
});

document.getElementById("dashboardBtn")?.addEventListener("click", function () {
    window.location.href = "dashboard.html";
});

function goBack() {
    window.location.href = "index.html";
}

function goHome() {
    window.location.href = "index.html";
}


/* =========================
   CAMERA
========================= */

function startCamera() {
    const video = document.getElementById("camera");

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(() => {
            alert("Camera permission denied");
        });
}


/* =========================
   ACCIDENT + ALERT UI
========================= */

function simulateAccident() {
    document.getElementById("statusText").innerText = "Accident Detected!";
    document.getElementById("probability").innerText = "96%";
    document.getElementById("locationText").innerText = "New Delhi, India";

    document.getElementById("alertBox")?.classList.remove("hidden");
    document.getElementById("alertPanel")?.classList.remove("hidden");
}

function sendAlerts() {
    document.getElementById("ambulanceStatus").innerText = "Sent ✅";
    document.getElementById("policeStatus").innerText = "Sent ✅";
    document.getElementById("contactStatus").innerText = "Sent ✅";

    alert("Emergency alerts sent successfully!");
}


/* =========================
   DASHBOARD DATA (DUMMY)
========================= */

const accidents = [
    {
        time: "10:45 AM",
        location: "NH-44, Delhi",
        severity: "High",
        status: "Sent"
    },
    {
        time: "11:20 AM",
        location: "Ring Road",
        severity: "Medium",
        status: "Pending"
    }
];

const table = document.getElementById("accidentTable");

if (table) {
    accidents.forEach(acc => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${acc.time}</td>
            <td>${acc.location}</td>
            <td>${acc.severity}</td>
            <td class="${acc.status === "Sent" ? "status-sent" : "status-pending"}">
                ${acc.status}
            </td>
        `;

        table.appendChild(row);
    });
}
// =========================
// FRONTEND → BACKEND TEST
// =========================
async function checkBackend() {
    try {
        const response = await fetch("http://localhost:8000/", {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }

        const data = await response.json();

        document.getElementById("statusText").innerText = "Backend Connected ✅";
        document.getElementById("probability").innerText = "API OK";

        alert(
            "Backend Connected Successfully!\n\n" +
            JSON.stringify(data, null, 2)
        );
    } catch (error) {
        alert("Backend not reachable ❌");
        console.error("Fetch error:", error);
    }
}
// =========================
// REAL VIDEO UPLOAD → BACKEND
// =========================
async function uploadVideo() {
    const input = document.getElementById("videoInput");
    const file = input.files[0];

    if (!file) {
        alert("Please select a video file first");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("statusText").innerText = "Analyzing video...";
    document.getElementById("probability").innerText = "...";

    try {
        const response = await fetch(
            "http://localhost:8000/api/upload-video",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (data.accident) {
            document.getElementById("statusText").innerText = "🚨 Accident Detected!";
            document.getElementById("probability").innerText =
                (data.confidence * 100).toFixed(1) + "%";
        } else {
            document.getElementById("statusText").innerText = "✅ No Accident";
            document.getElementById("probability").innerText =
                (data.confidence * 100).toFixed(1) + "%";
        }

        console.log("Detection Result:", data);

    } catch (error) {
        alert("Error connecting to backend");
        console.error(error);
    }
}
