# bibliotecas
import random
import threading
import time

import pandas as pd
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# problemas específicos para cada componente
PROBLEMAS_COMPONENTES = {
    "Placa mãe": [
        ("Circuito queimado", 300, "Substituição do circuito danificado"),
        ("Conexão com a RAM falhou", 150, "Reparo nos slots de RAM"),
        ("BIOS corrompida", 200, "Reinstalação ou atualização do BIOS")
    ],
    "Processador": [
        ("Superaquecimento", 250, "Substituição do cooler ou aplicação de pasta térmica"),
        ("Pinos danificados", 400, "Troca do processador"),
        ("Falha na execução de instruções", 350, "Reconfiguração do processador")
    ],
    "Memória RAM": [
        ("Falha em um módulo", 100, "Troca do módulo de memória"),
        ("Erro de paridade", 120, "Reparo na memória"),
        ("Conexão instável com a placa-mãe", 150, "Ajuste nos conectores")
    ],
    "Armazenamento": [
        ("Setores defeituosos", 200, "Reparação de setores ou clonagem de disco"),
        ("Controlador de disco com defeito", 250, "Troca do controlador"),
        ("Desgaste do SSD", 300, "Substituição do SSD")
    ],
    "Fonte de alimentação": [
        ("Falta de energia", 150, "Substituição de capacitores"),
        ("Sobrecarga", 180, "Reparo no circuito interno"),
        ("Capacitor queimado", 200, "Troca do capacitor")
    ]
}

# classe que representa um componente individual
class Componente:
    def __init__(self, nome, vida_maxima, id_componente):
        self.id = id_componente  # atribui uma identificação única ao componente
        self.nome = nome  # define o nome do componente
        self.tempo_vida = vida_maxima  # define o tempo de vida máximo do componente
        self.estado = "funcionando"  # estado inicial do componente
        self.problema = None  # armazena o problema específico quando o componente quebra
        self.aviso_manutencao = False  # indica a necessidade de manutenção preventiva
        self.custo_preventiva = random.randint(50, 100)  # custo para manutenção preventiva
        self.ciclos_ganhos_preventiva = random.randint(15, 25)  # ciclos ganhos após manutenção preventiva

    def degradar(self):
        # reduz o tempo de vida do componente e verifica se ele quebrou
        if self.estado == "funcionando":
            self.tempo_vida -= 1
            if self.tempo_vida <= 0:
                self.estado = "quebrado"
                self.problema = random.choice(PROBLEMAS_COMPONENTES[self.nome])
                self.aviso_manutencao = False
            else:
                # verifica necessidade de manutenção preventiva
                Manutencao.verificar_preventiva(self)

    def reparar(self, ambiente, computador_id):
        # realiza o reparo do componente e restaura seu estado
        problema, custo, conserto = Manutencao.obter_detalhes_problema(self.nome)
        self.tempo_vida = random.randint(5, 15)
        self.estado = "funcionando"
        self.problema = None  # remove o problema após o reparo

        # registra o problema no histórico
        Manutencao.registrar_problema(
            ambiente, computador_id, self.nome, problema, custo, conserto
        )


class Computador:
    def __init__(self, id):
        self.id = id  # define o identificador único do computador
        self.componentes = [
            Componente("Placa mãe", random.randint(5, 10), 1),
            Componente("Processador", random.randint(5, 10), 2),
            Componente("Memória RAM", random.randint(5, 10), 3),
            Componente("Armazenamento", random.randint(5, 10), 4),
            Componente("Fonte de alimentação", random.randint(5, 10), 5)
        ]
        self.funcionando = True  # indica se o computador está funcionando

    def verificar_componentes(self):
        # verifica todos os componentes e atualiza o estado do computador
        for componente in self.componentes:
            componente.degradar()
            if componente.estado == "quebrado":
                self.funcionando = False
                return  # interrompe a verificação ao encontrar um componente quebrado

    def consertar(self):
        # conserta componentes quebrados e reativa o computador
        for componente in self.componentes:
            if componente.estado == "quebrado":
                componente.reparar(ambiente, self.id)
        self.funcionando = True

    def verificar_manutencao_preventiva(self):
        # verifica quais componentes precisam de manutenção preventiva
        for componente in self.componentes:
            if componente.tempo_vida > 0:
                Manutencao.verificar_preventiva(componente)
            else:
                # remove o aviso de manutenção quando o tempo de vida chega a zero
                componente.aviso_manutencao = False


