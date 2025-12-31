document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const form = document.getElementById('ping-form');
    const output = document.getElementById('output');
    const historyBody = document.getElementById('history-body');
    const statLatency = document.getElementById('stat-latency');
    const statLoss = document.getElementById('stat-loss');

    let latencies = [];
    let received = 0;
    let sent = 0;

    const appendOutput = (text, type = '') => {
        const div = document.createElement('div');
        div.className = `output-line ${type}`;
        div.textContent = text;
        output.appendChild(div);
        output.scrollTop = output.scrollHeight;
    };

    const updateHistory = async () => {
        try {
            const resp = await fetch('/api/history?limit=10');
            const data = await resp.json();
            historyBody.innerHTML = '';
            data.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${item.host}</td>
                    <td>${item.avg} ms</td>
                    <td><span class="status-badge ${item.loss > 0 ? 'status-down' : 'status-up'}">${item.loss}%</span></td>
                    <td style="color: var(--text-secondary); font-size: 0.8rem;">${item.timestamp}</td>
                `;
                historyBody.appendChild(tr);
            });
        } catch (err) {
            console.error('Failed to fetch history:', err);
        }
    };

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const host = document.getElementById('host').value;
        const count = document.getElementById('count').value;
        const size = document.getElementById('size').value;

        output.innerHTML = '';
        appendOutput(`Initiating probe to ${host}...`);

        latencies = [];
        received = 0;
        sent = parseInt(count);

        socket.emit('start_ping', { host, count, size });

        document.getElementById('submit-btn').disabled = true;
        document.getElementById('submit-btn').textContent = 'Probing...';
    });

    socket.on('ping_update', (data) => {
        if (data.latency !== null) {
            latencies.append(data.latency);
            received++;
            appendOutput(`✔ ${data.line}`, 'success');

            const avg = latencies.reduce((a, b) => a + b, 0) / latencies.length;
            statLatency.textContent = avg.toFixed(2);
        } else {
            appendOutput(`✘ ${data.line}`, 'error');
        }

        const loss = ((sent - received) / sent) * 100;
        statLoss.textContent = `${loss.toFixed(1)}%`;
    });

    socket.on('ping_complete', () => {
        appendOutput('Probe operation completed.');
        document.getElementById('submit-btn').disabled = false;
        document.getElementById('submit-btn').textContent = 'Start Diagnosis';
        updateHistory();
    });

    socket.on('ping_error', (data) => {
        appendOutput(`Error: ${data.message}`, 'error');
        document.getElementById('submit-btn').disabled = false;
        document.getElementById('submit-btn').textContent = 'Start Diagnosis';
    });

    // Initial history load
    updateHistory();
});
