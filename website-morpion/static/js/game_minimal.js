/**
 * JavaScript ultra-minimal : synchronise uniquement morpion_id lorsque la sélection change
 * Le champ caché a déjà une valeur par défaut, il n'a besoin d'être mis à jour que si l'utilisateur change la sélection
 */
(function() {
    'use strict';

    function initMorpionSelectorSync(root) {
        const scope = root instanceof Element ? root : document;
        const morpionIdHidden = scope.querySelector('#hidden-morpion-id');
        if (!morpionIdHidden) {
            return;
        }
        const morpionInputs = scope.querySelectorAll('.morpion-selector__input');
        morpionInputs.forEach(function(input) {
            if (input.dataset.selectorBound === 'true') {
                return;
            }
            input.dataset.selectorBound = 'true';
            input.addEventListener('change', function() {
                morpionIdHidden.value = this.value;
            });
        });
    }

    window.initMorpionSelectorSync = initMorpionSelectorSync;

    document.addEventListener('DOMContentLoaded', function() {
        initMorpionSelectorSync(document);
    });
})();
