const BAR_COUNT = 50;

$(document).ready(function () {
    // get all page chart canvas
    let chartCanvas = $(".stock-chart");
    console.log(`found ${chartCanvas.length} canvas`);
    // foreach canva
    chartCanvas.each(function (index, element) {
        // get monitor id
        let monitorId = $(element).data('monitor-id');
        // get chart context
        let chartContext = element.getContext('2d');
        // create chart
        createChart(chartContext, monitorId);
        console.log(`created chart ${monitorId}`);
    });
});

async function loadMonitorData(monitorId) {
    let params = `monitor=${monitorId}&points=${BAR_COUNT}`;

    let response = await fetch(`/api/v1/user-monitor-stock-data/?${params}`, {
        method: 'GET',
        headers: {
            'Authorization': 'token ' + getCookie('token'),
        },
    });
    return await response.json();
}

function updateChartCard(monitorId, data){
    let current_price = data.prices.length ? data.prices[0] : null;

    let up_triangle = `<i class="fas fa-caret-up"></i>`;
    let down_triangle = `<i class="fas fa-caret-down"></i>`;

    if(current_price) {
        $(`#monitor-${monitorId}-current-price`).html(current_price.price + ' ' + (current_price.price > current_price.open_price ? up_triangle : down_triangle));
        $(`#monitor-${monitorId}-current-price`).css('color', current_price.price > current_price.open_price ? 'green' : 'red');

        $(`#monitor-${monitorId}-open-price`).text(current_price.open_price);

        let variation = current_price.price - current_price.open_price;
        let variation_percent = (variation / current_price.open_price) * 100;
        $(`#monitor-${monitorId}-variation-price`).text(variation.toFixed(2) + ' (' + variation_percent.toFixed(2) + '%)');
    }
}

async function createChart(chartContext, monitorId) {
    let data = await loadMonitorData(monitorId);
    updateChartCard(monitorId, data);
    console.log(data);

    let barData = data.prices.map(stockToBarData);

    // convert timestamp to show hours only
    data.prices.forEach(stock => {
        let date = new Date(stock.timestamp);
        stock.timestamp = date.getHours() + ':' + date.getMinutes();
    });

    console.log(barData);
    let lineData = data.prices.map(stock => {
        return {x: stock.timestamp, y: stock.price}
    });
    let top_line = data.prices.map(obj => {
        return {x: obj.timestamp, y: data.price_limit_top}
    });
    let bottom_line = data.prices.map(obj => {
        return {x: obj.timestamp, y: data.price_limit_bottom}
    });

    chartContext.canvas.width = '10rem';
    chartContext.canvas.height = '10rem';


    let chart = new Chart(chartContext, {
        type: 'linear',
        data: {
            datasets: [
                // {
                //     label: 'Ativo',
                //     data: barData,
                // }
                {
                    label: 'Valor do Ativo',
                    type: 'line',
                    data: lineData,
                    borderColor: 'rgb(85,196,199)',
                },
                // Top limit line dataset
                {
                    label: 'Limite para Venda',
                    type: 'line',
                    data: top_line,
                    borderColor: 'rgb(0,131,12)',
                    borderWidth: 1.5,
                    borderDash: [5, 5],
                    pointRadius: 0,
                },
                // Bottom limit line dataset
                {
                    label: 'Limite para Compra',
                    data: bottom_line,
                    type: 'line',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1.5,
                    borderDash: [5, 5],
                    pointRadius: 0,
                }
            ]
        }
    });
    chart.update();
}

function stockToBarData(stock) {
    return {
        x: stock.timestamp.valueOf(),
        o: parseFloat(stock.open_price),
        h: parseFloat(stock.high_price),
        l: parseFloat(stock.low_price),
        c: parseFloat(stock.close_price)
    };
}