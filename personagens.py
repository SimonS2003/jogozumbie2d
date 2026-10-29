from abc import ABC, abstractmethod
import math
import random


class Boneco(ABC):
    nome = str
    def __init__(self, nome : str, x : float, y : float, vida : int = 100, armadura : int = 0, dano : int = 5, velocidade : float = 2.0):
        self.nome = nome
        self.x = x
        self.y = y
        self.vida = vida
        self.armadura = armadura
        self.dano = dano
        self.velocidade = velocidade
        

    def receber_dano(self, quantidade : int):
        if not self.estar_vivo() or quantidade <=0:
            return

        dano_efetivo = max(1, quantidade - self.armadura)
        self.vida = max(0,self.vida - dano_efetivo)
        print(f"{self.__class__.__name__} recebeu {dano_efetivo} de dano! Vida restante: {self.vida}")

        if not self.estar_vivo():
            print(f"{self.nome} Morreu")

    def atacar(self, alvo):
        if self.estar_vivo():     
            alvo.receber_dano(self.dano)
        else:
            print(f"{self.__class__.__name__} não pode atacar porque está morto.")

    def estar_vivo(self):
        return self.vida > 0

    def movimentacao(self, direcao_x:float, direcao_y:float, dt:float):
        if not self.estar_vivo():
            return
        comprimento = (direcao_x ** 2 +direcao_y ** 2) ** 0.5
        if comprimento == 0:
            return
        self.x +=(direcao_x / comprimento) * self.velocidade * dt
        self.y +=(direcao_y / comprimento) * self.velocidade * dt


    @abstractmethod
    def atualizar(self, dt):
        pass

class Jogador(Boneco):

    def __init__(self, nome : str, x : float, y : float, dano : int = 10,):
        super().__init__(nome=nome, x=x, y=y, dano=dano)
        self.dinheiro = 5


    def equipar_arma(self, arma):
        self.arma_equipada = arma
        print(f"{self.nome} equipou a arma: {arma.nome}")

    def atirar_em(self, alvo):
        if not self.arma_equipada:
            print(f"{self.nome} não tem nenhuma arma em mãos!")
            return

        if not alvo.estar_vivo():
            print(f"{alvo.nome} já está morto!")
            return

        alvo.receber_dano(self.arma_equipada.dano)

    def atualizar(self, dt=0):
        if self.arma_equipada:
            self.arma_equipada.atualizar(dt)

class Npc(Boneco):
    def __init__(self, nome : str, x : float, y : float, vida : int, armadura : int, dano : int, velocidade : float):
        super().__init__(nome=nome, x=x, y=y, vida=vida, armadura=armadura, dano=dano, velocidade=velocidade)


class Inimigo(Boneco):
    def __init__(self, nome : str, x : float, y : float, vida : int, armadura : int, dano : int, velocidade : float, raio_visao : float = 200.0):
        super().__init__(nome=nome, x=x, y=y, vida=vida, armadura=armadura, dano=dano, velocidade=velocidade)
        self.direcao_x = 0
        self.direcao_y = 0
        self.tempo_para_mudar = 0
        self.raio_visao = raio_visao
        self.sortear_direcao()

    def sortear_direcao(self):
        angulo = random.uniform( 0, 2 * math.pi)
        self.direcao_x = math.cos(angulo)
        self.direcao_y = math.sin(angulo)
        self.tempo_para_mudar = random.uniform(1.0,3.0)

    def perseguir_alvo(self, alvo):
        dx = alvo.x - self.x
        dy = alvo.y - self.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia <= self.raio_visao and distancia > 0:
            self.direcao_x = dx / distancia
            self.direcao_y = dy / distancia
            return True
        return False
    
    def receber_dano(self, quantidade):
        # A armadura absorve um pouco de dano (mínimo de 1)
        dano_real = max(1, quantidade - self.armadura)
        self.vida = max(0, self.vida - dano_real)
        
        print(f"{self.nome} tomou {dano_real} de dano! Vida restante: {self.vida}")

        if not self.estar_vivo():
            print(f" {self.nome} foi derrotado!")

    
    def atualizar(self,dt):
        if not self.estar_vivo():
            return

        perseguindo = self.perseguir_alvo(Jogador) if Jogador else False

        if not perseguindo:
            self.tempo_para_mudar -= dt
            if self.tempo_para_mudar <= 0:
                self.sortear_direcao()
                
            self.movimentacao(self.direcao_x, self.direcao_y, dt)   


    


