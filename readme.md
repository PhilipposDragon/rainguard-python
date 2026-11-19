# RainGuard
 
## Ficha da CitizenTech
 
| Campo | Resposta |
|---|---|
| **Nome da CitizenTech** | RainGuard |
| **Cidade, bairro** | São Paulo, região do Ipiranga |
| **Cidadão beneficiado** | Moradores e pessoas que passam por locais sujeitos a alagamentos |
| **Problema, em uma frase** | Moradores e pessoas que passam pelo Ipiranga não sabem, antes de chegar a pontos que alagam, se há risco de alagamento naquele momento. |
| **Como funciona** | Combina chuva, nível da água e relatos da comunidade para mostrar o estado de um ponto: Normal, Atenção ou Crítico. |
| **O que cada parte faz** | **Python:** classifica as leituras em menu. **Edge (Wokwi):** circuito com os mesmos estados. **Front-end e Web:** página com módulo interativo de consulta. **Matemática:** modela os limites. |
| **Link do repositório** | https://github.com/PhilipposDragon/rainguard-python |
| **Indicador de impacto** | Cenários classificados como esperado no autoteste: 4 de 4 (normal, atenção, crítico e sensor sem leitura), nas duas áreas. É uma medida do protótipo, não de impacto comprovado. |
| **ODS conectados** | 11 e 13 |
 
## Equipe
 
| Nome | RM |
|---|---|
| Filipe Silva Fava | RM 574535 |
| Matheus Silveira Salvatico | RM 575556 |
| João Vitor Cordeiro De Godoi | RM 576228 |
| Kaio Henrique dos Santos Sousa | RM 574401 |
| Mateus Latorre da Silva | RM 574670 |
 
## Sobre esta parte: Computational Thinking with Python
 
Aplicação de terminal que recebe leituras de **chuva** (mm/h) e **nível da água** (cm), digitadas ou simuladas, e classifica o estado de uma de duas áreas de demonstração. As regras seguem as do circuito Edge (Wokwi).
 
### Menu
 
| Opção | O que faz |
|---|---|
| 1 | Escolhe a área de demonstração |
| 2 | Insere uma leitura de chuva e nível. ENTER vazio na chuva cancela; ENTER vazio no nível significa sensor sem leitura |
| 3 | Simula um cenário: Normal, Atenção, Crítico ou Sensor sem leitura |
| 4 | Mostra o histórico da sessão |
| 5 | Executa o autoteste dos cenários e das regras |
| 0 | Encerra |
 
### Regra de classificação
 
1. O **nível da água** define o estado base: Normal, Atenção ou Crítico.
2. **Chuva forte** sobe o estado em um nível, até no máximo Crítico.
3. **Sensor sem leitura** (nível não informado) vira Crítico, por segurança, como no circuito Edge.

| Item | Limite usado (igual ao Edge) |
|---|---|
| Nível de Atenção | a partir de 10 cm |
| Nível Crítico | a partir de 25 cm |
| Chuva forte | a partir de 30 mm/h |
 
| Situação | Estado final |
|---|---|
| Nível abaixo de 10 cm, sem chuva forte | Normal |
| Nível abaixo de 10 cm, com chuva forte | Atenção |
| Nível de 10 a 24,9 cm, sem chuva forte | Atenção |
| Nível de 10 a 24,9 cm, com chuva forte | Crítico |
| Nível a partir de 25 cm | Crítico |
| Sensor sem leitura | Crítico |
 
### Cenários de teste
 
| Cenário | Chuva | Nível | Estado esperado |
|---|---|---|---|
| Normal | 0 mm/h | 5 cm | Normal |
| Atenção | 15 mm/h | 17,5 cm | Atenção |
| Crítico | 36 mm/h | 30 cm | Crítico |
| Sensor sem leitura | 15 mm/h | sem leitura | Crítico |
 
O autoteste (opção 5) confere esses cenários nas duas áreas, as regras de classificação e o tratamento de entradas: 22 testes.
 
### Como ajustar áreas e limites
 
Tudo fica no bloco **CONFIGURAÇÃO** no começo do `main.py`: `nomes_areas`, `contexto_areas`, `chuva_forte`, `nivel_atencao`, `nivel_critico`, `chuva_maxima` e `nivel_maximo`. Cada lista tem um valor por área, na mesma ordem. Os cenários simulados e o autoteste são calculados a partir desses limites, então acompanham qualquer ajuste. Os valores atuais seguem o Edge, que tem um único sensor, por isso as duas áreas usam os mesmos limites.
 
### Tratamento de entradas
 
Aceita vírgula ou ponto decimal. Texto, número negativo e valor acima do máximo aceito (`chuva_maxima` = 240 mm/h, `nivel_maximo` = 40 cm) geram mensagem de erro e pedem novamente. Deixar o nível em branco não é erro de digitação: é tratado como sensor sem leitura.
 
### Conceitos de programação aplicados
 
Entrada e saída, conversões, operadores, `if/elif/else`, `match/case`, `while True`, `for` com `range` e `enumerate`, listas e `append`, funções com retorno, validação com `isnumeric()` e acumuladores.
 
### Limitações
 
- As leituras são digitadas ou simuladas, sem conexão ao vivo com o Wokwi ou com o site.
- As duas áreas têm histórico de alagamento documentado pela CGE/Prefeitura de São Paulo, mas as leituras de chuva e nível são simuladas, e os limites são hipóteses didáticas, não dados oficiais.
- A ferramenta é informativa e não substitui os alertas da Defesa Civil.

### Uso de IA
 
Veja o arquivo `prompt.md`.
