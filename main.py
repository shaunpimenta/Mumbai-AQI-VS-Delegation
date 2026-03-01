from flask import Flask, jsonify, render_template_string
from datetime import datetime, timedelta

app = Flask(__name__)

aqi_data = [
    {"date": "2026-01-29", "aqi": 118},
    {"date": "2026-01-30", "aqi": 165},
    {"date": "2026-01-31", "aqi": 175},
    {"date": "2026-02-01", "aqi": 168},
    {"date": "2026-02-02", "aqi": 187},
    {"date": "2026-02-03", "aqi": 180},
    {"date": "2026-02-04", "aqi": 199},
    {"date": "2026-02-05", "aqi": 198},
    {"date": "2026-02-06", "aqi": 189},
    {"date": "2026-02-07", "aqi": 173},
    {"date": "2026-02-08", "aqi": 177},
    {"date": "2026-02-09", "aqi": 160},
    {"date": "2026-02-10", "aqi": 150},
    {"date": "2026-02-11", "aqi": 152},
    {"date": "2026-02-12", "aqi": 185},
    {"date": "2026-02-13", "aqi": 180},
    {"date": "2026-02-14", "aqi": 178},
    {"date": "2026-02-15", "aqi": 168},
    {"date": "2026-02-16", "aqi": 148},
    {"date": "2026-02-17", "aqi": 125},
    {"date": "2026-02-18", "aqi": 88},
    {"date": "2026-02-19", "aqi": 83},
    {"date": "2026-02-20", "aqi": 147},
    {"date": "2026-02-21", "aqi": 198},
    {"date": "2026-02-22", "aqi": 189},
    {"date": "2026-02-23", "aqi": 172},
    {"date": "2026-02-24", "aqi": 163},
    {"date": "2026-02-25", "aqi": 126},
    {"date": "2026-02-26", "aqi": 80},
    {"date": "2026-02-27", "aqi": 70}
]

# -----------------------------
# Delegation Data
# -----------------------------
delegations = [
    {"country": "Germany", "start": "2026-01-12", "end": "2026-01-13", "criticalness": "Medium"},
    {"country": "USA", "start": "2026-02-03", "end": "2026-02-03", "criticalness": "Medium"},
    {"country": "Seychelles", "start": "2026-02-07", "end": "2026-02-08", "criticalness": "High"},
    {"country": "Australia", "start": "2026-02-10", "end": "2026-02-12", "criticalness": "Low"},
    {"country": "France", "start": "2026-02-17", "end": "2026-02-17", "criticalness": "High"},
    {"country": "Canada", "start": "2026-02-27", "end": "2026-03-02", "criticalness": "High"},
]

