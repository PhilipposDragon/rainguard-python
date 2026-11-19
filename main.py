"""
main.py - CitizenTech: RainGuard (monitoramento de alagamentos)
Disciplina: Computational Thinking with Python

Aplicação de terminal que recebe leituras de CHUVA (pluviômetro) e NÍVEL DA ÁGUA
(circuito Edge), simuladas ou digitadas, e classifica o estado de uma área:
Normal, Atenção ou Crítico. As regras seguem o circuito Edge: o nível define o
estado, chuva forte sobe um estado e sensor sem leitura é Crítico.
"""


# CONFIGURAÇÃO  -  Ajuste dos limites usados

# Nome e contexto de cada área
nomes_areas = [
    "Área 1 - Av. Dr. Ricardo Jafet x R. Paulo Bregaro",
    "Área 2 - Av. Teresa Cristina x R. Tabor",
]
contexto_areas = [
    "Ponto com histórico de alagamento documentado (fonte: CGE/Prefeitura de São Paulo). Leituras simuladas.",
    "Ponto com histórico de alagamento documentado (fonte: CGE/Prefeitura de São Paulo). Leituras simuladas.",
]

# Limite de CHUVA FORTE em mm/h (a partir dele o estado sobe um nível)
chuva_forte = [30.0, 30.0]

# Limites de NÍVEL DA ÁGUA em cm (a partir de quanto vira Atenção e Crítico)
nivel_atencao = [10.0, 10.0]
nivel_critico = [25.0, 25.0]

# Valores máximos aceitos na digitação (acima disso a leitura é considerada inválida)
chuva_maxima = 240.0
nivel_maximo = 40.0

# Estados (o número é a gravidade: 0 = menor, 2 = maior)
nomes_estados = ["Normal", "Atenção", "Crítico"]

# Cenários de simulação e o estado esperado de cada um
nomes_cenarios = ["Normal", "Atenção", "Crítico", "Sensor sem leitura"]
estado_do_cenario = [0, 1, 2, 2]

# Histórico da sessão (uma posição em cada lista por leitura)
hist_area = []
hist_chuva = []
hist_nivel = []
hist_estado = []


# FUNÇÕES

def texto_para_numero(texto):
    """
    Converte o texto digitado em número. Aceita vírgula (85,5).
    Devolve -1 se não for um número válido (não negativo).
    """
    texto = texto.strip().replace(",", ".")
    if texto.replace(".", "", 1).isnumeric():
        return float(texto)
    return -1


def classificar_valor(valor, limite_atencao, limite_critico):
    """
    Classifica um valor: 0 = Normal, 1 = Atenção, 2 = Crítico.
    """
    if valor >= limite_critico:
        return 2
    elif valor >= limite_atencao:
        return 1
    else:
        return 0


def classificar_leitura(area, chuva, nivel):
    """
    Classifica a leitura de uma área, como no circuito Edge:
    - o estado base vem do nível da água;
    - chuva forte (acima do limite) sobe um estado, até no máximo Crítico;
    - nível -1 significa sensor sem leitura e vira Crítico, por segurança.
    Devolve: estado final, se a chuva é forte (True/False), estado do nível.
    """
    forte = chuva >= chuva_forte[area]
    if nivel == -1:
        return 2, forte, 2
    estado_nivel = classificar_valor(nivel, nivel_atencao[area], nivel_critico[area])
    estado_final = estado_nivel
    if forte and estado_nivel < 2:
        estado_final = estado_nivel + 1
    return estado_final, forte, estado_nivel


def nome_chuva(area, chuva):
    """
    Nome da condição de chuva (mesmos nomes do circuito Edge).
    """
    if chuva <= 0:
        return "SEM CHUVA"
    elif chuva >= chuva_forte[area]:
        return "CHUVA FORTE"
    else:
        return "CHUVA"


def valores_do_cenario(area, cenario):
    """
    Gera chuva e nível de um cenário a partir dos limites da área,
    para que a simulação acompanhe qualquer ajuste feito na configuração.
    cenario: 0 = Normal, 1 = Atenção, 2 = Crítico, 3 = Sensor sem leitura.
    No cenário 3 o nível é -1 (sem leitura).
    """
    if cenario == 0:
        chuva = 0.0
        nivel = nivel_atencao[area] / 2
    elif cenario == 1:
        chuva = chuva_forte[area] / 2
        nivel = (nivel_atencao[area] + nivel_critico[area]) / 2
    elif cenario == 2:
        chuva = chuva_forte[area] * 1.2
        nivel = nivel_critico[area] * 1.2
    else:
        chuva = chuva_forte[area] / 2
        nivel = -1
    return chuva, nivel


