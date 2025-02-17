document.addEventListener('DOMContentLoaded', () => { 
    const colorPicker = document.getElementById('color-picker');
    const clearBtn = document.getElementById('clear-btn');
    const eraserBtn = document.getElementById('eraser-btn');
    const opacitySlider = document.getElementById('opacity-slider');
    const sizeButtons = document.querySelectorAll('.size-btn');
    let isEraserMode = false;

    colorPicker.addEventListener('input', async (event) => {
        const color = event.target.value;
        document.getElementById('selected-color').style.backgroundColor = color;
        await fetch('/change_color', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ color })
        });
        isEraserMode = false;  
        eraserBtn.classList.remove('active');
    });

    clearBtn.addEventListener('click', async () => {
        try {
            document.getElementById('video-feed').src = ""; 
            const response = await fetch('/clear_canvas', {
                method: 'POST'
            });
            if (response.ok) {
                console.log('Canvas cleared successfully');
                document.getElementById('video-feed').src = "/video_feed"; 
            } else {
                console.error('Failed to clear canvas on server');
            }
        } catch (error) {
            console.error('Error clearing canvas:', error);
        }
    });

    eraserBtn.addEventListener('click', async () => {
        isEraserMode = !isEraserMode;
        eraserBtn.classList.toggle('active', isEraserMode);
        await fetch('/toggle_eraser', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ eraser: isEraserMode })
        });
    });

    opacitySlider.addEventListener('input', async (event) => {
        const opacity = parseFloat(event.target.value);
        await fetch('/change_opacity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ opacity })
        });
    });

    sizeButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            const size = parseInt(event.target.getAttribute('data-size'));
            await fetch('/change_size', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ size })
            });
            sizeButtons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        });
    });
});
