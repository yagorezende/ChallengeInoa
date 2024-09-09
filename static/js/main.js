// Validation for the login form
(function () {
    'use strict'
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
})();

// start create monitor select options
$(document).ready(function () {
    loadList('/api/v1/stock/', {page_size: 5}, function (options) {
        // fill the dropdown with options
        options.forEach(option => {
            $('#dropdownOptions').append(`<a href="#" data-stock-id="${option.id}" onclick="setSelectedStock(this)" class="list-group-item list-group-item-action">${option.symbol} - ${option.company_name}</a>`);
        });
    });
});

// Dropdown search box
$(document).ready(function () {
    $('#searchBox').on('input', function () {
        let query = {
            search: $(this).val(),
            page_size: 5, // you can adjust this based on your needs
        }
        loadList('/api/v1/stock/', query, function (options) {
            $('#dropdownOptions').empty();
            // deal with empty options
            if (options.length === 0) {
                $('#dropdownOptions').append(`<a href="#" class="list-group-item list-group-item-action">Ativo não encontrado</a>`);
                return;
            }
            // fill the dropdown with options
            options.forEach(option => {
                $('#dropdownOptions').append(`<a href="#" data-stock-id="${option.id}" onclick="setSelectedStock(this)" class="list-group-item list-group-item-action">${option.symbol} - ${option.company_name}</a>`);
            });
        });
    });
});

// money mask
$(document).ready(function () {
    var maskOptions = {
        mask: Number,
        scale: 2,
        signed: false,
        thousandsSeparator: '',
        padFractionalZeros: true,
        normalizeZeros: true,
        radix: '.',
        mapToRadix: [','],
        min: 0,
        max: Number.MAX_SAFE_INTEGER,
        reverse: true
    };
    $('.money-mask').each(function () {
        IMask(this, maskOptions)
    });
});

// send form with auth token
$(document).ready(function () {
    $('#createMonitorForm').submit(function (event) {
        loadingAnimation();
        event.preventDefault();
        let jsonData = {
            stock: $('#stockId').val(),
            price_limit_top: $('#price_limit_top').val(),
            price_limit_bottom: $('#price_limit_bottom').val(),
            interval: $('#intervalSelect').val(),
            notify: $('#notify').is(':checked'),
        }

        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: JSON.stringify(jsonData),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'token ' + getCookie('token'),
            },
            success: function (response) {
                showAlert('success', "Monitor criado com sucesso!");
                loadingAnimation(false);
                // reset form
                $('#createMonitorForm').trigger('reset');
                // close modal
                $('#createMonitorModal').toggle();

                // reload the page after 2 seconds
                setTimeout(function () {
                    location.reload();
                }, 2000);
            },
            error: function (response) {
                // show error message using bootstrap alert
                showAlert('danger', "Erro ao criar monitor. Tente novamente mais tarde.");
                loadingAnimation(false);
                $('#createMonitorModal').toggle();
            }
        });
    });
});


// BEGIN OF [HELPER FUNCTIONS]

/***
 * Function to get the value of a cookie
 * @param name - The name of the cookie
 * @returns {null|*} - The value of the cookie
 * */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/***
 * Function to load any list from the API
 * @param endpoint - The endpoint to be called
 * @param query - The query parameters to be sent
 * @param callback - The function to be called when the request is successful
 */
function loadList(endpoint, query, callback) {
    $.ajax({
        url: endpoint,
        method: 'GET',
        data: query,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + getCookie('token'),
        },
        success: function (response) {
            callback(response.results);
        },
        error: function (response) {
            callback([]);
        }
    });
}

async function getStockPriceNow(stockId) {
    let price = {};
    loadingAnimation();
    await $.ajax({
        url: `/api/v1/stock-price/now/${stockId}/`,
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + getCookie('token'),
        },
        success: function (response) {
            price = response?.price;
            loadingAnimation(false);
        },
        error: function (response) {
            loadingAnimation(false);
        }
    });
    return price;
}

/***
 * Function to set the selected stock in the form
 * @param element - The element that was clicked
 * */
async function setSelectedStock(element) {
    $('#stockId').val($(element).data('stock-id'));
    $('#stocksDropdown').text($(element).text());
    getStockPriceNow($(element).data('stock-id')).then(price => {
        $('#stocksDropdown').text($(element).text() + ` - R$ ${price?.regularMarketPrice}`);
        // TODO: review to a better way to calculate the variation
        var variation = Math.abs(price?.regularMarketChangePercent) * 1.5;
        console.log("Variation --> ", variation);
        // get absolute value
        $('#price_limit_top').val((price?.regularMarketPrice + variation).toFixed(2));
        $('#price_limit_bottom').val((price?.regularMarketPrice - variation).toFixed(2));
    });
}

function showAlert(type, message) {
    $('.alert-' + type + ' .alert-msg').text(message);
    $('.alert-' + type).attr('hidden', false);
    $('.alert-' + type).addClass('show');

    // hide the alert after 5 seconds
    setTimeout(function () {
        $('.alert-' + type).removeClass('show');
        $('.alert-' + type).attr('hidden', true);
    }, 5000);
}

function loadingAnimation(on = true) {
    if (on) {
        $("#loadingBackdrop").addClass('active'); // Show the backdrop and spinner
        // Hide the loading backdrop after 5 seconds as a backup of errors
        setTimeout(function () {
            $("#loadingBackdrop").removeClass('active');// Hide the backdrop and spinner
        }, 5000);
        return;
    }
    $("#loadingBackdrop").removeClass('active');// Hide the backdrop and spinner


}

// END OF [HELPER FUNCTIONS]