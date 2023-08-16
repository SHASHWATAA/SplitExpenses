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

function addRowWithName(name) {
    var rows = document.querySelectorAll('.row');
    var firstRow = rows[0];
    var firstNameInput = firstRow.querySelector('input[type=text]');
    var firstExpenseInput = firstRow.querySelector('input[type=number]');
    if (firstNameInput.value === '') {
        firstNameInput.value = name;
        firstExpenseInput.focus();
    } else {
        addRow();
        var rows = document.querySelectorAll('.row')
        var lastRow = rows[rows.length - 1];
        var nameInput = lastRow.querySelector('input[type=text]');
        var expenseInput = lastRow.querySelector('input[type=number]');
        nameInput.value = name;
        expenseInput.focus();
    }
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
