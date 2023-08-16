function addRow() {
    var rows = document.querySelector('#rows');
    var row = document.createElement('div');
    row.className = 'row';

    var nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.name = 'names_expenses[]';
    nameInput.placeholder = 'Enter name';
    row.appendChild(nameInput);

    var expenseInput = document.createElement('input');
    expenseInput.type = 'number';
    expenseInput.name = 'names_expenses[]';
    expenseInput.placeholder = 'Enter expense';
    row.appendChild(expenseInput);

    rows.appendChild(row);

    [nameInput, expenseInput].forEach(function(input) {
        input.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                if (event.shiftKey) {
                    document.querySelector('form').dispatchEvent(new Event('submit'));
                } else {
                    addRow();
                }
            }
        });
    });

    nameInput.focus();
}



document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    fetch('/calculate', {
        method: 'POST',
        body: new FormData(this)
    })
    .then(response => response.text())
    .then(result => {
        document.querySelector('#result').innerHTML = result;
    });
});

document.querySelectorAll('input').forEach(function(input) {
    input.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (event.shiftKey) {
                document.querySelector('form').dispatchEvent(new Event('submit'));
            } else {
                addRow();
            }
        }
    });
});