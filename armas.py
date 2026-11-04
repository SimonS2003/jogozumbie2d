from abc import ABC, abstractmethod 

class Arma(ABC):
    def __init__(self, nome, dano, capacidade_pente,
        municao_reserva, tempo_recarga, peso, alcance, tipo_disparo, velocidade_tiro, preco=0):
        self.nome = nome
        self.dano = dano
        self.capacidade_pente = capacidade_pente
        self.municao_reserva = municao_reserva
        self.tempo_recarga = tempo_recarga
        self.peso = peso
        self.alcance = alcance
        self.tipo_disparo = tipo_disparo
        self.velocidade_tiro = velocidade_tiro
        self.recarregando = False
        self.tempo_restante = 0

    def atirar(self):
        if self.recarregando:
            print(f"{self.nome} está recarregando...")
            return False

        if self.municao_no_pente <= 0:
            print(f"{self.nome} está sem munição! Recarregue a arma.")
            return False

        self.municao_no_pente -= 1
        print(f"💥 Tiro disparado com {self.nome}! Balas no pente: {self.municao_no_pente}/{self.capacidade_pente}")
        return True

    def iniciar_recarga(self):
        if self.recarregando:
            return False
        if self.municao_no_pente == self.capacidade_pente:
            return False
        if self.municao_reserva <= 0:
            return False

        self.recarregando = True
        self.tempo_restante = self.tempo_recarga
        print(f"🔄 Recarregando {self.nome}...")
        return True

    @abstractmethod
    def atualizar(self, dt=0):
        if not self.recarregando:
            return

        self.tempo_restante = max(0, self.tempo_restante - dt)
        if self.tempo_restante == 0:
            faltam = self.capacidade_pente - self.municao_no_pente
            quantidade = min(faltam, self.municao_reserva)
            self.municao_no_pente += quantidade
            self.municao_reserva -= quantidade
            self.recarregando = False
            print(f"✅ {self.nome} recarregada!")
    
class Submetralhadora(Arma):
    def __init__(self, nome, dano, capacidade_pente, municao_reserva, velocidade_tiro):
        super().__init__(
            nome=nome,
            dano=dano,
            capacidade_pente=capacidade_pente,
            municao_reserva=municao_reserva,
            tempo_recarga=2.0,
            alcance=10,
            tipo_disparo="Automático",
            velocidade_tiro=velocidade_tiro,
            peso=1
        )
class FuzilDeAssalto(Arma):
    def __init__(self, nome, dano, capacidade_pente, municao_reserva, velocidade_tiro):
        super().__init__(
            nome=nome,
            dano=dano,
            capacidade_pente=capacidade_pente,
            municao_reserva=municao_reserva,
            tempo_recarga=2.5,
            alcance=20,                        
            tipo_disparo="Semi-Automático",
            velocidade_tiro=velocidade_tiro,
            peso=2
        )
class FuzilDePrecisao(Arma):
    def __init__(self, nome, dano, capacidade_pente, municao_reserva, velocidade_tiro):
        super().__init__(
            nome=nome,
            dano=dano,
            capacidade_pente=capacidade_pente,
            municao_reserva=municao_reserva,
            tempo_recarga=3.5,                  
            alcance=30,                        
            tipo_disparo="Disparo Único",           
            velocidade_tiro=velocidade_tiro,
            peso=3
        )
class MetralhadoraLeve(Arma):
    def __init__(self, nome, dano, capacidade_pente, municao_reserva, velocidade_tiro):
        super().__init__(
            nome=nome,
            dano=dano,
            capacidade_pente=capacidade_pente,
            municao_reserva=municao_reserva,
            tempo_recarga=5,                 
            alcance=20,                       
            tipo_disparo="Automático",           
            velocidade_tiro=velocidade_tiro,
            peso=5
        )
class Escopeta(Arma):
    def __init__(self, nome, dano, capacidade_pente, municao_reserva, velocidade_tiro):
        super().__init__(
            nome=nome,
            dano=dano,
            capacidade_pente=capacidade_pente,
            municao_reserva=municao_reserva,
            tempo_recarga=3,                  
            alcance=10,                        
            tipo_disparo="Semi-Automático",           
            velocidade_tiro=velocidade_tiro,
            peso=2
        )

class Pistola(Arma):
    def __init__(self, nome, dano, capacidade_pente, municao_reserva, velocidade_tiro):
        super().__init__(
            nome=nome, 
            dano=dano,
            capacidade_pente=capacidade_pente,
            municao_reserva=municao_reserva,
            tempo_recarga=1.5,                  
            alcance=5,                        
            tipo_disparo="Semi-automático",
            velocidade_tiro=velocidade_tiro,
            peso=1
        )   
        
"""
class MP5(Submetralhadora):
    def __init__(self):
        super().__init__(nome="MP5", dano=10, capacidade_pente=30, municao_reserva=90, velocidade_tiro=2)

class M8A1(FuzilDeAssalto):
    def __init__(self):
        super().__init__(nome="M8A1", 
                         dano=35, 
                         capacidade_pente=45, 
                         municao_reserva=120, 
                         velocidade_tiro=2)

class Balista(FuzilDePrecisao):
    def __init__(self):
        super().__init__(nome="Balista", 
                         dano=150, 
                         capacidade_pente=12, 
                         municao_reserva=30, 
                         velocidade_tiro=1)

class LSAT(MetralhadoraLeve):
    def __init__(self):
        super().__init__(nome="LSAT", dano=30, 
                         capacidade_pente=60, 
                         municao_reserva=240, 
                         velocidade_tiro=2)

class RM870(Escopeta):
    def __init__(self):
        super().__init__(nome="RM870", 
                         dano=70, 
                         capacidade_pente=8, 
                         municao_reserva=32, 
                         velocidade_tiro=2)

class FiveSeven(Pistola):
    def __init__(self):
        super().__init__(nome="Five-Seven", 
                         dano=20, 
                         capacidade_pente=15, 
                         municao_reserva=60, 
                         velocidade_tiro=1)    
"""
