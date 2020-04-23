import math

class ITA_DeadReckoning2d:

    def __init__(self):
        self.ultimoTempo = 0        # Último tempo, usado pra calcular o intervalo de tempo
        self.pospredictX = 1000     # Posição X estimada pelo algoritmo
        self.pospredictY = 1000     # Posição Y estimada pelo algoritmo
        self.ultimoGpsX = 0
        self.timeToGround = 0
        self.posPayloadDropX = 1000
        self.posPayloadDropY = 1000
        self.distCargaAlvo = 1000
        self.erroAlinhamento = 0
        self.head_aviao_alvo = 0
        self.erroAlinhamento = 0


    def estimaPosi(self, gpsx, gpsy, head, vel, tempoAtual, xAlvo, yAlvo):

        # GPS atualizou
        if(self.ultimoGpsX != gpsx):
            self.pospredictX = gpsx
            self.pospredictY = gpsy
            self.ultimoGpsX = gpsx

        # Se o GPS ainda não atualizou
        else:
            self.pospredictX = self.pospredictX + math.cos(head*math.pi/180)*vel*(tempoAtual-self.ultimoTempo)
            self.pospredictY = self.pospredictY + math.sin(head*math.pi/180)*vel*(tempoAtual-self.ultimoTempo)
        self.ultimoTempo = tempoAtual

        self.distAviaoAlvo = math.sqrt((self.pospredictX-xAlvo)**2+(self.pospredictY-yAlvo)**2)

        # Limita posição X em 1000
        if(self.pospredictX > 1000):
            self.pospredictX = 1000
        if(self.pospredictX < -1000):
            self.pospredictX = -1000

        # Limita posição Y em 1000
        if(self.pospredictY > 1000):
            self.pospredictY = 1000
        if(self.pospredictY < -1000):
            self.pospredictY = -1000
    
        return self.pospredictX, self.pospredictY
        


    def estimaPosiCarga(self, altitude, head, vel, tempoAjuste, xAlvo, yAlvo):
        # Tempo para carga chegar no chão
        self.timeToGround = math.sqrt(2*abs(altitude)/9.8)

        self.posPayloadDropX = self.pospredictX + math.cos(head*math.pi/180)*vel*(self.timeToGround+tempoAjuste)
        self.posPayloadDropY = self.pospredictY + math.sin(head*math.pi/180)*vel*(self.timeToGround+tempoAjuste)

        self.distCargaAlvo = math.sqrt((self.posPayloadDropX-xAlvo)**2+(self.posPayloadDropY-yAlvo)**2)


        # Limita posição carga X em 1000
        if(self.posPayloadDropX > 1000):
            self.posPayloadDropX = 1000
        if(self.posPayloadDropX < -1000):
            self.posPayloadDropX = -1000

        # Limita posição carga Y em 1000
        if(self.posPayloadDropY > 1000):
            self.posPayloadDropY = 1000
        if(self.posPayloadDropY < -1000):
            self.posPayloadDropY = -1000

        if(self.distCargaAlvo > 1000):
            self.distCargaAlvo = 1000
        if(self.distCargaAlvo < -1000):
            self.distCargaAlvo = -1000

        headProvi = (math.atan2((self.pospredictY-yAlvo),(self.pospredictX-xAlvo)))*180/(math.pi)

        #atan2 trabalha entre -pi e pi, enquanto o head do gps trabalha entre 0 e 360,
        # então padronizamos tudo para trabalhar entre 0 e 360
        self.head_aviao_alvo = (headProvi+180)
        alinhaerro = self.head_aviao_alvo - head

        if(alinhaerro > 180):
            alinhaerro = alinhaerro-360
        self.erroAlinhamento = alinhaerro

        return self.posPayloadDropX, self.posPayloadDropY



