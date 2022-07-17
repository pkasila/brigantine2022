import generateText from "./generateText";

let dataset = [];

fetch('/imgs/dataset.json')
    .then(r => r.json())
    .then(r => {
        dataset = r;
        dispatchEvent(new Event('loadedDataset'));
    });

window.handleImageLoad = (evt) => {
    const interval = setInterval(() => {
        const img = document.getElementById('formula');
        if (img.naturalWidth > 0 && img.naturalHeight > 0) {
            clearInterval(interval);
            dispatchEvent(new Event('renderDone'));
        }
    }, 20);
}

function render(idx) {
    let words = generateText(50);

    const image = `<img id="formula" onload="handleImageLoad()" class="formula" src="/imgs/${dataset.images[idx].file}" alt="Formula">`;

    if (Math.random() > 0.5) {
        words[0] = `<strong>${words[0].charAt(0).toUpperCase() + words[0].slice(1)}</strong>`;
    } else {
        words[0] = words[0].charAt(0).toUpperCase() + words[0].slice(1);
    }

    let splitIdx = Math.floor(Math.random() * (words.length - 4));

    if (splitIdx < 3) {
        splitIdx = 3
    } else if (splitIdx > words.length - 3) {
        splitIdx = words.length - 3;
    }

    words = [...words.splice(0, splitIdx), image, ...words.splice(splitIdx, words.length - splitIdx - 1)];

    const text = words
        .map((word, idx) => word + (Math.random() > 0.9 && idx !== words.length - 1 ? ',' : ''))
        .join(' ') + '.';

    document.getElementById('root').innerHTML = text;
}

let counter = 0;

addEventListener('renderNewFormula', () => {
    if (counter < dataset.total) {
        render(counter);
        counter++;
    }
})
