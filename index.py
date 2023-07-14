#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

 

# Configurar pandas para mostrar todas las columnas

pd.set_option('display.max_columns', None)

 

# Configurar pandas para mostrar todas las filas

pd.set_option('display.max_rows', None)

 

fecha_generacion = str(input('Ingrese la fecha de generación del informe'))

 

print('Configurando columnas')

columns_rendimientos = ['Código de fondo',  'Código interno del afiliado',  'tipo_id_rendimientos', 'numero_id_rendimientos',   'Fecha calculo saldo',  'Saldo final en cuotas al ge',  'Saldo en pesos a la fecha   ', 'Pesos historicos totales   ',  'Rendimientos totales       ',  'Valor final cuenta individu',  'Saldo final en cuotas oblig',  'Saldo en pesos obligatorias',  'Pesos historicos cot. obl.',   'Rendimientos cot. oblig.', 'Saldo final en cuotas volunt', 'Saldo en pesos voluntaria a',  'Pesos historicos CVA       ',  'Rendimientos CVA           ',  'Saldo final en cuotas volun',  'Saldo en pesos volunt emple',  'Pesos historicos CVE       ',  'Rendimientos CVE           ',  'Saldo total voluntarias ent ', 'Saldo total voluntarias en',   'Pesos hist. aportes vol. to',  'Rendim. aportes vol. totale',  'retenciones contingentes   ',  'Aportes oblig. RAIS         ', 'Rend.CO fondo actual       ',  'Rendimientos RAIS           ', 'Total aportes               ', 'Total rendimientos         ',  'Saldo total ahorrado       ',  'Valor seguro previsional   ',  'Tipo novedad               ',  'Usuario modificación       ',  'Fecha modificación']

columns_prima = ['planilla', 'tipo_id_prima',   'numero_id_prima',  'Codigo interno del afiliado_prima',    'Fecha en que se hizo el dep',  'Perido cotizado_prima',    'Valor Prima seguro',   'Tipo de transaccion y conce',  'Tipo de transaccion y conc',   'Estado del movimiento',    'Subestado', 'periodo cotizado prima']

columns_contraloria = ['PERIODO',   'NIT',  'RAZON_SOCIAL_AFP', 'tipo_id_contraloria',  'numero_id_contraloria',    'AF_PRIMERNOMBRE',  'AF_SEGUNDONOMBRE', 'AF_PRIMERAPELLIDO',    'AF_SEGUNDOAPELLIDO',   'FECHA_DE_NACIMIENTO',  'GÉNERO',   'COD_MUNIC_NACIMIENTO', 'NOMBRE_MUNIC_NACIMIENTO',  'COD_DEPART_NACIMIENTO',    'NOMBRE_DEPART_NACIMIENTO', 'COD_MUNIC_RESIDENCIA', 'NOMBRE_MUNIC_RESIDENCIA',  'COD_DEPART_RESIDENCIA',    'NOMBRE_DEPART_RESIDENCIA', 'FECHA_AFILIACION', 'FECHA_DESVINCULACION', 'ESTADO_AFILIADO',  'COTIZANTE',    'SALARIO',  'Cobertura Seguros Previsionales',  'TIPO_DE_NOVEDAD',  'SEMANAS_REGIMEN_PRIMA_MEDIA',  'SEMANAS_REGIMEN_AHORRO_INDIVIDUAL_CON_SOLIDARIDAD',    'TOTAL_SEMANAS_COTIZADAS',  'APORTES_OBLIGATORIOS_ACUMULADOS',  'APORTES_VOLUNTARIOS_NETOS_ACUMULADOS', 'RENDIMIENTOS_AHORRO_INDIVIDUAL_OBLIGATORIO',   'RENDIMIENTOS_AHORRO_INDIVIDUAL_VOLUNTARIO',    'SALDO_TOTAL_AHORRADO', 'NOMBRE_FONDO(S)',  'VALOR_FONDO_MODERADO', 'VALOR_FONDO_CONSERVADOR',  'VALOR_FONDO_MAYOR_RIESGO', 'RENDIMIENTOS_FONDO_MODERADO',  'RENDIMIENTOS_FONDO_CONSERVADOR',   'RENDIMIENTOS_FONDO_MAYOR_RIESGO']

 

