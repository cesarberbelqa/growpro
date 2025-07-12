/*
 * Arquivo: static/js/main.js
 * Descrição: Scripts JavaScript globais para o projeto GrowPro.
 */

// Garante que o DOM esteja totalmente carregado antes de executar os scripts.
document.addEventListener('DOMContentLoaded', function() {

    console.log('GrowPro JS Carregado!');

    /**
     * Função para gerenciar a visibilidade do campo de intervalo no formulário de agendamento de rega.
     */
    function handleWateringScheduleForm() {
        const scheduleForm = document.getElementById('scheduleForm');
        if (!scheduleForm) {
            return; // Sai se não estiver na página do formulário
        }

        const frequenciaSelect = document.getElementById('id_frequencia');
        const intervaloInputDiv = document.getElementById('id_dias_intervalo').parentElement;

        function toggleIntervaloInput() {
            if (frequenciaSelect.value === 'INTERVALO') {
                intervaloInputDiv.style.display = 'block';
            } else {
                intervaloInputDiv.style.display = 'none';
            }
        }

        // Executa a função na carga da página e quando o select mudar
        toggleIntervaloInput();
        frequenciaSelect.addEventListener('change', toggleIntervaloInput);
    }

    /**
     * Inicializa os Tooltips do Bootstrap em todo o site.
     * Para usar, adicione os atributos `data-bs-toggle="tooltip"` e `title="Seu texto"` a um elemento HTML.
     * Ex: <button data-bs-toggle="tooltip" title="Clique para salvar">Salvar</button>
     */
    function initializeTooltips() {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }


    // --- Chamada das Funções ---
    handleWateringScheduleForm();
    initializeTooltips();

});