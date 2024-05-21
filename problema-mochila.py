# criação do código genético conforme exercício praticado em aula
import random
import numpy as np

# regras:
pesoMaximo = 40
mutacao = 0.1

# números aleatórios, fornecidos para o exercício apenas
randomPaiMelhor = 0.63
randomPaiPior = 0.27
randomGene = 0.77
randomMutacao = 0.08
randomPaiMutacao = 0.57
randomGeneMutacao = 0.45
randomNovoGeneMutacao = 0.98

# itens da mochila
items = [
# peso, valor, qtdLimit/e
  [3, 100, 7], #1º item
  [6, 200, 2], #2º item
  [4, 50,  5], #3º item
]

#depois deixar apenas a quantidade de itens, tirar o peso e valor
individuos = [
  # qtdItem1, qtdItem2, qtdItem3, pesoInd, valorInd
  [2, 2, 4, 34, 800],
  [4, 1, 3, 30, 750],
  [7, 0, 2, 29, 800],
  [1, 2, 4, 31, 700]
]

# gerando um indivíduo dentro das regras
def gerandoIndividuos():
  todosIndividuos = []  # Inicializa como uma lista vazia
  quantidadesInd = np.array([]) 
  somas = []

  contador = 0
  for x in range(0,4): #4 individuos
    novoIndiv = True
    contador += 1

    while novoIndiv:
      quantidades = []
      for item in items:
        quantidades.append(random.randint(0, item[2]))

      pesos = np.array([])
      for x in range(len(quantidades)):
        pesos = np.append(pesos, items[x][0]*quantidades[x])

      soma = np.sum(pesos)
      somas.append(soma)
      if soma <= 40:
        novoIndiv = False
        todosIndividuos.append(quantidades)
    
  # print('somas:',somas)
  individuos = []
  for x in range(len(todosIndividuos)):
    valor = calcValor(todosIndividuos[x])
    arr = [todosIndividuos[x][0], todosIndividuos[x][1], todosIndividuos[x][2], somas[x], valor]
    individuos.append(arr)

  return individuos

def calcValor(individuo):
  valor = 0
  for x in range(0,3):
    valor += individuo[x]*items[x][1]
  
  return valor

def calcPeso(individuo):
  valor = 0
  for x in range(0,3):
    valor += individuo[x]*items[x][0]

  return valor


def classificandoIndividuos(arrayInd):
  # colocando o idx antes de fazer a classicação para que depois a nova população seja criada corretamente
  individuosOrdenados = np.array(arrayInd)
  indices = np.arange(len(individuosOrdenados)).reshape(-1, 1) # Cria um array de índices
  individuosOrdenados = np.concatenate((individuosOrdenados, indices), axis=1)

  individuosOrdenados = sorted(individuosOrdenados, key=lambda x: x[4], reverse=True)
  somaMelhores = individuosOrdenados[0][4] + individuosOrdenados[1][4]
  somaPiores = individuosOrdenados[2][4] + individuosOrdenados[3][4]

  # print('Classificados: ', individuosOrdenados)
  # print('Soma Melhores: ', somaMelhores)
  # print('Soma Piores: ', somaPiores)
  escolhendoIndividuosCrossover(somaMelhores, somaPiores, individuosOrdenados)

def escolhendoIndividuosCrossover(somaMelhores, somaPiores, individuosClassificados):
  # calculando a percentagem de cada
  percIndividuos = np.array([])
  aux = 0
  for individuo in individuosClassificados:
    aux = aux + 1
    if(aux < 3):
      percIndividuos = np.append(percIndividuos, individuo[4]/somaMelhores)
    else:
      percIndividuos = np.append(percIndividuos, individuo[4]/somaPiores)

  # escolhendo um indivíduo dos melhores
  if(randomPaiMelhor < 1 and randomPaiMelhor > percIndividuos[0]):
    melhorEscolhido = individuosClassificados[1]
  else:
    melhorEscolhido = individuosClassificados[0]
  # print("Melhor escolhido: ", melhorEscolhido)
  
  # escolhendo um indivíduo dos piores
  if(randomPaiPior < 1 and randomPaiPior > percIndividuos[2]):
    piorEscolhido = individuosClassificados[3]
  else:
    piorEscolhido = individuosClassificados[2]
  # print("Pior escolhido: ", piorEscolhido)

  crossover(melhorEscolhido, piorEscolhido)

