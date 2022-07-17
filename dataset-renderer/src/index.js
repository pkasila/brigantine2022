import generateText from "./generateText";

let words = generateText(50);

words[25] = `<img id="formula" class="formula" src="/imgs/1a0a0dfbac.png" alt="Formula">`;

if (Math.random() > 0.5) {
    words[0] = `<strong>${words[0].charAt(0).toUpperCase() + words[0].slice(1)}</strong>`;
} else {
    words[0] = words[0].charAt(0).toUpperCase() + words[0].slice(1);
}

let text = words
    .map((word, idx) => word + (Math.random() > 0.5 && idx !== words.length - 1 ? ',' : ''))
    .join(' ') + '.';

const root = document.getElementById('root');

root.innerHTML = text;

const formula = document.getElementById('formula');
