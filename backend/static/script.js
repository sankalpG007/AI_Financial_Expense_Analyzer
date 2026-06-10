console.log("SCRIPT LOADED SUCCESSFULLY");

let categoryChart;
let monthlyChart;

// ======================================
// WAIT FOR PAGE TO LOAD
// ======================================


// ======================================
// FILE UPLOAD + ANALYSIS
// ======================================

async function uploadFile() {

    console.log("UPLOAD FUNCTION STARTED");
    alert("BUTTON WORKING");
    
    const fileInput =
        document.getElementById("fileInput");

    const loader =
        document.getElementById("loader");

    const statusText =
        document.getElementById("statusText");

    // Validation
    if (!fileInput.files[0]) {

        statusText.innerText =
            "❌ Please upload a file";

        return;
    }

    // Loader ON
    loader.classList.remove("hidden");

    statusText.innerText =
        "⏳ Analyzing your expenses...";

    // Form Data
    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    try {

        console.log("Sending API request...");

        const response = await fetch(
            "http://127.0.0.1:5000/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        console.log("Response received");

        if (!response.ok) {

    const errorText =
        await response.text();

    console.error(errorText);

    return;
}

const data =
    await response.json();

        console.log("DATA:", data);

        // Loader OFF
        loader.classList.add("hidden");

        statusText.innerText =
            "✅ Analysis completed successfully";

        // ======================================
        // UPDATE KPI CARDS
        // ======================================

        document.getElementById("totalSpending")
            .textContent =
            `₹${data.total_spending}`;

        document.getElementById("prediction")
            .textContent =
            `₹${Math.round(data.prediction)}`;

        document.getElementById("anomalies")
            .textContent =
            data.anomaly_count;

        // ======================================
        // INSIGHTS
        // ======================================

        const insightList =
            document.getElementById("insightList");

        insightList.innerHTML = "";

        data.insights.forEach(insight => {

            const li =
                document.createElement("li");

            li.textContent = insight;


            insightList.appendChild(li);
        });

        // =========================
        // AGENTIC AI ADVICE
        // =========================

        const adviceBox =
            document.getElementById(
                "agentAdvice"
            );

        adviceBox.innerText =
            data.agent_advice;

        // =========================
        // MULTI STEP REASONING
        // =========================

        const reasoningBox =
            document.getElementById(
                "reasoningBox"
            );

        reasoningBox.innerText =
            data.reasoning;

        // ======================================
        // CHARTS
        // ======================================

        createCategoryChart(
            data.category_spending
        );

        createMonthlyChart(
            data.monthly_spending
        );

    } catch (error) {

        console.error("FRONTEND ERROR:", error);

        loader.classList.add("hidden");

        statusText.innerText =
            "❌ Error analyzing file";
    }
}

// ======================================
// CATEGORY CHART
// ======================================

function createCategoryChart(data) {

    const ctx =
        document.getElementById("categoryChart");

    if (categoryChart)
        categoryChart.destroy();

    categoryChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: Object.keys(data),

            datasets: [{

                data: Object.values(data),

                backgroundColor: [

                    "#00FFAA",
                    "#00BFFF",
                    "#8B5CF6",
                    "#F59E0B",
                    "#EF4444",
                    "#10B981",
                    "#EC4899",
                    "#6366F1",
                    "#14B8A6"

                ],

                borderWidth: 2,

                borderColor: "#111827"
            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {
                        color: "white"
                    }
                }
            }
        }
    });
}


function createMonthlyChart(data) {

    const ctx =
        document.getElementById("monthlyChart");

    if (monthlyChart)
        monthlyChart.destroy();

    monthlyChart = new Chart(ctx, {

        type: "line",

        data: {

            labels: Object.keys(data),

            datasets: [{

                label: "Monthly Spending",

                data: Object.values(data),

                tension: 0.4,

                borderColor: "#00FFAA",

                backgroundColor:
                    "rgba(0,255,170,0.2)",

                fill: true,

                borderWidth: 3,

                pointBackgroundColor: "#00FFAA",

                pointRadius: 5
            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {
                        color: "white"
                    }
                }
            },

            scales: {

                x: {
                    ticks: {
                        color: "white"
                    }
                },

                y: {
                    ticks: {
                        color: "white"
                    }
                }
            }
        }
    });
}

async function sendMessage() {

     console.log("SEND MESSAGE CLICKED");

    const input =
        document.getElementById("chatInput");

    const chatBox =
        document.getElementById("chatBox");

    const message =
        input.value;

    if (!message) return;

    // USER MESSAGE

    chatBox.innerHTML += `
        <div class="message user">
            ${message}
        </div>
    `;

    input.value = "";

    // SEND TO BACKEND

    const response = await fetch(
        "http://127.0.0.1:5000/chat",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        }
    );


    if (!response.ok) {

    const errorText =
        await response.text();

    console.error(errorText);

    return;
}

const data =
    await response.json();

    // BOT MESSAGE

    chatBox.innerHTML += `
        <div class="message bot">
            ${data.response}
<br><small>
Memory Size: ${data.memory_size}
</small>
        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