print("Leyendo archivo de rendimientos")

df_rendimientos = pd.DataFrame(pd.read_csv('rendimientos.csv', sep=';', names=columns_rendimientos))

print("Leyendo archivo de prima")

df_prima = pd.DataFrame(pd.read_csv('prima.csv', header=None, sep=';', encoding='ISO-8859-1', names=columns_prima))

print("Leyendo archivo de contraloria")

df_contraloria = pd.DataFrame(pd.read_csv('contraloria.csv', sep=';', header=None, encoding='ISO-8859-1', names=columns_contraloria))

print("Leyendo archivo IDCONTRALORIA")

df_idcontraloria = pd.DataFrame(pd.read_csv('IDCONTRALORIA.csv', sep=';'))

 

#df_rendimientos.head(10000).to_csv('rendimientos2.csv')

 

print('Sumando rendimientos por número de documento')

afondos = df_rendimientos.pivot_table(index=['tipo_id_rendimientos', 'numero_id_rendimientos'], columns='Código de fondo', values='Saldo total ahorrado       ', aggfunc='sum')

 

print('Renombrando Afondos')

nombres_originales_afondos = afondos.columns.tolist()

nuevos_nombres_afondos = ['VALOR_FONDO_CONSERVADOR_prima', 'VALOR_FONDO_MODERADO_prima', 'VALOR_FONDO_MAYOR_RIESGO_prima']

diccionario_nombres = dict(zip(nombres_originales_afondos, nuevos_nombres_afondos))

afondos = afondos.rename(columns=diccionario_nombres)

 

#rfondos = df_rendimientos.pivot_table(index=['tipo_id_rendimientos', 'numero_id_rendimientos'], columns='Código de fondo', values='Total rendimientos         ', aggfunc='sum')

print('Calculando rendimientos')

calculos = df_rendimientos.groupby(['tipo_id_rendimientos', 'numero_id_rendimientos']).agg({'Aportes oblig. RAIS         ': 'sum', 'Pesos hist. aportes vol. to': 'sum', 'Rendimientos RAIS           ': 'sum', 'Rendim. aportes vol. totale': 'sum', 'Saldo total ahorrado       ': 'sum'})

print('Sumando valor de prima por número de documento')

vlr_prima = df_prima.groupby(['tipo_id_prima', 'numero_id_prima']).agg({'Valor Prima seguro': 'sum', 'Perido cotizado_prima':'max'})

 

#vlr_prima.head(10)

print('Uniendo contraloria con IDCONTRALORIA')

merge_id_contraloria = df_contraloria.merge(df_idcontraloria, left_on=df_contraloria['tipo_id_contraloria'], right_on=df_idcontraloria['tipo id'],how='left')

print('Uniendo contraloria con rendimientos')

merge_afondos = merge_id_contraloria.merge(afondos, left_on=['dato_futura', 'numero_id_contraloria'], right_on=['tipo_id_rendimientos', 'numero_id_rendimientos'] ,how='left')



 

#merge_rfondos = merge_afondos.merge(rfondos, left_on=['dato_futura', 'numero_id_contraloria'], right_on=['tipo_id_rendimientos', 'numero_id_rendimientos'])

print('Uniendo contraloria con calculos de rendimientos')

merge_calculos = merge_afondos.merge(calculos, left_on=['dato_futura', 'numero_id_contraloria'], right_on=['tipo_id_rendimientos', 'numero_id_rendimientos'],how='left')

print('Uniendo contraloria con valor de prima')

merge_vlr_prima = merge_calculos.merge(vlr_prima, left_on=['dato_futura', 'numero_id_contraloria'], right_on=['tipo_id_prima', 'numero_id_prima'],how='left')



 

print('Agrupando columnas')

