document.addEventListener('DOMContentLoaded', function () {
    const priceSliderElement = document.getElementById('price-slider');
    const hiddenMinPrice = document.getElementById('hidden_min_price');
    const hiddenMaxPrice = document.getElementById('hidden_max_price');
    const minPriceDisplay = document.getElementById('min-price-display');
    const maxPriceDisplay = document.getElementById('max-price-display');

    const configScriptElement = document.getElementById('price-slider-js-config-data');
    if (!configScriptElement) {
        console.error('Price slider configuration data not found!');
        return;
    }
    const config = JSON.parse(configScriptElement.textContent);

    let overallMin = parseFloat(config.overallMin);
    let overallMax = parseFloat(config.overallMax);
    let initialMin = parseFloat(config.initialMin);
    let initialMax = parseFloat(config.initialMax);

    overallMin = isNaN(overallMin) ? 0 : overallMin;
    overallMax = isNaN(overallMax) ? 1000 : overallMax;
    initialMin = isNaN(initialMin) ? overallMin : initialMin;
    initialMax = isNaN(initialMax) ? overallMax : initialMax;
    
    initialMin = Math.max(overallMin, Math.min(initialMin, overallMax));
    initialMax = Math.min(overallMax, Math.max(initialMax, initialMin));

    if (priceSliderElement) {
        noUiSlider.create(priceSliderElement, {
            start: [initialMin, initialMax],
            connect: true,
            range: {
                'min': overallMin,
                'max': overallMax
            },
            step: 1, 
            format: {
                to: function (value) {
                    return value.toFixed(2);
                },
                from: function (value) {
                    return Number(value);
                }
            }
        });

        priceSliderElement.noUiSlider.on('update', function (values, handle) {
            const minValue = values[0];
            const maxValue = values[1];

            if (minPriceDisplay) {
                 minPriceDisplay.textContent = '$' + minValue;
            }
            if (maxPriceDisplay) {
                maxPriceDisplay.textContent = '$' + maxValue;
            }
            if (hiddenMinPrice) {
                hiddenMinPrice.value = minValue;
            }
            if (hiddenMaxPrice) {
                hiddenMaxPrice.value = maxValue;
            }
        });
    } 
});