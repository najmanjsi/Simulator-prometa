// --------------------------------------------------
// MAP
// --------------------------------------------------

const map = L.map('map', {
    zoomControl: false
}).setView([46.05, 14.5], 12);

// re-add zoom control bottom-right
L.control.zoom({
    position: 'bottomright'
}).addTo(map);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        attribution:
            '&copy; OpenStreetMap contributors'
    }
).addTo(map);


// --------------------------------------------------
// DATA
// --------------------------------------------------

let segmentsMap = new Map();

let edgeToSegments = {};

let layerGroup =
    L.layerGroup().addTo(map);


// --------------------------------------------------
// LOAD SEGMENTS
// --------------------------------------------------

async function loadSegments() {

    const response = await fetch('../data/geometry.json');
    const rows = await response.json();

    //console.log('Loaded segments:', rows.length);

    for (const row of rows) {

        segmentsMap.set(
            String(row.segment_id),
            row.geometry
        );
    }
}


// --------------------------------------------------
// LOAD EDGE MAPPING
// --------------------------------------------------

async function loadEdgeMapping() {

    const response =
        await fetch(
            '../data/edge2segments.json'
        );

    edgeToSegments =
        await response.json();

    //console.log('Loaded edge mapping');
}


// --------------------------------------------------
// DRAW SEGMENTS
// --------------------------------------------------

function drawSegments(segmentIds) {

    layerGroup.clearLayers();

    for (const segmentId of segmentIds) {

        const geometry =
            segmentsMap.get(
                String(segmentId)
            );

        if (!geometry)
            continue;

        const latlngs =
            geometry.map(p => [
                p[0],
                p[1]
            ]);

        L.polyline(latlngs, {

            color: 'red',

            weight: 4,

            opacity: 0.8

        })
        .bindPopup(
            `Segment: ${segmentId}`
        )
        .addTo(layerGroup);
    }
}


// --------------------------------------------------
// SHOW ALL
// --------------------------------------------------

function showAllSegments() {

    const segmentSet = new Set();

    let countSegments = 0;
    for (const edgeId in edgeToSegments) {

        const segments = edgeToSegments[edgeId];

        if (!segments) continue;

        for (const segmentId of segments) {

            segmentSet.add(String(segmentId));
            countSegments++;
        }
    }

    drawSegments(Array.from(segmentSet));
    //console.log(countSegments);
}


// --------------------------------------------------
// SHOW SELECTED EDGES
// --------------------------------------------------

function showSelectedEdges(edgeIds) {

    const segmentSet =
        new Set();

    for (const edgeId of edgeIds) {

        const segments =
            edgeToSegments[edgeId];

        if (!segments)
            continue;

        for (const segmentId of segments) {

            segmentSet.add(
                String(segmentId)
            );
        }
    }

    drawSegments(
        Array.from(segmentSet)
    );
}


// --------------------------------------------------
// UI
// --------------------------------------------------

function populateEdgeDropdown() {

    const select =
        document.getElementById('edgeSelect');

    select.innerHTML = '';

    for (const edgeId in edgeToSegments) {

        const option =
            document.createElement('option');

        option.value = edgeId;
        option.textContent = edgeId;

        select.appendChild(option);
    }
}


document
    .getElementById('edgeSearch')
    .addEventListener('input', (e) => {

        const query =
            e.target.value.toLowerCase();

        const options =
            document
                .getElementById('edgeSelect')
                .options;

        for (const opt of options) {

            opt.style.display =
                opt.value.toLowerCase()
                    .includes(query)
                ? ''
                : 'none';
        }
    });


document
    .getElementById('showBtn')
    .addEventListener('click', () => {

        const select =
            document.getElementById('edgeSelect');

        const selectedEdges =
            Array.from(select.selectedOptions)
                .map(opt => opt.value);

        showSelectedEdges(selectedEdges);
    });


document
    .getElementById('showAllBtn')
    .addEventListener('click', () => {

        showAllSegments();
    });


// --------------------------------------------------
// INIT
// --------------------------------------------------

async function init() {

    await loadSegments();

    await loadEdgeMapping();

    populateEdgeDropdown();

    showAllSegments();
}

init();