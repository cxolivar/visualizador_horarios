# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 10:54:58 2024

@author: camilo.olivares
"""

import pandas as pd
import numpy as np



def bloques(prueba_inicio,prueba_fin):  # SEGUN EL HORARIO DE INICIO A FIN LE ASIGNA SU EQUIVALENCIA EN EL CORRESPONDIENTE BLOQUE
    bloque_inicio=[]
    bloque_fin=[]
    
    for i in range(len(bloques_horarios)):       
        if bloques_horarios["hora_inicio"][i]<=prueba_inicio and bloques_horarios["hora_fin"][i]>=prueba_inicio:
            bloque_inicio.append(bloques_horarios["Bloque"][i])

    for i in range(len(bloques_horarios)):       
        if bloques_horarios["hora_inicio"][i]<=prueba_fin and bloques_horarios["hora_fin"][i]>=prueba_fin:
            bloque_fin.append(bloques_horarios["Bloque"][i])


    listado_bloques=[]
    k=bloque_inicio[0]
    while k<=bloque_fin[0]:
        
        listado_bloques.append(k)
        k=k+1

    return listado_bloques


def armado_columna_bloques(plani):  # AGREGA AL DATA FRAME UNA COLUMNA CORRESPONDIENTE A LA ASIGNACION DE BLOQUES

    columna_bloques=[]
    for i in range(len(plani)):
        
        
    
        try:
            columna_bloques.append(bloques(plani["HORA_INCIO"][i],plani["HORA_FIN"][i]))
    
        except:       
            columna_bloques.append([-1])
    
    plani_modificada=plani 
    plani_modificada["BLOQUES_HORARIOS"]=columna_bloques        
    
    return plani_modificada
        

def horario_sala(nueva_plani): # SUMA, ELIMINA DUPLICADOS DE BLOQUES, ACA SE DEBE PONER 
    suma=[]
    for i in range(len(nueva_plani["BLOQUES_HORARIOS"])):
        suma=suma+nueva_plani["BLOQUES_HORARIOS"][i]
      
       
    suma.sort()
    sumadf=pd.DataFrame({"lista":suma})
    sumadf=sumadf.drop_duplicates()
    serie=sumadf["lista"]
    lista=serie.tolist()
    #lista.remove(-1)
    return lista
    

def ocupacion_salon(edificio,salon,nueva_plani,dia): # entrega el horario ocupado en un dia especifico
    
    filtro=nueva_plani[nueva_plani["EDIFICIO"]==edificio]
    filtro=filtro[filtro["COD_SALON"]==salon]
    
    lunes=filtro[filtro[dia.upper()]=="Y"].reset_index(drop=True)
    
    th=lunes["TIPO_HORARIO"]


    # return horario_sala(lunes),len(horario_sala(lunes))/bloques_vespertinos
    return horario_sala(lunes),th


bloques_horarios=pd.read_excel("bloques_horarios.xlsx")


plani=pd.read_excel("plani-7-marzo.xlsx")



inicio=plani["HORA_INCIO"][195]
fin=plani["HORA_FIN"][195]
bbb=bloques(inicio,fin)



todo_banner=pd.DataFrame()


plani=pd.read_excel("plani-7-marzo.xlsx")
bloques_horarios=pd.read_excel("bloques_horarios.xlsx")
dias_semana=["lunes","martes","miercoles","jueves","viernes"]
bloques_vespertinos=5


# SALAS DE LA PLANIFICACION
salas=plani[["SEDE","EDIFICIO","COD_SALON","SALON"]].drop_duplicates().dropna() 
salas=salas[salas["SALON"]!="SALA VIRTUAL"] # ELIMINO LAS SALAS VIRTUALES
salas=salas.reset_index(drop=True) # RESETEO DE INDEX

#total de salas por campus
salas_providencia=len(salas[salas["SEDE"]=="PR"])
salas_san_miguel=len(salas[salas["SEDE"]=="SM"])
salas_talca=len(salas[salas["SEDE"]=="TA"])
salas_temuco=len(salas[salas["SEDE"]=="TE"])


# total de bloques por campus, considerando 5 dias a la semana
total_bloques_providencia_diurno=salas_providencia*bloques_vespertinos*5
total_bloques_san_miguel_diurno=salas_san_miguel*bloques_vespertinos*5
total_bloques_talca_diurno=salas_talca*bloques_vespertinos*5
total_bloques_temuco_diurno=salas_temuco*bloques_vespertinos*5


total_nrc_PR=len(plani[plani["SEDE"]=="PR"]["NRC"].drop_duplicates())
total_nrc_SM=len(plani[plani["SEDE"]=="SM"]["NRC"].drop_duplicates())
total_nrc_TA=len(plani[plani["SEDE"]=="TA"]["NRC"].drop_duplicates())
total_nrc_TE=len(plani[plani["SEDE"]=="TE"]["NRC"].drop_duplicates())

#HOARIOS


###########PRIMERA METODO QUE SE DEBE UTILIZAR, AGREGAR LA COLUMNA BLOQUES A LA PLAN#################
nueva_plani=armado_columna_bloques(plani)
nueva_plani=nueva_plani[["PROGRAMA","NRC","MATERIA","CURSO","SEDE","LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","HORA_INCIO","HORA_FIN","BLOQUES_HORARIOS","EDIFICIO","COD_SALON","TIPO_HORARIO","FECHA_INCIO","FECHA_FIN"]]
nueva_plani=nueva_plani.dropna(subset=['FECHA_INCIO'])
nueva_plani=nueva_plani.dropna(subset=['FECHA_FIN'])
#####################################################################################################
i=1
dia="lunes"

##### Acá se procesan todas las salas###########333
periodo=202420
todas_las_salas=pd.DataFrame()
aux=pd.DataFrame()
todo_banner=pd.DataFrame()
for i in range(len(salas["EDIFICIO"])):
    
    sede=salas["SEDE"][i]
    edificio=salas["EDIFICIO"][i]
    salon=salas["COD_SALON"][i]
    tipo=salas["SALON"][i]

    for dia in dias_semana:
        
        bloques,porcentaje_ocupacion=ocupacion_salon(edificio, salon, nueva_plani,dia)
        
        aux=pd.DataFrame({"Periodo":periodo,"Sede":[sede],"Edificio":[edificio],"Sala":[salon],"Tipo Sala":[tipo],"Dia":[dia],"% ocupacion":[porcentaje_ocupacion],"total bloques":[len(bloques)]})
        todas_las_salas=pd.concat([todas_las_salas,aux])
    


todo_banner=pd.concat([todo_banner,todas_las_salas])


todo_banner.to_excel("ocupacion_salas_202531_23_enero_2.xlsx")



todo_union=pd.DataFrame()
for dia in dias_semana:


    
    
    for i in range(len(salas)):
        sede=salas["SEDE"][i]
        edificio=salas["EDIFICIO"][i]
        salon=salas["COD_SALON"][i]
        tipo=salas["SALON"][i]
        
        
        plani_mod,tipo_H=ocupacion_salon(edificio,salon,nueva_plani,dia)
        
        if len(plani_mod)==len(tipo_H):
            union=pd.DataFrame({"BLOQUES":plani_mod,"TIPO_HORARIO":tipo_H})
            union["SEDE"]=sede
            union["EDIFICIO"]=edificio
            union["SALON"]=salon
            union["DIA"]=dia
            union["TIPO_SALON"]=tipo
            
        else:
            valor_a_llenar=tipo_H[0]
            tipo_H = tipo_H.to_list()  + [valor_a_llenar] * (len(plani_mod) - len(tipo_H ))
            union=pd.DataFrame({"BLOQUES":plani_mod,"TIPO_HORARIO":tipo_H})
            union["SEDE"]=sede
            union["EDIFICIO"]=edificio
            union["SALON"]=salon
            union["DIA"]=dia
            union["TIPO_SALON"]=tipo
            
            
        
        todo_union=pd.concat([todo_union,union])
        

todo_union.to_excel("primer_modelo3.xlsx")








### calcula el total de bloques utilizados
suma_PR_D=sum(todas_las_salas[todas_las_salas["Sede"]=="PR"]["total bloques"])
suma_SM_D=sum(todas_las_salas[todas_las_salas["Sede"]=="SM"]["total bloques"])
suma_TA_D=sum(todas_las_salas[todas_las_salas["Sede"]=="TA"]["total bloques"])
suma_TE_D=sum(todas_las_salas[todas_las_salas["Sede"]=="TE"]["total bloques"])

### obtiene el % de ocupacion por sede
ocupacion_PR_D=suma_PR_D/total_bloques_providencia_diurno
ocupacion_SM_D=suma_PR_D/total_bloques_san_miguel_diurno
ocupacion_TA_D=suma_PR_D/total_bloques_talca_diurno
ocupacion_TE_D=suma_PR_D/total_bloques_temuco_diurno





todos_porcentajes=[ocupacion_PR_D,ocupacion_SM_D,ocupacion_TA_D,ocupacion_TE_D]
sedes=["Providencia","San Miguel","Talca","Temuco"]
todos_los_NRC=[total_nrc_PR,total_nrc_SM,total_nrc_TA,total_nrc_TE]
periodos=[periodo,periodo,periodo,periodo]

acumulados=pd.DataFrame({"Periodo":periodos,"Sede":sedes,"% ocupacion":todos_porcentajes,"Total NRCs":todos_los_NRC})







acumulados.to_excel(f"Ocupacion_{periodo}.xlsx")















#def ventanas(edificio,salon,nueva_plani,dia): # entrega el horario ocupado en un dia especifico
total=nueva_plani["NRC"].drop_duplicates()
todas_los_nrc=pd.DataFrame()


for n in total:

#nrc_prueba=nueva_plani["NRC"][406]
    plani_prueba=nueva_plani[nueva_plani["NRC"]==n].reset_index()
    aaaa=horario_sala(plani_prueba)
    aux=pd.DataFrame({"NRC":[n],"bloques":[aaaa]})
    todas_los_nrc=pd.concat([todas_los_nrc,aux])

todas_los_nrc.to_excel("a_lo_crack.xlsx")

