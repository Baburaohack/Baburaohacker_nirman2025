document.addEventListener('DOMContentLoaded', function () {
    const machineCardsContainer = document.getElementById('machine-cards');
    const userInfoForm = document.getElementById('user-info-form');
    const userInfoDisplay = document.getElementById('user-info');
    const displayName = document.getElementById('display-name');
    const displayCompany = document.getElementById('display-company');
    const displayIndustry = document.getElementById('display-industry');
    const displayTagline = document.getElementById('display-tagline');

    // Default thresholds
    let thresholds = {
        cpuUtilization: 90,
        memoryUsage: 90,
        airTemperature: 300,
        diskIO: 4500,
        networkLatency: 50,
        powerConsumption: 500,
        vibrationLevel: 2.0,
        coolingEfficiency: 60,
        networkThroughput: 200
    };

    // Weights for each parameter in failure probability calculation
    const weights = {
        cpuUtilization: 0.2,
        memoryUsage: 0.2,
        airTemperature: 0.15,
        diskIO: 0.1,
        networkLatency: 0.1,
        powerConsumption: 0.1,
        vibrationLevel: 0.1,
        coolingEfficiency: 0.05,
        networkThroughput: 0.05
    };

    // Function to generate random data for a machine
    function generateRandomMachineData(machineId) {
        return {
            UDI: machineId,
            'CPU Utilization [%]': Math.floor(Math.random() * 101), // 0-100%
            'Memory Usage [%]': Math.floor(Math.random() * 101), // 0-100%
            'Air Temperature [K]': Math.floor(Math.random() * 21) + 290, // 290-310K
            'Disk I/O Operations': Math.floor(Math.random() * 5001), // 0-5000
            'Network Latency [ms]': Math.floor(Math.random() * 61), // 0-60ms
            'Power Consumption [W]': Math.floor(Math.random() * 601), // 0-600W
            'Vibration Level [g]': (Math.random() * 2.5).toFixed(2), // 0-2.5g
            'Cooling Efficiency [%]': Math.floor(Math.random() * 101), // 0-100%
            'Network Throughput [Mbps]': Math.floor(Math.random() * 1001) // 0-1000Mbps
        };
    }

    // Function to calculate failure probability and reason
    function calculateFailureProbability(machine) {
        let probability = 0;
        const reasons = [];

        // Check each parameter against its threshold
        if (machine['CPU Utilization [%]'] > thresholds.cpuUtilization) {
            probability += weights.cpuUtilization;
            reasons.push('High CPU Utilization');
        }
        if (machine['Memory Usage [%]'] > thresholds.memoryUsage) {
            probability += weights.memoryUsage;
            reasons.push('High Memory Usage');
        }
        if (machine['Air Temperature [K]'] > thresholds.airTemperature) {
            probability += weights.airTemperature;
            reasons.push('High Air Temperature');
        }
        if (machine['Disk I/O Operations'] > thresholds.diskIO) {
            probability += weights.diskIO;
            reasons.push('High Disk I/O');
        }
        if (machine['Network Latency [ms]'] > thresholds.networkLatency) {
            probability += weights.networkLatency;
            reasons.push('High Network Latency');
        }
        if (machine['Power Consumption [W]'] > thresholds.powerConsumption) {
            probability += weights.powerConsumption;
            reasons.push('High Power Consumption');
        }
        if (machine['Vibration Level [g]'] > thresholds.vibrationLevel) {
            probability += weights.vibrationLevel;
            reasons.push('High Vibration Level');
        }
        if (machine['Cooling Efficiency [%]'] < thresholds.coolingEfficiency) {
            probability += weights.coolingEfficiency;
            reasons.push('Low Cooling Efficiency');
        }
        if (machine['Network Throughput [Mbps]'] < thresholds.networkThroughput) {
            probability += weights.networkThroughput;
            reasons.push('Low Network Throughput');
        }

        // Cap probability at 100%
        probability = Math.min(probability, 1);

        return { probability, reasons };
    }

    // Function to update machine data and charts
    function updateMachineData(machines, charts) {
        machines.forEach((machine, index) => {
            const newData = generateRandomMachineData(machine.UDI);
            const { probability, reasons } = calculateFailureProbability(newData);

            // Update the displayed stats
            const card = machineCardsContainer.children[index];
            card.querySelector('.cpu-utilization').textContent = `${newData['CPU Utilization [%]']}%`;
            card.querySelector('.memory-usage').textContent = `${newData['Memory Usage [%]']}%`;
            card.querySelector('.air-temperature').textContent = `${newData['Air Temperature [K]']}K`;
            card.querySelector('.disk-io').textContent = newData['Disk I/O Operations'];
            card.querySelector('.network-latency').textContent = `${newData['Network Latency [ms]']}ms`;
            card.querySelector('.power-consumption').textContent = `${newData['Power Consumption [W]']}W`;
            card.querySelector('.vibration-level').textContent = `${newData['Vibration Level [g]']}g`;
            card.querySelector('.cooling-efficiency').textContent = `${newData['Cooling Efficiency [%]']}%`;
            card.querySelector('.network-throughput').textContent = `${newData['Network Throughput [Mbps]']}Mbps`;
            card.querySelector('.failure-probability').textContent = `${(probability * 100).toFixed(2)}%`;
            card.querySelector('.failure-reasons').textContent = reasons.join(', ') || 'None';

            // Show alert if failure probability is high
            if (probability > 0.7) {
                alert(`Machine ${machine.UDI} has a high failure probability (${(probability * 100).toFixed(2)}%). Reasons: ${reasons.join(', ')}`);
            }

            // Update the chart data
            const chart = charts[index];
            chart.data.datasets[0].data = [
                newData['CPU Utilization [%]'],
                newData['Memory Usage [%]'],
                newData['Air Temperature [K]'],
                newData['Disk I/O Operations'],
                newData['Network Latency [ms]'],
                newData['Power Consumption [W]'],
                newData['Vibration Level [g]'],
                newData['Cooling Efficiency [%]'],
                newData['Network Throughput [Mbps]']
            ];
            chart.update();
        });
    }

    // Function to create a machine card
    function createMachineCard(machine) {
        const card = document.createElement('div');
        card.className = 'bg-white p-6 rounded-lg shadow-lg card-hover';
        card.innerHTML = `
            <h2 class="text-xl font-bold mb-4">Machine ${machine.UDI}</h2>
            <canvas id="machine-${machine.UDI}-chart" class="mb-4"></canvas>
            <p class="text-sm"><span class="font-semibold tooltip">CPU Utilization<span class="tooltiptext">Percentage of CPU usage</span>:</span> <span class="cpu-utilization">${machine['CPU Utilization [%]']}%</span></p>
            <p class="text-sm"><span class="font-semibold tooltip">Memory Usage<span class="tooltiptext">Percentage of memory usage</span>:</span> <span class="memory-usage">${machine['Memory Usage [%]']}%</span></p>
            <p class="text-sm"><span class="font-semibold tooltip">Air Temperature<span class="tooltiptext">Temperature in Kelvin</span>:</span> <span class="air-temperature">${machine['Air Temperature [K]']}K</span></p>
            <p class="text-sm"><span class="font-semibold tooltip">Disk I/O Operations<span class="tooltiptext">Number of disk I/O operations</span>:</span> <span class="disk-io">${machine['Disk I/O Operations']}</span></p>
            <p class="text-sm"><span class="font-semibold tooltip">Network Latency<span class="tooltiptext">Latency in milliseconds</span>:</span> <span class="network-latency">${machine['Network Latency [ms]']}ms</span></p>
            <p class="text-sm"><span class="font-semibold tooltip">Power Consumption<span class="tooltiptext">Power usage in watts</span>:</span> <span class="power-consumption">${machine['Power Consumption [W]']}W</span></p>
            <p class="text-sm"><span class="font-semibold tooltip">Vibration Level<span class="tooltiptext">Vibration level in g</span>:</span> <span class="vibration-level">${machine['Vibration Level [g]']}g</span></p>
            <p class="text-sm"><span class="font-semibold tooltip">Cooling Efficiency<span class="tooltiptext">Cooling efficiency percentage</span>:</span> <span class="cooling-efficiency">${machine['Cooling Efficiency [%]']}%</span></p>
            <p class="text-sm"><span class="font-semibold tooltip">Network Throughput<span class="tooltiptext">Throughput in Mbps</span>:</span> <span class="network-throughput">${machine['Network Throughput [Mbps]']}Mbps</span></p>
            <p class="text-sm"><span class="font-semibold">Failure Probability:</span> <span class="failure-probability">0%</span></p>
            <p class="text-sm"><span class="font-semibold">Failure Reasons:</span> <span class="failure-reasons">None</span></p>
        `;
        return card;
    }

    // Function to initialize a chart for a machine
    function initializeChart(machine) {
        const ctx = document.getElementById(`machine-${machine.UDI}-chart`).getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['CPU Utilization', 'Memory Usage', 'Air Temperature', 'Disk I/O', 'Network Latency', 'Power Consumption', 'Vibration Level', 'Cooling Efficiency', 'Network Throughput'],
                datasets: [{
                    label: `Machine ${machine.UDI} Metrics`,
                    data: [
                        machine['CPU Utilization [%]'],
                        machine['Memory Usage [%]'],
                        machine['Air Temperature [K]'],
                        machine['Disk I/O Operations'],
                        machine['Network Latency [ms]'],
                        machine['Power Consumption [W]'],
                        machine['Vibration Level [g]'],
                        machine['Cooling Efficiency [%]'],
                        machine['Network Throughput [Mbps]']
                    ],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Initialize the dashboard with 5 machines (this will be shown only after the form is submitted)
    const machines = [];
    const charts = [];

    userInfoForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const userName = document.getElementById('user-name').value;
        const companyName = document.getElementById('company-name').value;
        const industry = document.getElementById('industry').value;
        const tagline = document.getElementById('tagline').value;

        // Display user information
        displayName.textContent = userName;
        displayCompany.textContent = companyName;
        displayIndustry.textContent = industry;
        displayTagline.textContent = tagline;
        userInfoDisplay.classList.remove('hidden');

        // Optionally, you can hide the form after submission
        userInfoForm.classList.add('hidden');

        // Initialize the dashboard (this code will be executed after form submission)
        for (let i = 1; i <= 5; i++) {
            const machine = generateRandomMachineData(i);
            machines.push(machine);
            const card = createMachineCard(machine);
            machineCardsContainer.appendChild(card);
            const chart = initializeChart(machine);
            charts.push(chart);
        }

        // Show the machine cards dashboard
        machineCardsContainer.classList.remove('hidden');

        // Update data every 2 seconds
        setInterval(() => updateMachineData(machines, charts), 2000);
    });
});