class Manutencao:
    @staticmethod
    def realizar_manutencao(computador):
        # realiza a manutenção corretiva de um computador
        computador.consertar()

    @staticmethod
    def calcular_custo(conserto):
        # calcula o custo do conserto de um componente
        _, custo, descricao = conserto
        return custo, descricao

    @staticmethod
    def obter_detalhes_problema(nome_componente):
        # obtém os detalhes do problema de um componente
        problemas = PROBLEMAS_COMPONENTES[nome_componente]
        problema, custo, conserto = random.choice(problemas)
        return problema, custo, conserto

    @staticmethod
    def verificar_preventiva(componente):
        # ativa o aviso de manutenção preventiva se necessário
        if componente.tempo_vida <= 3 and componente.estado == "funcionando":
            componente.aviso_manutencao = True

    @staticmethod
    def registrar_problema(ambiente, computador_id, componente, problema, custo, conserto):
        # registra um problema no histórico global
        ambiente.registrar_problema(
            computador_id, componente, problema, custo, conserto
        )


class Ambiente:
    def __init__(self):
        self.computadores = []  # lista de computadores no ambiente
        self.historico_problemas = []  # histórico global de problemas

    def adicionar_computador(self, computador):
        # adiciona um novo computador ao ambiente
        self.computadores.append(computador)

    def verificar_status(self):
        # verifica o estado dos computadores e seus componentes
        for computador in self.computadores:
            if computador.funcionando:
                for componente in computador.componentes:
                    Manutencao.verificar_preventiva(componente)
                    estado_anterior = componente.estado
                    componente.degradar()
                    if estado_anterior == "funcionando" and componente.estado == "quebrado":
                        problema, custo, conserto = Manutencao.obter_detalhes_problema(
                            componente.nome)
                        self.registrar_problema(
                            computador.id, componente.nome, problema, custo, conserto
                        )
                        computador.funcionando = False
                        break

    def registrar_problema(self, computador_id, componente, problema, custo, conserto):
        # registra um problema no histórico
        self.historico_problemas.append({
            "computador_id": computador_id,
            "componente": componente,
            "problema": problema,
            "custo": custo,
            "conserto": conserto
        })

    def mostrar_historico_problemas(self):
        # retorna o histórico de problemas
        return self.historico_problemas

    def mostrar_status(self):
        # retorna o status atual dos computadores e componentes
        status = []
        for computador in self.computadores:
            comp_status = {
                "id": computador.id,
                "componentes": [
                    {
                        "nome": componente.nome,
                        "vida": componente.tempo_vida,
                        "estado": componente.estado,
                        "aviso_manutencao": componente.aviso_manutencao
                    } for componente in computador.componentes
                ],
                "funcionando": computador.funcionando
            }
            status.append(comp_status)
        return status


# configuração do ambiente
ambiente = Ambiente()
for i in range(3):
    ambiente.adicionar_computador(Computador(i))


@app.route("/atualizar_tempo_vida", methods=["GET"])
def atualizar_tempo_vida():
    # atualiza o tempo de vida dos componentes e retorna o status atualizado
    ambiente.verificar_status()
    return jsonify(status=ambiente.mostrar_status())


@app.route("/atualizar_status", methods=["GET"])
def atualizar_status():
    # atualiza o status dos computadores
    ambiente.verificar_status()
    return jsonify(status=ambiente.mostrar_status())


@app.route("/analise")
def analise():
    # exibe análises dos problemas no ambiente
    df = pd.DataFrame(ambiente.mostrar_historico_problemas())
    return render_template("analise.html", analise=df.to_html())


@app.route("/")
def home():
    # página inicial que exibe o status e histórico
    return render_template("index.html", status=ambiente.mostrar_status(), problemas=ambiente.mostrar_historico_problemas())


def simular_ciclos():
    ciclo = 0
    while True:
        ciclo += 1
        print(f"Ciclo {ciclo}")
        ambiente.verificar_status()

        # Log de avisos de manutenção preventiva
        for computador in ambiente.computadores:
            for componente in computador.componentes:
                if componente.aviso_manutencao:
                    print(f"[AVISO] {componente.nome} no Computador {
                          computador.id} precisa de manutenção preventiva!")

        time.sleep(10)


# inicia a simulação em uma thread separada
threading.Thread(target=simular_ciclos, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)
