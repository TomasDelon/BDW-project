/**
 * JavaScript ultra-mínimo: Solo sincroniza morpion_id cuando cambia la selección
 * El campo oculto ya tiene un valor por defecto, solo necesita actualizarse si el usuario cambia la selección
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
