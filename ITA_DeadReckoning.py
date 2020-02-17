import math

class ITA_DeadReckoning:

    def __init__(self):
        self.ultimoTempo = 0        # Último tempo, usado pra calcular o intervalo de tempo
        self.ultimoDistAlvoGPS = 0  # Ultima distância que o módulo do GPS informou que o avião encontra-se do alvo
        self.sinalPredict = 1       # Sinal que indica se o avião está se afastando ou se aproximando do alvo
        self.distAlvoPredict = 1000    # Distância que o deadreckoning acha que está do alvo nesse momento.
        self.pos = 1000
        
    # Função utilizada para realizar o deadreckoning 1D.
    # A ideia é que conforme o avião vai se aproximando do alvo, no intervalo que o GPS não pega dado, a distância do alvo
    #   vai sendo diminuída de acordo com a velocidade do avião
    def estimaPosi(self, distAlvoGPS, vel, tempoAtual):
    # Se o GPS atualizou agora, confiamos segamente na posição fornecida por ele
        if(self.ultimoDistAlvoGPS != distAlvoGPS):
            self.distAlvoPredict = distAlvoGPS
            if(self.ultimoDistAlvoGPS > distAlvoGPS):
                self.sinalPredict = -1
            else:
                self.sinalPredict = 1
            self.ultimoDistAlvoGPS = distAlvoGPS
        # Se o GPS ainda não atualizou
        else:
            self.distAlvoPredict = self.distAlvoPredict + self.sinalPredict*vel*(tempoAtual-self.ultimoTempo)
        self.ultimoTempo = tempoAtual
        if(self.distAlvoPredict > 1000):
            self.distAlvoPredict = 1000
        if(self.distAlvoPredict < -1000):
            self.distAlvoPredict = -1000
        self.pos = self.distAlvoPredict
        return self.distAlvoPredict





