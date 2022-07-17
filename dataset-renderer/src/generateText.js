import words from 'russian-words';

export default function generateText(len) {
    const length = (words ?? []).length;

    return Array.from({length: len})
        .map(_ => words[Math.floor(Math.random() * length)]);
}
