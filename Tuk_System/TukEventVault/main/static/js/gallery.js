const viewButtons = document.querySelectorAll('.view-button');
const shareButtons = document.querySelectorAll('.share-button');

viewButtons.forEach(button => {
    button.addEventListener('click', () => {
        const galleryItem = button.closest('.gallery-item');
        const image = galleryItem.querySelector('img');
        const video = galleryItem.querySelector('video');

        if (image) {
            window.open(image.src, '_blank');
        } else if (video) {
            window.open(video.src, '_blank');
        }
    });
});

// Using the Web Share API for cross-platform sharing
shareButtons.forEach(button => {
    button.addEventListener('click', () => {
        const shareUrl = button.dataset.url;
        const title = document.title; // Or provide a custom title

        if (navigator.share) {
            navigator.share({
                title: title,
                url: shareUrl
            })
            .then(() => console.log('Successful share'))
            .catch((error) => console.error('Error sharing:', error));
        } else {
            // Fallback for browsers that don't support Web Share API
            // You can use platform-specific sharing methods or libraries here
            console.log('Web Share API not supported');
        }
    });
});