def ler_numero(mensagem, maximo):
    """
    Pede um número até receber um válido. ENTER vazio devolve -1.
    """
    while True:
        texto = input(mensagem)
        if texto.strip() == "":
            return -1
        valor = texto_para_numero(texto)
        if valor == -1:
            print("  Entrada inválida: digite apenas um número (ex.: 12 ou 12,5).")
        elif valor > maximo:
            print(f"  Valor acima do máximo aceito ({maximo:g}). Verifique a leitura.")
        else:
            return valor


def escolher_area(area_atual):
    """
    Mostra as áreas e devolve a posição da área escolhida.
    """
    print("\nÁreas de demonstração:")
    for i, nome in enumerate(nomes_areas, start=1):
        print(f"  {i} - {nome}")
    escolha = input("Escolha a área: ")
    if escolha.isnumeric() and 1 <= int(escolha) <= len(nomes_areas):
        nova = int(escolha) - 1
        print(f"  Área selecionada: {nomes_areas[nova]}")
        print(f"  Contexto: {contexto_areas[nova]}")
        return nova
    print("  Opção inválida. A área não foi alterada.")
    return area_atual


def registrar_leitura(area, chuva, nivel):
    """
    Classifica a leitura, guarda no histórico e mostra o resultado.
    """
    estado, forte, estado_nivel = classificar_leitura(area, chuva, nivel)
    hist_area.append(area)
    hist_chuva.append(chuva)
    hist_nivel.append(nivel)
    hist_estado.append(estado)

    print(f"\n  {nomes_areas[area]}")
    print(f"  Chuva: {chuva:.1f} mm/h -> {nome_chuva(area, chuva)}")
    if nivel == -1:
        print("  Nível da água: SEM LEITURA (sensor com falha) -> tratado como Crítico")
    else:
        print(f"  Nível da água: {nivel:.1f} cm -> {nomes_estados[estado_nivel]}")
    if forte and estado_nivel < 2:
        print("  Chuva forte: o estado sobe um nível.")
    print(f"  ESTADO DA ÁREA: {nomes_estados[estado].upper()}")

    match estado:
        case 2:
            print("  >> Evite passar por este ponto e siga as orientações oficiais (Defesa Civil: 199).")
        case 1:
            print("  >> Acompanhe a situação: as condições do local pioraram.")
        case _:
            print("  >> Sem sinais de risco nesta leitura.")


def inserir_leitura(area):
    """
    Pede chuva e nível ao usuário e registra a leitura.
    """
    print(f"\nInserir leitura para: {nomes_areas[area]}")
    chuva = ler_numero("Chuva (mm/h) [ENTER vazio cancela]: ", chuva_maxima)
    if chuva == -1:
        print("  Leitura cancelada.")
        return
    nivel = ler_numero("Nível da água (cm) [ENTER vazio = sensor sem leitura]: ", nivel_maximo)
    registrar_leitura(area, chuva, nivel)


def simular_cenario(area):
    """
    Registra uma leitura simulada de um dos quatro cenários.
    """
    print("\nCenários: 1 - Normal   2 - Atenção   3 - Crítico   4 - Sensor sem leitura")
    escolha = input("Escolha o cenário: ")
    if escolha.isnumeric() and 1 <= int(escolha) <= 4:
        cenario = int(escolha) - 1
        chuva, nivel = valores_do_cenario(area, cenario)
        print(f"\n--- Cenário simulado: {nomes_cenarios[cenario]} ---")
        registrar_leitura(area, chuva, nivel)
    else:
        print("  Opção inválida.")


def ver_historico():
    """
    Mostra todas as leituras da sessão.
    """
    if len(hist_estado) == 0:
        print("  Nenhuma leitura registrada nesta sessão.")
        return
    print("\n  Nº  Área  Chuva(mm/h)  Nível(cm)  Estado")
    contagem = [0, 0, 0]
    for i in range(len(hist_estado)):
        if hist_nivel[i] == -1:
            texto_nivel = "---"
        else:
            texto_nivel = f"{hist_nivel[i]:.1f}"
        print(f"  {i + 1:<3} {hist_area[i] + 1:<5} {hist_chuva[i]:<12.1f} "
              f"{texto_nivel:<10} {nomes_estados[hist_estado[i]]}")
        contagem[hist_estado[i]] += 1
    print(f"\n  Total: {len(hist_estado)} leituras | "
          f"Normal: {contagem[0]} | Atenção: {contagem[1]} | Crítico: {contagem[2]}")