def get_criticalness(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def check_delegation(date_obj):
    for d in delegations:
        start = datetime.strptime(d["start"], "%Y-%m-%d").date()
        end = datetime.strptime(d["end"], "%Y-%m-%d").date()
        if start <= date_obj <= end:
            return d["country"], d["criticalness"]
    return None, None

# -----------------------------
# Build Final Dataset
# -----------------------------
def build_dataset():
    final_data = []

    for entry in aqi_data:
        date_obj = datetime.strptime(entry["date"], "%Y-%m-%d").date()
        delegation_country, criticalness = check_delegation(date_obj)

        final_data.append({
            "Date": entry["date"],
            "AQI": entry["aqi"],
            "Delegation": delegation_country if delegation_country else "",
            "Delegation_Criticalness": criticalness if criticalness else ""
        })
    final_data.sort(key=lambda x: x["Date"], reverse=True)
    return final_data

@app.route("/api")
def api():
    return jsonify(build_dataset())

@app.route("/")
def home():
    data = build_dataset()
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Mumbai AQI vs Delegations</title>
    <script>
        window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
    </script>
    <script defer src="/_vercel/insights/script.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }

        .container {
            width: 90%;
            margin: 40px auto;
        }

        h2 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 32px;
            letter-spacing: 1px;
        }

        /* Chart Section Styles */
        .chart-wrapper {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .custom-legend {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            font-size: 14px;
        }

        .legend-color {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            margin-right: 8px;
            display: inline-block;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            overflow: hidden;
        }

        th {
            background: rgba(255, 255, 255, 0.15);
            padding: 14px;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 1px;
        }

        td {
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        tr:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        .badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 12px;
        }

        /* AQI Colors */
        .good { background: #2ecc71; }
        .moderate { background: #f1c40f; color: black; }
        .unhealthy { background: #e67e22; }
        .very-unhealthy { background: #e74c3c; }
        .hazardous { background: #8e44ad; }

        /* Delegation Importance */
        .high { background: #ff4757; }
        .medium { background: #ffa502; }
        .low { background: #2ed573; }
        .none { background: #57606f; }

        .footer {
            text-align: center;
            padding: 15px 0;
            background: rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(8px);
            font-size: 14px;
            letter-spacing: 0.5px;
        }

        .footer a {
            color: #2ed573;
            text-decoration: none;
            font-weight: 600;
            transition: 0.3s ease;
        }

        .footer a:hover {
            color: #ffffff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Mumbai AQI vs Delegations (Last 30 Days)</h2>

        <div class="chart-wrapper">
            <canvas id="aqiChart" height="80"></canvas>
            <div class="custom-legend">
                <span class="legend-item"><span class="legend-color high"></span>High Importance</span>
                <span class="legend-item"><span class="legend-color medium"></span>Medium Importance</span>
                <span class="legend-item"><span class="legend-color low"></span>Low Importance</span>
                <span class="legend-item"><span class="legend-color none"></span>No Delegation</span>
            </div>
        </div>

        <table>
            <tr>
                <th>Date</th>
                <th>AQI</th>
                <th>Delegation</th>
                <th>Delegation Importance</th>
            </tr>

            {% for row in data %}
            <tr>
                <td>{{ row.Date }}</td>

                <td>
                    {% set aqi = row.AQI %}
                    {% if aqi <= 50 %}
                        <span class="badge good">{{ aqi }}</span>
                    {% elif aqi <= 100 %}
                        <span class="badge moderate">{{ aqi }}</span>
                    {% elif aqi <= 200 %}
                        <span class="badge unhealthy">{{ aqi }}</span>
                    {% elif aqi <= 300 %}
                        <span class="badge very-unhealthy">{{ aqi }}</span>
                    {% else %}
                        <span class="badge hazardous">{{ aqi }}</span>
                    {% endif %}
                </td>

                <td>{{ row.Delegation }}</td>

                <td>
                    {% if row.Delegation_Criticalness == "High" %}
                        <span class="badge high">High</span>
                    {% elif row.Delegation_Criticalness == "Medium" %}
                        <span class="badge medium">Medium</span>
                    {% elif row.Delegation_Criticalness == "Low" %}
                        <span class="badge low">Low</span>
                    {% else %}
                        <span class="badge none">None</span>
                    {% endif %}
                </td>

            </tr>
            {% endfor %}
        </table>
    </div>
    
    <footer class="footer">
        <div class="footer-content">
            Built with curiosity & data • 
            <a href="https://github.com/shaunpimenta/Mumbai-AQI-VS-Delegation" target="_blank">
                View on GitHub
            </a>
        </div>
    </footer>

    <script>
        // Load data injected from Flask
        const rawData = {{ data | tojson | safe }};
        
        // Reverse array so the graph displays chronologically (oldest -> newest) left-to-right
        const chartData = [...rawData].reverse();

        const labels = chartData.map(d => d.Date);
        const aqiValues = chartData.map(d => d.AQI);
        
        // Map importance to your existing UI hex codes
        const backgroundColors = chartData.map(d => {
            if (d.Delegation_Criticalness === 'High') return '#ff4757';   // .high class
            if (d.Delegation_Criticalness === 'Medium') return '#ffa502'; // .medium class
            if (d.Delegation_Criticalness === 'Low') return '#2ed573';    // .low class
            return '#57606f'; // .none class
        });

        const ctx = document.getElementById('aqiChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'AQI Level',
                    data: aqiValues,
                    backgroundColor: backgroundColors,
                    borderRadius: 4,
                    borderWidth: 1,
                    borderColor: 'rgba(255, 255, 255, 0.1)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false // Disabled default legend to use the custom HTML legend
                    },
                    tooltip: {
                        callbacks: {
                            afterLabel: function(context) {
                                const dataIndex = context.dataIndex;
                                const delegation = chartData[dataIndex].Delegation;
                                const importance = chartData[dataIndex].Delegation_Criticalness;
                                if (delegation) {
                                    return `Delegation: ${delegation} (${importance})`;
                                }
                                return 'No Delegation';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)',
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
""", data=data)

if __name__ == "__main__":
    app.run(debug=True)