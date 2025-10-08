/*
charts.js - Global Chart Helper for Servisio

Purpose:
    Initializes and updates Chart.js graphs used across dashboards.

Usage:
    Included in base.html (after Bootstrap bundle).
    Can be called by any page that includes a <canvas> element.
*/

document.addEventListener("DOMContentLoaded", () => {
    const chartCanvas = document.getElementById("ticketChart");
    if (chartCanvas) {
        fetch("/admin/dashboard/data")
            .then(res => res.json())
            .then(data => {
                new Chart(chartCanvas, {
                    type: "doughnut",
                    data: {
                        labels: data.labels,
                        datasets: [{
                            data: data.values,
                            backgroundColor: ["#0d6efd", "#ffc107", "#198754"]
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: "bottom"
                            },
                            title: {
                                display: true,
                                text: "Ticket Status Overview"
                            }
                        }
                    }
                });
            });
    }
});
