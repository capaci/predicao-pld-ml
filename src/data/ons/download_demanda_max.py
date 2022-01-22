# %%
from tableauscraper import TableauScraper as TS

url = 'https://tableau.ons.org.br/t/ONS_Publico/views/DemandaMxima/HistricoDemandaMxima'


ts = TS()
ts.loads(url)
wb = ts.getWorkbook()

# %%
for t in wb.worksheets:
    print(f'worksheet name : {t.name}')

# %%
wb.getStoryPoints()
# %%
# %%
wb = wb.setParameter('Escala de Tempo DM Simp 4', 'Dia')
wb = wb.setParameter('Início Primeiro Período DM Simp 4', '01/01/2001')
wb = wb.setParameter('Fim Primeiro Período DM Simp 4', '26/12/2021')
# %%
wb = wb.setParameter('Selecione DM Simp 4', 'Demanda Máxima Horária (MWh/h)')
# wb = wb.setParameter("Selecione DM Simp 4", "Demanda Máxima Instântanea (MW)")

# %%
ws = wb.getWorksheet('Simples Demanda Máxima Semana Ano')

# %%


# %%
ws = wb.getWorksheet("Simples Demanda Máxima Ano")
print(ws.getFilters())

# Select subsystem
wb = ws.setFilter("Subsistema", "N")
ws = wb.getWorksheet("Simples Demanda Máxima Semana Dia")

# %%
print(ws.data)


# %%

ws.data.to_csv('/home/capaci/Documents/mba-usp/tcc/tcc-mba-cd-icmc/data/external/ons/demanda-maxima-diaria-sudeste.csv')

# %%
sp = wb.goToStoryPoint(storyPointId=2)

# %%
sp.getWorksheetNames()

# %%
ws = sp.getWorksheet('Comparativo Demanda Máxima Semana Dia')

# %%
print(ws.data.head())
# %%
sp.getParameters()
# %%
# %%
sp = sp.setParameter('Escala de Tempo DM Simp 4', 'Dia')
sp = sp.setParameter('Início Primeiro Período DM Simp 4', '01/01/2001')
sp = sp.setParameter('Fim Primeiro Período DM Simp 4', '26/12/2021')