def crossover(individuoUm, individuoDois):
  # pegando a quantidade de genes que cada ind tem, retirando o valor, peso do indv e idx. E depois pegando a percentagem de chances de ser cada um
  qtdGenes = (100 / (len(individuoUm) - 3)) / 100 # deixando em decimal, não em percentagem

  if(randomGene >= 0 and randomGene <= qtdGenes):
    geneEscolhido = 0
  elif(randomGene > qtdGenes and randomGene <= (qtdGenes*2)):
    geneEscolhido = 1
  else:
    geneEscolhido = 2

  individuoUm[geneEscolhido], individuoDois[geneEscolhido] = individuoDois[geneEscolhido], individuoUm[geneEscolhido]

  # calculando novos pesos e valores
  individuoUm = novoPesoValor(individuoUm)
  individuoDois = novoPesoValor(individuoDois)

  #verificando se ainda respeita as regras de peso
  if(individuoUm[3] <= 40 and individuoDois[3] <= 40):
    arrCrossover = np.array([individuoUm, individuoDois])
    mutacaoIndividuo(arrCrossover)

# aqui irá receber os dois individuos que sofreram o crossover para ver se a mutação irá ocorrer e quem irá sofrer
def mutacaoIndividuo(array):
  # vendo se a mutação irá ocorrer
  if(randomMutacao <= mutacao):
    # pegando os indivíduos do crossover para ver o range pelo qual vai ser escolhido qual sofrerá a mutação
    mutacaoRange = 100 / len(array)
    
    if(randomPaiMutacao > 0 and randomPaiMutacao <= mutacaoRange/100):
      individuoMutar = array[0]
      idxMutado = 0
    else:
      individuoMutar = array[1]
      idxMutado = 1

    # escolhendo qual gene irá mutar
    qtdGene = (100 / (len(individuoMutar) - 3)) / 100 # tira o valor e peso, apenas os genes. Depois, reansforma em decimal
    
    if(randomGeneMutacao > 0 and randomGeneMutacao <= qtdGene):
      geneMutar = 0
    elif(randomGeneMutacao > qtdGene and randomGeneMutacao <= (qtdGene*2)):
      geneMutar = 1
    else:
      geneMutar = 2
    
    qtdMaximaGene = 100 / (items[geneMutar][2] + 1) # +1 pois é possível escolher o zero também
    rangeGenes = qtdMaximaGene/100

    novoValor = -1
    # vendo dentro de qual range o aleatorio está para saber qual o novo valor da mutação
    for x in range(0,int(100//qtdMaximaGene) +1):
      if(randomNovoGeneMutacao > rangeGenes*x and randomNovoGeneMutacao <= rangeGenes*(x+1)):
        novoValor = x

    # print("Indivíduo mutado (antes):", individuoMutar)
    individuoMutar[geneMutar] = novoValor
    # calculando novos valores e pesos
    individuoMutar[4] = calcValor(individuoMutar)
    individuoMutar[3] = calcPeso(individuoMutar)
    # print("Indivíduo mutado (depois):", individuoMutar)
    array[idxMutado] = individuoMutar
  # concatena os valores alterados na população, gerando uma nova
  gerarNovaPopulacao(array)

def gerarNovaPopulacao(arrayMutados):
  for x in range(len(arrayMutados)):
    # print(x, '-',arrayMutados[x])
    index = int(arrayMutados[x][5])
    individuos[index] =  [arrayMutados[x][0], arrayMutados[x][1], arrayMutados[x][2], arrayMutados[x][3], arrayMutados[x][4]]

  apresentarPopulacao(individuos)


def apresentarPopulacao(individuos):
  idx = 0
  for individuo in individuos:
    idx+=1
    print(f"{idx} - ITEM 1: {individuo[0]} ITEM 2: {individuo[1]} ITEM 3: {individuo[2]} PESO: {individuo[3]} VALOR: {individuo[4]}")

def novoPesoValor(individuo):
  # novoPeso
  individuo[3] = individuo[0]*items[0][0] + individuo[1]*items[1][0] + individuo[2]*items[2][0]
  # novo valor
  individuo[4] = individuo[0]*items[0][1] + individuo[1]*items[1][1] + individuo[2]*items[2][1]

  return individuo


# para gerar indivíduos aleatórios:
# individuos = gerandoIndividuos()
classificandoIndividuos(individuos)