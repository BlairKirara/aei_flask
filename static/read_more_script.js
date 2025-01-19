document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.toggle-button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const textBlock = button.parentElement;
            const shortText = textBlock.querySelector('.short-text');
            const fullText = textBlock.querySelector('.full-text');

            if (fullText && shortText) {
                if (shortText.style.display === 'none') {
                    shortText.style.display = 'block';
                    fullText.style.display = 'none';
                    button.textContent = 'Czytaj więcej';
                } else {
                    shortText.style.display = 'none';
                    fullText.style.display = 'block';
                    button.textContent = 'Czytaj mniej';
                }
            }
        });
    });
});
