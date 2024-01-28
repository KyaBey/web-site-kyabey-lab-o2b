// script.js

document.addEventListener('DOMContentLoaded', function () {
    adjustVideoPositions();
});

function adjustVideoPositions() {
    var playlistContainers = document.querySelectorAll('.playlist-container');

    playlistContainers.forEach(function (container) {
        var videos = container.querySelectorAll('.video-info');
        var videosPerRow = 6; // Defina o número desejado de vídeos por linha

        for (var i = 0; i < videos.length; i += videosPerRow) {
            var row = Array.from(videos).slice(i, i + videosPerRow);

            var totalWidth = 0;
            row.forEach(function (video) {
                totalWidth += video.offsetWidth;
            });

            var marginTotal = (row.length - 1) * 20; // 20px de margem entre os vídeos
            var spaceAvailable = container.offsetWidth - marginTotal;
            var spacePerVideo = spaceAvailable / row.length;

            row.forEach(function (video) {
                video.style.marginRight = '20px'; // Manter a margem à direita
                video.style.width = spacePerVideo + 'px';
            });
        }
    });
}
