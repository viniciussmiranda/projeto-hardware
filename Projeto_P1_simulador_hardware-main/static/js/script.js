
        // Função para atualizar o tempo de vida dos computadores
        function atualizarTempoVida() {
            fetch('/atualizar_tempo_vida')
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Erro ao atualizar o tempo de vida.');
                    }
                })
                .then(data => {
                    const computadoresContainer = document.querySelector('.computadores-container');
                    computadoresContainer.innerHTML = ''; // Limpa o conteúdo atual

                    // Atualiza a interface com os dados recebidos
                    data.status.forEach(computador => {
                        const computadorDiv = document.createElement('div');
                        computadorDiv.classList.add('computador');
                        computadorDiv.setAttribute('data-id', computador.id);
                        computadorDiv.innerHTML = `
                            <img src="/static/image/computer-svgrepo-com.png" alt="Computador" height="100px" width="100px">
                            <h2>Computador ${computador.id}</h2>
                            ${computador.componentes.map(componente => `
                                <div class="componente">
                                    <p>Componente: ${componente.nome}</p>
                                    <p>Estado: <span class="${componente.estado === 'funcionando' ? 'funcionando' : 'quebrado'}">${componente.estado}</span></p>
                                    <p>Tempo de vida: ${componente.vida}</p>
                                    ${componente.aviso_manutencao && componente.vida <= 3 ? `
                                        <p class="aviso">⚠️ Manutenção preventiva recomendada!</p>
                                        <button onclick="realizarManutencaoPreventiva(${computador.id}, ${componente.id})">Realizar manutenção preventiva</button>
                                    ` : ''}
                                </div>
                            `).join('')}
                            <button onclick="consertarComputador(${computador.id})">🔧 Consertar Computador</button>
                        `;
                        computadoresContainer.appendChild(computadorDiv);
                    });
                })
                .catch(error => {
                    console.error('Erro:', error);
                });
        }

        // Atualiza o tempo de vida a cada 5 segundos
        setInterval(atualizarTempoVida, 2000); // 5000 ms = 5 segundos

        function consertarComputador(id) {
            fetch(`/consertar/${id}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert("Erro ao consertar o computador.");
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert("Erro ao consertar o computador.");
                });
        }

        function realizarManutencaoPreventiva(computadorId, componenteId) {
            fetch(`/manutencao_preventiva/${computadorId}/${componenteId}`, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();  // Recarrega a página para mostrar o novo status
                    } else {
                        alert("Erro ao realizar manutenção preventiva: " + response.statusText);
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert("Erro ao realizar manutenção preventiva.");
                });
        }

        function adicionarComputador() {
            fetch('/adicionar', {  // Corrigido para '/adicionar'
                method: 'POST'
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload();  // Recarrega a página para mostrar o novo computador
                } else {
                    alert("Erro ao adicionar computador: " + response.statusText);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert("Erro ao adicionar computador.");
            });
        }
