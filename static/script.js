const examples = {
    basic:
`# Basic arithmetic operations
plant a 10
plant b 5

tend a
water 15     # a = 10 + 15 = 25
prune 7      # a = 25 - 7 = 18
harvest a

tend b
graft 3      # b = 5 * 3 = 15
divide 2     # b = 15 / 2 = 7 (integer division)
harvest b`,
    
    loop: 
`# Calculate 2^4 (2*2*2*2)
plant base 2
plant exponent 4
plant result 1
plant one 1

bloom exponent PowerLoop

label PowerLoop
tend result
graft base
tend exponent
prune one
wither

tend result
harvest`,
    
    function:
`# Function example
function test [a] {
return 42
}

call test 0
harvest return`,
    
    weather:
`# Using weather effects
plant growth 10
weather sunny
tend growth
graft 2
harvest growth   # Output: 20

weather rainy
tend growth
divide 4
graft 3
harvest growth   # Output: 15

weather stormy
tend growth
plant growth 5
harvest growth   # Output: 5`,
    string:
`# String manipulation example
plant msg "Hello, World!"
tend msg
harvest msg`
};

document.getElementById('examples').addEventListener('change', function() {
    const exampleKey = this.value;
    if (exampleKey && examples[exampleKey]) {
        document.getElementById('editor').value = examples[exampleKey];
        document.getElementById('examples').value = "";
    }
});

function runCode() {
    const code = document.getElementById('editor').value;
    const outputDiv = document.getElementById('output');
    const statusEl = document.getElementById('status');
    const placeholder = document.getElementById('output-placeholder');
    
    outputDiv.innerHTML = '';
    outputDiv.className = '';
    placeholder.style.display = 'block';
    
    statusEl.textContent = 'Running...';
    statusEl.className = 'status active';
    statusEl.style.background = '#e1f5fe';
    statusEl.style.color = '#0288d1';
    
    const runBtn = document.querySelector('.btn-run');
    runBtn.disabled = true;
    runBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';
    
    fetch('/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server responded with error');
        }
        return response.json();
    })
    .then(data => {
        placeholder.style.display = 'none';
        
        if (data.error) {
            outputDiv.innerHTML = `<div class="error">ERROR: ${data.error}</div>`;
            statusEl.textContent = 'Error';
            statusEl.style.background = 'rgba(231, 76, 60, 0.1)';
            statusEl.style.color = '#e74c3c';
        } else {
            outputDiv.textContent = data.harvest || "Program executed successfully (no output)";
            statusEl.textContent = 'Completed';
            statusEl.style.background = 'rgba(39, 174, 96, 0.1)';
            statusEl.style.color = '#27ae60';
        }
    })
    .catch(error => {
        placeholder.style.display = 'none';
        outputDiv.innerHTML = `<div class="error">NETWORK ERROR: ${error.message}</div>`;
        statusEl.textContent = 'Failed';
        statusEl.style.background = 'rgba(231, 76, 60, 0.1)';
        statusEl.style.color = '#e74c3c';
    })
    .finally(() => {
        runBtn.disabled = false;
        runBtn.innerHTML = '<i class="fas fa-play"></i> Run Code';
        
        setTimeout(() => {
            statusEl.classList.remove('active');
        }, 3000);
    });
}

const editor = document.getElementById('editor');
editor.addEventListener('input', function() {
    this.style.color = '#2d3436';
});

editor.addEventListener('focus', function() {
    document.getElementById('output-placeholder').style.display = 'none';
});