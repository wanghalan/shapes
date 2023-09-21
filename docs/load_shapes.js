// Main function to initialize the app
const loadData = () => {
    fetch('https://raw.githubusercontent.com/wanghalan/shapes/main/data/testing/va_combined.topojson')
    .then((response) => response.json())
    .then((json) => console.log(json));
};

// Initialize the app
loadData();
