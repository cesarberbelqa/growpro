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
        if (!scheduleForm) return;

        const frequenciaSelect = document.getElementById('id_frequencia');
        const intervaloInputDiv = document.getElementById('id_dias_intervalo').parentElement;

        function toggleIntervaloInput() {
            if (frequenciaSelect.value === 'INTERVALO') {
                intervaloInputDiv.style.display = 'block';
            } else {
                intervaloInputDiv.style.display = 'none';
            }
        }
        toggleIntervaloInput();
        frequenciaSelect.addEventListener('change', toggleIntervaloInput);
    }

    /**
     * Função para validar a capacidade do ambiente em tempo real no formulário da planta.
     */
    function handleEnvironmentCapacityCheck() {
        const environmentSelect = document.getElementById('id_ambiente_atual');
        // Só executa se o elemento existir na página atual.
        if (!environmentSelect) return;

        // Cria um elemento para mostrar a mensagem de aviso uma única vez.
        let warningDiv = document.querySelector('#env-capacity-warning');
        if (!warningDiv) {
            warningDiv = document.createElement('div');
            warningDiv.id = 'env-capacity-warning';
            warningDiv.className = 'alert alert-warning p-2 mt-2 d-none'; // Inicia escondido
            environmentSelect.parentElement.appendChild(warningDiv);
        }

        const checkCapacity = () => {
            const environmentId = environmentSelect.value;
            
            // Esconde o aviso se nenhum ambiente for selecionado
            if (!environmentId) {
                warningDiv.classList.add('d-none');
                return;
            }
            
            // A URL da nossa API
            const url = `/environments/api/capacity/${environmentId}/`;

            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Obtém o ID da planta que está sendo editada, se houver.
                    const plantId = document.body.dataset.plantId || null;

                    // A validação de 'is_full' deve considerar o caso de edição.
                    // Se a planta já estiver no ambiente, o ambiente não está "cheio" para ela.
                    // Esta lógica é complexa no frontend, então confiamos na mensagem do backend.
                    // O frontend apenas avisa sobre a capacidade.
                    const currentCapacity = data.current_plant_count;
                    const maxCapacity = data.numero_maximo_plantas;

                    if (currentCapacity >= maxCapacity) {
                        warningDiv.textContent = `Atenção: Este ambiente está na capacidade máxima (${currentCapacity}/${maxCapacity}).`;
                        warningDiv.classList.remove('d-none');
                    } else {
                        // Opcional: mostrar a capacidade mesmo quando não está cheio.
                        // warningDiv.textContent = `Capacidade: ${currentCapacity}/${maxCapacity}`;
                        // warningDiv.classList.remove('d-none');
                        // warningDiv.classList.replace('alert-warning', 'alert-info');
                        
                        // Ou simplesmente esconder o aviso
                        warningDiv.classList.add('d-none');
                    }
                })
                .catch(error => {
                    console.error('Erro ao buscar capacidade:', error);
                    warningDiv.classList.add('d-none');
                });
        };

        // Adiciona o "ouvinte" de evento
        environmentSelect.addEventListener('change', checkCapacity);
        
        // Opcional: verifica a capacidade ao carregar a página se um ambiente já estiver selecionado
        if (environmentSelect.value) {
            checkCapacity();
        }
    }


    /**
     * Inicializa os Tooltips do Bootstrap em todo o site.
     */
    function initializeTooltips() {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }


    // --- Chamada de Todas as Funções de Inicialização ---
    handleWateringScheduleForm();
    handleEnvironmentCapacityCheck(); // <-- Adicionamos a nova função aqui
    initializeTooltips();
});