def autoteste():
    """
    Confere se os cenários estão certos.
    """
    falhas = 0
    total = 0

    print("\n=== CENÁRIOS SIMULADOS POR ÁREA ===")
    for area in range(len(nomes_areas)):
        for cenario in range(4):
            chuva, nivel = valores_do_cenario(area, cenario)
            obtido = classificar_leitura(area, chuva, nivel)[0]
            total += 1
            if obtido == estado_do_cenario[cenario]:
                resultado = "OK    "
            else:
                resultado = "FALHOU"
                falhas += 1
            if nivel == -1:
                texto_nivel = "sem leitura"
            else:
                texto_nivel = f"{nivel:.1f}"
            print(f"  {resultado} Área {area + 1} | {nomes_cenarios[cenario]}: "
                  f"chuva {chuva:.1f}, nível {texto_nivel} -> {nomes_estados[obtido]}")

    print("\n=== REGRAS DE CLASSIFICAÇÃO ===")
    area = 0
    casos = [
        ("Nível exatamente no limite de Atenção, sem chuva", 0.0, nivel_atencao[area], 1),
        ("Nível exatamente no limite Crítico, sem chuva", 0.0, nivel_critico[area], 2),
        ("Chuva abaixo do limite forte não muda o estado", chuva_forte[area] - 0.1, 0.0, 0),
        ("Chuva forte com nível Normal sobe para Atenção", chuva_forte[area], 0.0, 1),
        ("Chuva forte com nível em Atenção sobe para Crítico", chuva_forte[area], nivel_atencao[area], 2),
        ("Chuva forte com nível Crítico continua Crítico", chuva_forte[area], nivel_critico[area], 2),
        ("Sensor sem leitura vira Crítico", 0.0, -1, 2),
        ("Tudo zerado é Normal", 0.0, 0.0, 0),
    ]
    for descricao, chuva, nivel, esperado in casos:
        obtido = classificar_leitura(area, chuva, nivel)[0]
        total += 1
        if obtido == esperado:
            resultado = "OK    "
        else:
            resultado = "FALHOU"
            falhas += 1
        print(f"  {resultado} {descricao}: {nomes_estados[obtido]}")

    print("\n=== TRATAMENTO DE ENTRADAS ===")
    entradas = [("12", 12.0), ("12,5", 12.5), ("abc", -1), ("", -1), ("-3", -1), ("1.2.3", -1)]
    for texto, esperado in entradas:
        obtido = texto_para_numero(texto)
        total += 1
        if obtido == esperado:
            resultado = "OK    "
        else:
            resultado = "FALHOU"
            falhas += 1
        print(f"  {resultado} entrada '{texto}' -> {obtido} (esperado {esperado})")

    print(f"\nResultado: {total - falhas} de {total} testes passaram.")


def mostrar_menu(area):
    print("\n" + "=" * 52)
    print("   RAINGUARD - monitoramento de alagamentos")
    print("=" * 52)
    print(f"Área atual: {nomes_areas[area]}")
    print("1 - Escolher área")
    print("2 - Inserir leitura (chuva e nível da água)")
    print("3 - Simular cenário (Normal, Atenção, Crítico ou sensor sem leitura)")
    print("4 - Consultar histórico da sessão")
    print("5 - Executar autoteste dos cenários")
    print("0 - Encerrar")


def main():
    area_atual = 0
    while True:
        mostrar_menu(area_atual)
        opcao = input("Escolha: ")
        match opcao:
            case "1":
                area_atual = escolher_area(area_atual)
            case "2":
                inserir_leitura(area_atual)
            case "3":
                simular_cenario(area_atual)
            case "4":
                ver_historico()
            case "5":
                autoteste()
            case "0":
                print("Encerrando. Em caso de emergência, ligue 199 (Defesa Civil).")
                break
            case _:
                print("  Opção inválida. Escolha um número do menu.")
        input("\nPressione Enter para continuar . . .")


main()