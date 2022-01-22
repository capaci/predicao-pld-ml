# Bases de dados

Breve descrição das bases de dados utilizadas e das variáveis originais, antes de qualquer transformação


## Bases

### PLD Horário

Preço de Liquidação das Diferenças. Basicamente o preço da energia. 

**Fonte**: [https://www.ccee.org.br/web/guest/precos/painel-precos](https://www.ccee.org.br/web/guest/precos/painel-precos)

#### Método para obtenção dos dados

1. Na seção "Planilhas para download dos dados históricos", selecionar o tipo como "Preço horário"
2. É disponibilizado um link com a série histórica até uma certa data (até a publicação do trabalho, a data disponível era até 02/12/2021)
3. Baixar essa planilha ([link original](
Planilhas para download dos dados históricos
https://www.ccee.org.br/documents/80415/919464/Hist%C3%B3rico+do+Pre%C3%A7o+Hor%C3%A1rio+17+de+abril+de+2018+a+2+de+dezembro+de+2021.xls/e014d4d9-f805-0173-f9a3-45eb2726c176?version=1.0&t=1638487606389&download=true))

4. Caso os dados disponíveis sejam anteriores a 30/12/2021, selecionar as datas faltantes nos campos de data e clicar em "Gerar Arquivo"
5. Baixar o arquivo com o restante dos dados


### Demanda Máxima

**Fonte**: <a href="http://www.ons.org.br/Paginas/resultados-da-operacao/historico-da-operacao/demanda_maxima.aspx" target="_blank">http://www.ons.org.br/Paginas/resultados-da-operacao/historico-da-operacao/demanda_maxima.aspx</a>


#### Método pra obtenção dos dados

1. Acessar a url
2. Selecionar o *storybook* "Comparativo"
3. Definir os seguintes parâmetros de filtros
   - Demanda Máxima Horária (MWh/h)
   - **Escala de tempo**: Dia
   - **Subsistema**: "Nordeste", "Norte", "Sudeste/Centro-Oeste" e "Sul"
   - **Período Início**: 01/01/2001
   - **Período Fim**: 26/12/2021
4. Clicar no eixo Y
5. Clicar no botão "Baixar" no rodapé
6. Clicar na opção "Dados"
7. Na janela que se abrirá, clicar em "Baixar todas as linhas como um arquivo de texto"


### Geração de Energia

**Fonte**: <a href="http://www.ons.org.br/Paginas/resultados-da-operacao/historico-da-operacao/demanda_maxima.aspx" target="_blank">http://www.ons.org.br/Paginas/resultados-da-operacao/historico-da-operacao/demanda_maxima.aspx</a>


#### Método pra obtenção dos dados

1. Acessar a url
2. Selecionar o *storybook* "Comparativo"
3. Definir os seguintes parâmetros de filtros
   - Demanda Máxima Horária (MWh/h)
   - **Escala de tempo**: Dia
   - **Subsistema**: "Nordeste", "Norte", "Sudeste/Centro-Oeste" e "Sul"
   - **Período Início**: 01/01/2001
   - **Período Fim**: 26/12/2021
4. Clicar no eixo Y
5. Clicar no botão "Baixar" no rodapé
6. Clicar na opção "Dados"
7. Na janela que se abrirá, clicar em "Baixar todas as linhas como um arquivo de texto"



### Energia Armazenada (EAR) Diário por Subsistema

Dados de Energia Armazenada (EAR) em periodicidade diária por Subsistema.  Esta 
grandeza representa a energia associada ao volume de  água armazenado nos reservatórios que 
pode  ser  convertido  em  geração  na  própria  usina  e  em  todas  as  usinas  a  jusante  da  cascata.  A 
grandeza de EAR considera o nível verificado nos reservatórios na data de referência. A grandeza 
de EAR máxima é a capacidade de armazenamento caso todos os reservatórios estivessem cheios. 


**Fonte**: <a href="https://dados.ons.org.br/dataset/ear-diario-por-subsistema" target="_blank">https://dados.ons.org.br/dataset/ear-diario-por-subsistema</a>

#### Dicionário das variáveis originais

|Descrição|Código|Tipo de Dado|Formato|
|---|---|---|---|
|Código do Subsistema |id_subsistema|TEXTO|2 POSIÇÕES|
|Nome da Subsistema|nom_subsistema|TEXTO|20 POSIÇÕES|
|Dia observado da medida|ear_data|DATETIME|YYYY-MM-DD|
|Valor de EAR máxima por subsistema na unidade de medida MWmês|ear_max_subsistema|FLOAT||
|Valor de EAR verificada no dia por subsistema na unidade de medida MWmês|ear_verif_subsistema_mwmes|FLOAT||
|Valor de EAR verificada no dia por subsistema na unidade de medida %|ear_verif_subsistema_percentual|FLOAT||
 

### Energia Natural de Afluentes (ENA) Diário por Subsistema

Dados de Energia Natural Afluente (ENA) em periodicidade diária por Subsistema. A ENA Bruta representa a energia produzível pelo reservatório e é calculada pelo produto das vazões naturais aos reservatórios com as produtividades a 65% dos volumes úteis. A ENA Armazenável considera as vazões naturais descontadas das vazões vertidas nos reservatórios. 


**Fonte**: <a href="https://dados.ons.org.br/dataset/ena-diario-por-subsistema" target="_blank">https://dados.ons.org.br/dataset/ena-diario-por-subsistema</a>

|Descrição|Código|Tipo de Dado|Formato|
|---|---|---|---|
|Código do Subsistema|id_subsistema|TEXTO|2 POSIÇÕES|
|Nome da Subsistema|nom_subsistema|TEXTO|20 POSIÇÕES|
|Dia observado da medida|ena_data|DATETIME|YYYY-MM-DD|
|Valor de ENA bruta por Subsistema na unidade de medida MWmês|ena_bruta_regiao_mwmed|FLOAT||
|Valor de ENA bruta por Subsistema medido em percentual por média de longo termo-MLT (%)|ena_bruta_regiao_percentualmlt|FLOAT||
|Valor de ENA armazenável por Subsistema na unidade de medida MWmês|ena_armazenavel_regiao_mwmed|FLOAT||
|Valor de ENA armazenável por subsistema em percentual por média de longo termo-MLT (%)|ena_armazenavel_regiao_percentualmlt|FLOAT||
 

### Carga de Energia

**Fonte**: <a href="https://dados.ons.org.br/dataset/carga-energia" target="_blank">https://dados.ons.org.br/dataset/carga-energia</a>

Dados de carga por subsistema numa data de referência em base diária.  
 
|Descrição|Código|Tipo de Dado|Formato|
|---|---|---|---|
|Código do Subsistema|id_subsistema|TEXTO|3 POSIÇÕES|
|Nome do Subsistema|nom_subsistema|TEXTO|20 POSIÇÕES|
|Data de referência|din_instante|DATETIME|YYYY-MM-DD HH:MM:SS|
|Valor da Carga de Energia, em MWmed|val_cargaenergiamwmed|FLOAT||
  


### Intercâmbio entre Subsistemas

Dados de intercâmbio entre subsistemas em **base horária**, em MWmed. As 
grandezas representam a soma das medidas de fluxo de potência ativa nas linhas de transmissão 
de fronteira entre os subsistemas.   
Observações: (1) A relação de linhas de transmissão de fronteira pode ser encontrada no produto 
"Relatório  Quadrimestral  de  Limites  de  Intercâmbio  para  o  Modelo  Newave",  disponível  Portal 
SINtegre - ONS.  (2) O intercâmbio do subsistema Sul com os países vizinhos não consta nesta 
consulta e pode ser obtido nos dados de intercâmbio do SIN. 
 
**Fonte**: <a href="https://dados.ons.org.br/dataset/intercambio-nacional" target="_blank">https://dados.ons.org.br/dataset/intercambio-nacional</a>

|Descrição|Código|Tipo de Dado|Formato|
|---|---|---|---|
|Data/hora  (início  do  período  de agregação)|din_instante|DATETIME YYYY-MM-DD HH:MM:SS|
|Código do Subsistema de Origem|id_subsistema_origem|TEXTO|3 POSIÇÕES|
|Nome do Subsistema de Origem|nom_subsistema_origem|TEXTO|20 POSIÇÕES|
|Código do Subsistema de Destino|id_subsistema_destino|TEXTO|3 POSIÇÕES|
|Nome do Subsistema de Destino|nom_subsistema_destino|TEXTO|20 POSIÇÕES|
|Intercâmbio verificado em base horária, representando a soma das medidas de fluxo de potência ativa nas linhas de transmissão de fronteira entre os subsistemas em MWmed|val_intercambiomwmed|FLOAT||
 




## Test Heading 1

This is a text block

### Small heading

Another *hello*, **hello**

    quoation
    hello

```{tip}
This is a tip
```

```{warning}
This is a warning
```

```{note} Título da nota
And here's a note with a colon fence!
```

```{seealso}
See also
```

```{admonition} Here's my title
Here's my admonition content
```

```html
<h1>code block example</h1>
```
[123](launch)

```sql
select * from tables;
insert into tables values ('a','b');
```

## Some links

[python](http://www.python.org)

[Westpac](http://www.westpac.com.au)

[How to install Read The Doc](https://github.com/rtfd/sphinx_rtd_theme)

## Let's see a table

|------------|------------|-----------|
| Header 1   | Header 2   | Header 3  |
|:-----------|:----------:|----------:|
| body row 1 | column 2   | column 3  |
| body row 2 | Cells may s| pan columns.|
| body row 3 | Cells may  | - Cells   |
| body row 4 |            | - blocks. |
