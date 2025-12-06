/**
 * JavaScript pour la création de morpions personnalisés
 * Gère la validation des stats, la webcam et l'upload d'images
 */
(function() {
    'use strict';

    // === VALIDATION DES STATS EN TEMPS RÉEL ===

    const statInputs = ['hp', 'attack', 'mana', 'accuracy'];
    const totalValueSpan = document.getElementById('total-value');
    const totalStatus = document.getElementById('total-status');
    const submitBtn = document.getElementById('submit-btn');

    function updateStatsTotal() {
        let total = 0;
        statInputs.forEach(function(id) {
            const input = document.getElementById(id);
            const value = parseInt(input.value) || 0;
            total += value;
        });

        totalValueSpan.textContent = total;

        // Afficher le statut
        if (total === 15) {
            totalStatus.textContent = '✅ Parfait !';
            totalStatus.className = 'status-valid';
            return true;
        } else if (total < 15) {
            totalStatus.textContent = '⚠️ Il reste ' + (15 - total) + ' points';
            totalStatus.className = 'status-warning';
            return false;
        } else {
            totalStatus.textContent = '❌ ' + (total - 15) + ' points en trop';
            totalStatus.className = 'status-error';
            return false;
        }
    }

    // Écouter les changements sur tous les inputs de stats
    statInputs.forEach(function(id) {
        const input = document.getElementById(id);
        input.addEventListener('input', function() {
            updateStatsTotal();
            validateForm();
        });
    });

    // Initialiser le total
    updateStatsTotal();

    // === GESTION WEBCAM ===

    let stream = null;
    const webcamVideo = document.getElementById('webcam-video');
    const webcamCanvas = document.getElementById('webcam-canvas');
    const webcamContainer = document.getElementById('webcam-container');
    const startWebcamBtn = document.getElementById('start-webcam-btn');
    const captureBtn = document.getElementById('capture-btn');
    const stopWebcamBtn = document.getElementById('stop-webcam-btn');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const clearImageBtn = document.getElementById('clear-image-btn');
    const imageDataInput = document.getElementById('image_data');

    const uploadInput = document.getElementById('upload-input');

    function setPreview(imageData) {
        imagePreview.src = imageData;
        previewContainer.style.display = 'block';
        imageDataInput.value = imageData;
        validateForm();
    }

    // Démarrer la webcam
    startWebcamBtn.addEventListener('click', async function() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 }
            });
            webcamVideo.srcObject = stream;
            webcamContainer.style.display = 'block';
            captureBtn.style.display = 'inline-block';
            stopWebcamBtn.style.display = 'inline-block';
            startWebcamBtn.style.display = 'none';
        } catch (err) {
            alert('Impossible d\'accéder à la webcam: ' + err.message);
        }
    });

    // Capturer l'image
    captureBtn.addEventListener('click', function() {
        const context = webcamCanvas.getContext('2d');
        const OUTPUT_SIZE = 400;
        webcamCanvas.width = OUTPUT_SIZE;
        webcamCanvas.height = OUTPUT_SIZE;

        const videoWidth = webcamVideo.videoWidth || OUTPUT_SIZE;
        const videoHeight = webcamVideo.videoHeight || OUTPUT_SIZE;
        const squareSize = Math.min(videoWidth, videoHeight);
        const sx = (videoWidth - squareSize) / 2;
        const sy = (videoHeight - squareSize) / 2;

        // Dessiner la vidéo recadrée pour éviter l'écrasement
        context.drawImage(
            webcamVideo,
            sx,
            sy,
            squareSize,
            squareSize,
            0,
            0,
            OUTPUT_SIZE,
            OUTPUT_SIZE
        );

        const imageData = webcamCanvas.toDataURL('image/png');
        setPreview(imageData);
        stopWebcam();
    });

    // Arrêter la webcam
    function stopWebcam() {
        if (stream) {
            stream.getTracks().forEach(function(track) {
                track.stop();
            });
            stream = null;
        }
        webcamContainer.style.display = 'none';
        captureBtn.style.display = 'none';
        stopWebcamBtn.style.display = 'none';
        startWebcamBtn.style.display = 'inline-block';
    }

    stopWebcamBtn.addEventListener('click', stopWebcam);

    // Supprimer l'image
    clearImageBtn.addEventListener('click', function() {
        imagePreview.src = '';
        previewContainer.style.display = 'none';
        imageDataInput.value = '';
        uploadInput.value = '';
        validateForm();
    });

    // Upload d'image depuis le disque
    uploadInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (!file) {
            return;
        }

        if (!file.type.startsWith('image/')) {
            alert('Merci de sélectionner un fichier image (PNG ou JPG).');
            uploadInput.value = '';
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            setPreview(e.target.result);
            stopWebcam();
        };
        reader.readAsDataURL(file);
    });

    // === VALIDATION GLOBALE DU FORMULAIRE ===

    function validateForm() {
        const nameValid = document.getElementById('morpion_name').value.trim().length > 0;
        const statsValid = updateStatsTotal();
        const imageValid = imageDataInput.value.length > 0;

        if (nameValid && statsValid && imageValid) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    // Écouter le nom
    document.getElementById('morpion_name').addEventListener('input', validateForm);

    // Validation initiale
    validateForm();

    // === NETTOYAGE À LA FERMETURE ===

    window.addEventListener('beforeunload', function() {
        stopWebcam();
    });

})();