resultado = merge_vlr_prima[['PERIODO', 'NIT', 'RAZON_SOCIAL_AFP', 'tipo_id_contraloria', 'numero_id_contraloria', 'AF_PRIMERNOMBRE',

                 'AF_SEGUNDONOMBRE', 'AF_PRIMERAPELLIDO', 'AF_SEGUNDOAPELLIDO', 'FECHA_DE_NACIMIENTO', 'GÉNERO',

                 'COD_MUNIC_NACIMIENTO', 'NOMBRE_MUNIC_NACIMIENTO', 'COD_DEPART_NACIMIENTO', 'NOMBRE_DEPART_NACIMIENTO',

                 'COD_MUNIC_RESIDENCIA', 'NOMBRE_MUNIC_RESIDENCIA', 'COD_DEPART_RESIDENCIA', 'NOMBRE_DEPART_RESIDENCIA',

                 'FECHA_AFILIACION', 'FECHA_DESVINCULACION', 'ESTADO_AFILIADO', 'COTIZANTE', 'SALARIO',

                 'Valor Prima seguro',

                 'TIPO_DE_NOVEDAD', 'SEMANAS_REGIMEN_PRIMA_MEDIA', 'SEMANAS_REGIMEN_AHORRO_INDIVIDUAL_CON_SOLIDARIDAD',

                 'TOTAL_SEMANAS_COTIZADAS', 'Aportes oblig. RAIS         ', 'Pesos hist. aportes vol. to',

                 'Rendimientos RAIS           ', 'Rendim. aportes vol. totale', 'Saldo total ahorrado       ',

                 'NOMBRE_FONDO(S)', 'VALOR_FONDO_MODERADO_prima', 'VALOR_FONDO_CONSERVADOR_prima', 'VALOR_FONDO_MAYOR_RIESGO_prima']]

 

print('Renombrando Informe')

nombres_originales_informe = resultado.columns.tolist()

nuevos_nombres_informe = ['PERIODO',    'NIT_AFP',  'RAZON_SOCIAL_AFP', 'TIPO_DOCUMENTO_AFILIADO',  'DOCUMENTO_AFILIADO',   'AF_PRIMERNOMBRE',  'AF_SEGUNDONOMBRE', 'AF_PRIMERAPELLIDO',    'AF_SEGUNDOAPELLIDO',   'FECHA_DE_NACIMIENTO',  'GÉNERO',   'COD_MUNIC_NACIMIENTO', 'NOMBRE_MUNIC_NACIMIENTO',  'COD_DEPART_NACIMIENTO',    'NOMBRE_DEPART_NACIMIENTO', 'COD_MUNIC_RESIDENCIA', 'NOMBRE_MUNIC_RESIDENCIA',  'COD_DEPART_RESIDENCIA',    'NOMBRE_DEPART_RESIDENCIA', 'FECHA_AFILIACION', 'FECHA_DESVINCULACION', 'ESTADO_AFILIADO',  'COTIZANTE',    'SALARIO_AFILIADO', 'VALOR_SEGUROS_PREVISIONALES',  'TIPO_DE_NOVEDAD',  'SEMANAS_COTIZADAS_REGIMEN_PRIMA_MEDIA',    'SEMANAS_COTIZADAS_REGIMEN_AHORRO_INDIVIDUAL_CON_SOLIDARIDAD',  'TOTAL_SEMANAS_COTIZADAS',  'APORTES_OBLIGATORIOS_ACUMULADOS',  'APORTES_VOLUNTARIOS_NETOS_ACUMULADOS', 'RENDIMIENTOS_AHORRO_INDIVIDUAL_OBLIGATORIO',   'RENDIMIENTOS_AHORRO_INDIVIDUAL_VOLUNTARIO',    'SALDO_TOTAL_AHORRADO', 'NOMBRE_FONDO(S)',  'VALOR_FONDO_MODERADO', 'VALOR_FONDO_CONSERVADOR',  'VALOR_FONDO_MAYOR_RIESGO',]

diccionario_nombres_informe = dict(zip(nombres_originales_informe, nuevos_nombres_informe))

resultado = resultado.rename(columns=diccionario_nombres_informe)



 

print('Guardando informe')

resultado.to_csv('Informe contraloria ' + fecha_generacion+ '.csv', sep=';', encoding='ISO-8859-1', index=False)

print('Informe generado')

#merge_vlr_prima.head()






 

#df_rendimientos.groupby('Código de fondo').count()

