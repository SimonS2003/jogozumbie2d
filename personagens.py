from abc import ABC, abstractmethod
import math
import random
import pygame

class Boneco(ABC):
    nome = str
    def __init__(self, nome : str, x : float, y : float, vida : int = 100, armadura : int = 0, dano : int = 5, velocidade : float = 2.0, cor_base=(0, 128, 255)):
        self.nome = nome
        self.x = x
        self.y = y
        self.vida = vida
        self.armadura = armadura
        self.dano = dano
        self.velocidade = velocidade
        
        self.largura = 32
        self.altura = 32
        self.cor_base = cor_base
        self.imagem_original = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)

        self.gerar_sprite_pixelarray()

        self.imagem_atual = self.imagem_original.copy()
        self.tempo_efeito_dano = 0.0

    def gerar_sprite_pixelarray(self):
        self.imagem_original.fill((0, 0, 0, 0))
        with pygame.PixelArray(self.imagem_original) as pixels:
            #Corpo
            pixels[4:28, 4:28] = self.cor_base

            #Bordas
            pixels[4:28, 4] = (0, 0, 0)  
            pixels[4:28, 27] = (0, 0, 0)
            pixels[4, 4:28] = (0, 0, 0)
            pixels[27, 4:28] = (0, 0, 0)

            #Olhos
            pixels[10:14, 10:14] = (255, 255, 255)
            pixels[18:22, 10:14] = (255, 255, 255)

    def trocar_cor(self, cor_base, nova_cor):
        with pygame.PixelArray(self.imagem_original) as pixels:
            pixels.replace(cor_base, nova_cor)
        self.imagem_atual = self.imagem_original.copy()
        self.cor_base = nova_cor

    def efeito_piscar_dano(self):
        self.imagem_atual = self.imagem_original.copy()
        with pygame.PixelArray(self.imagem_atual) as pixels:
            pixels.replace(self.cor_base, (255, 100, 100))
        self.tempo_efeito_dano = 0.15

    def receber_dano(self, quantidade : int):
        if not self.estar_vivo() or quantidade <=0:
            return

        dano_efetivo = max(1, quantidade - self.armadura)
        self.vida = max(0,self.vida - dano_efetivo)
        self.efeito_piscar_dano()

        print(f"{self.__class__.__name__} recebeu {dano_efetivo} de dano! Vida restante: {self.vida}")

        if not self.estar_vivo():
            print(f"{self.nome} Morreu")

    def atualizar_efeito_dano(self, dt: float):
        if self.tempo_efeito_dano > 0:
            self.tempo_efeito_dano -= dt
            if self.tempo_efeito_dano <= 0:
                self.imagem_atual = self.imagem_original.copy()

    def desenhar(self, tela):
        if self.estar_vivo():
            tela.blit(self.imagem_atual, (int(self.x), int(self.y)))

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
        comprimento = (direcao_x ** 2 + direcao_y ** 2) ** 0.5
        if comprimento == 0:
            return
        self.x +=(direcao_x / comprimento) * self.velocidade * dt
        self.y +=(direcao_y / comprimento) * self.velocidade * dt


    @abstractmethod
    def atualizar(self, dt):
        pass

class Jogador(Boneco):

    def __init__(self, nome : str, x : float, y : float, dano : int = 10,):
        super().__init__(nome=nome, x=x, y=y, dano=dano, velocidade=220.0, cor_base=(0, 128, 255))
        self.dinheiro = 5
        self.arma_equipada = None

    def equipar_arma(self, arma):
        self.arma_equipada = arma
        print(f"{self.nome} equipou a arma: {arma.nome}")

    def atirar_em(self, alvo):
        if not self.arma_equipada:
            alvo.receber_dano(self.dano)
            return

        if not alvo.estar_vivo():
            print(f"{alvo.nome} já está morto!")
            return

        alvo.receber_dano(self.arma_equipada.dano)

    def atualizar(self, dt=0):
        self.atualizar_efeito_dano(dt)
        if self.arma_equipada:
            self.arma_equipada.atualizar(dt)

class Npc(Boneco):
    def __init__(self, nome: str, x: float, y: float, vida: int = 100, armadura: int = 0, dano: int = 0, velocidade: float = 100.0):
        super().__init__(nome=nome, x=x, y=y, vida=vida, armadura=armadura, dano=dano, velocidade=velocidade, cor_base=(50, 200, 50))

    def atualizar(self, dt):
        self.atualizar_efeito_dano(dt)

class Inimigo(Boneco):
    def __init__(self, nome: str, x: float, y: float, vida: int = 50, armadura: int = 2, dano: int = 10, velocidade: float = 120.0, raio_visao: float = 200.0, cor_base=(90, 150, 80)):
        super().__init__(nome=nome, x=x, y=y, vida=vida, armadura=armadura, dano=dano, velocidade=velocidade, cor_base=cor_base)

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
        if alvo is None:
            return False
            
        # Só verifica estar_vivo() se 'alvo' for um Boneco (e não um Vector2)
        if hasattr(alvo, "estar_vivo") and not alvo.estar_vivo():
            return False

        dx = alvo.x - self.x
        dy = alvo.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        if 0 < distancia <= self.raio_visao:
            self.direcao_x = dx / distancia
            self.direcao_y = dy / distancia
            return True
        return False
    
    def atualizar(self, dt, alvo=None):
        if not self.estar_vivo():
            return

        self.atualizar_efeito_dano(dt)  
        perseguindo = self.perseguir_alvo(alvo) if alvo is not None else False 

        if not perseguindo:
            self.tempo_para_mudar -= dt
            if self.tempo_para_mudar <= 0:
                self.sortear_direcao()
                
        self.movimentacao(self.direcao_x, self.direcao_y, dt)   