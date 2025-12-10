// static/main.js

// Initialize map
const map = L.map('map').setView([0, 0], 3); // Center at the equator, zoom level 3

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Define a custom sailing boat icon
const sailingBoatIcon = L.icon({
  iconUrl: 'static/sailing-boat.png', // Path to your sailing boat icon
  iconSize: [32, 32], // Size of the icon
  iconAnchor: [16, 32], // Anchor point of the icon (bottom center)
  popupAnchor: [0, -32] // Point where the popup should open relative to the icon
});

// Helper function to convert degrees/minutes to decimal
function convertToDecimal(coord) {
  const match = coord.match(/^(\d+)°([\d.]+)'([NSEW])$/);
  if (!match) {
    console.error('Invalid coordinate:', coord);
    return null;
  }

  const degrees = parseInt(match[1], 10);
  const minutes = parseFloat(match[2]);
  const direction = match[3];

  let decimal = degrees + (minutes / 60);
  if (direction === 'S' || direction === 'W') {
    decimal = -decimal;
  }
  return decimal;
}

// Fetch API data
const apiKey = 'cm44faxbx0000rkg5qsqg17hr'; // Replace with your API key
fetch(`https://www.vendeeglobeapi.com/api/vgdata?apikey=${apiKey}`)
  .then(response => response.json())
  .then(data => {
    const boats = data.latestdata.data;

    boats.forEach(boat => {
      const lat = convertToDecimal(boat.Latitude);
      const lon = convertToDecimal(boat.Longitude);

      if (lat !== null && lon !== null) {
        // Add custom sailing boat markers for each boat
        const marker = L.marker([lat, lon], { icon: sailingBoatIcon }).addTo(map);

        // Add popup info
        const popupContent = `
          <div class="boat-popup">
            <strong>${boat.Boat}</strong><br>
            Skipper: ${boat.Skipper_Boat}<br>
            Rank: ${boat.Rank}<br>
            Speed: ${boat.Speed_LastReport} kts<br>
            Heading: ${boat.Heading_LastReport}°<br>
            <img src="${boat.CountryFlag}" alt="${boat.Country} Flag">
          </div>
        `;
        marker.bindPopup(popupContent);
      }
    });

    // Adjust map bounds to fit all markers
    const bounds = boats
      .map(boat => {
        const lat = convertToDecimal(boat.Latitude);
        const lon = convertToDecimal(boat.Longitude);
        return lat !== null && lon !== null ? [lat, lon] : null;
      })
      .filter(Boolean);

    if (bounds.length) {
      map.fitBounds(bounds);
    }
  })
  .catch(error => console.error('Error fetching API data:', error));

