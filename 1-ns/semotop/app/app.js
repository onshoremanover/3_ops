// app.js

// --- 1. Define RD New (EPSG:28992) CRS ------------------------

// Resolutions for the Dutch RD tiling scheme
const rdResolutions = [
    3440.64, 1720.32, 860.16, 430.08,
    215.04, 107.52, 53.76, 26.88,
    13.44, 6.72, 3.36, 1.68,
    0.84, 0.42
];

// Define CRS using proj4 + proj4leaflet
const rdCrs = new L.Proj.CRS(
    "EPSG:28992",
    "+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 " +
    "+k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel " +
    "+towgs84=565.2369,50.0087,465.658,-0.406857,0.350732,-1.87035,4.0812 " +
    "+units=m +no_defs",
    {
        origin: [-285401.92, 903401.92],
        resolutions: rdResolutions
    }
);

// --- 2. Create map in RD --------------------------------------

// RD coordinates of NL approx centre (155000, 463000)
const rdCenter = L.point(155000, 463000);

const map = L.map("map", {
    crs: rdCrs,
    center: rdCrs.projection.unproject(rdCenter),
    zoom: 7,                              // RD zoom index
    minZoom: 3,                           // WMS tiles only available from zoom 3+
    maxZoom: rdResolutions.length - 1     // 13
});

// Helper to create WMS layers with zoom bands
function makeWmsLayer(baseUrl, layerName, minZ, maxZ, attribution) {
    return L.tileLayer.wms(baseUrl, {
        layers: layerName,
        format: "image/png",
        transparent: true,
        version: "1.3.0",
        styles: "",
        minZoom: minZ,
        maxZoom: maxZ,
        attribution
    });
}

// --- 3. PDOK endpoints ----------------------------------------

const TOPRASTER_WMS = "https://service.pdok.nl/brt/topraster/wms/v1_0?";
const TOP10NL_WMS = "https://service.pdok.nl/brt/top10nl/wms/v1_0?";

// --- 4. Define TOPraster + TOP10NL layers ----------------------
//
// Zoom bands overlap so there is always at least one visible.
// Zoom levels shifted down by 2 to start at level 1

// 1:1,000,000 – very small scale
const top1000 = makeWmsLayer(TOPRASTER_WMS, "top1000raster", 1, 3, "TOPraster 1:1M");

// 1:500,000 – small scale, overlaps 1M and 1:250k
const top500 = makeWmsLayer(TOPRASTER_WMS, "top500raster", 2, 4, "TOPraster 1:500k");

// 1:250,000 – regional
const top250 = makeWmsLayer(TOPRASTER_WMS, "top250raster", 3, 6, "TOPraster 1:250k");

// 1:100,000 – province-ish
const top100 = makeWmsLayer(TOPRASTER_WMS, "top100raster", 5, 8, "TOPraster 1:100k");

// 1:50,000 – local region
const top50 = makeWmsLayer(TOPRASTER_WMS, "top50raster", 7, 10, "TOPraster 1:50k");

// 1:25,000 – detailed topo
const top25 = makeWmsLayer(TOPRASTER_WMS, "top25raster", 9, 12, "TOPraster 1:25k");

// TOP10NL – highest detail
const top10 = makeWmsLayer(TOP10NL_WMS, "top10nl", 11, 13, "TOP10NL");

// Add them all; minZoom/maxZoom decides when they actually draw
[top1000, top500, top250, top100, top50, top25, top10].forEach(layer => layer.addTo(map));

// --- 5. Bicycle network layer (optional overlay) --------------

const FIETSNETWERK_WMS = "https://service.pdok.nl/fietsplatform/regionale-fietsnetwerken/wms/v1_0?";

const bikeLayer = L.tileLayer.wms(FIETSNETWERK_WMS, {
    layers: "fietsknooppunten",
    format: "image/png",
    transparent: true,
    version: "1.3.0",
    styles: "",
    opacity: 1.0,
    attribution: "PDOK Fietsnetwerk"
});

// Toggle control for bicycle layer
const bikeCheckbox = document.getElementById("bike-toggle");
if (bikeCheckbox) {
    bikeCheckbox.addEventListener("change", (e) => {
        if (e.target.checked) {
            map.addLayer(bikeLayer);
        } else {
            map.removeLayer(bikeLayer);
        }
    });
}

// --- 6. Debug: log RD zoom level on change --------------------

map.on("zoomend", () => {
    console.log("RD zoom:", map.getZoom());
});