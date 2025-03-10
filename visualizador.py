import pandas as pd
import numpy as np
import streamlit as st



# lectura y union de archivos

bloques_horarios=pd.read_excel("bloques_horarios.xlsx")


#################FUNCION PARA DEFINIR BLOQUES########################################


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






###############################################################################################
@st.cache_data
def lectura():

    # lectura y union de archivos
    plani_202510=pd.read_excel("plani_202510.xlsx")
    plani_202531=pd.read_excel("plani_202531.xlsx")
    plani_union=pd.concat([plani_202510,plani_202531],axis=0).reset_index()
    
    
    
    a=plani_union[plani_union["NRC"]==10212]
    aa=armado_columna_bloques(a)
    
    # se agregan los bloques de horarios
    nueva_plani=armado_columna_bloques(plani_union)
    # datos utiles
    
    plani=nueva_plani[["CODIGO_PERIODO","PROGRAMA","NIVEL","NRC","MATERIA","CURSO","TITULO","SEDE","TIPO_HORARIO","INSCRITOS","LUNES","MARTES","MIERCOLES","JUEVES","VIERNES","BLOQUES_HORARIOS"]]

    return plani



# plani.to_excel("plani_base.xlsx")


# plani=pd.read_excel("plani_base.xlsx")

# cursos=plani_filtros[["NRC","MATERIA","CURSO","TITULO"]].drop_duplicates()
# cursos["NRC"]=cursos["NRC"].astype(str)
# cursos["CURSO"]=cursos["CURSO"].astype(str)
# cursos["llave"]=cursos["NRC"]+"-"+cursos["MATERIA"]+"_"+cursos["CURSO"]+"-"+cursos["TITULO"]

periodo=202510
sede="TA"
nrc=10036

def calendario_fun(per,se,n,plani):
    
    
    periodo=per
    sede=se
    nrc=n
    
    plani_filtros=plani[plani["CODIGO_PERIODO"]==periodo]
    plani_filtros=plani_filtros[plani_filtros["SEDE"]==sede]        
    horario=plani_filtros[plani_filtros["NRC"]==int(nrc)]
    
    
    
    
    lunes=horario[horario["LUNES"]=="Y"].reset_index()
    martes=horario[horario["MARTES"]=="Y"].reset_index()
    miercoles=horario[horario["MIERCOLES"]=="Y"].reset_index()
    jueves=horario[horario["JUEVES"]=="Y"].reset_index()
    viernes=horario[horario["VIERNES"]=="Y"].reset_index()
    
    
    if len(lunes)==0:
        lunes_bloq=[0]
    
    else:
        lunes_bloq=horario_sala(lunes)
    
    
    if len(martes)==0:
        martes_bloq=[0]
    
    else:
        martes_bloq=horario_sala(martes)
    
    
    if len(miercoles)==0:
        miercoles_bloq=[0]
    
    else:
        miercoles_bloq=horario_sala(miercoles)
        
    if len(jueves)==0:
        jueves_bloq=[0]
    
    else:
        jueves_bloq=horario_sala(jueves)
        
    if len(viernes)==0:
        viernes_bloq=[0]
    
    else:
        viernes_bloq=horario_sala(viernes)
    
    
    calendario=pd.DataFrame()
    calendario["Bloques"]=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    calendario["LUNES"]=["","","","","","","","","","","","","","","","","","","","",""]
    calendario["MARTES"]=["","","","","","","","","","","","","","","","","","","","",""]
    calendario["MIERCOLES"]=["","","","","","","","","","","","","","","","","","","","",""]
    calendario["JUEVES"]=["","","","","","","","","","","","","","","","","","","","",""]
    calendario["VIERNES"]=["","","","","","","","","","","","","","","","","","","","",""]
    

 
    
    if not 0 in lunes_bloq:
        for b in lunes_bloq:
            calendario.loc[b-1, "LUNES"] = "CLASES" 
            
    if not 0 in martes_bloq:
        for b in martes_bloq:
            calendario.loc[b-1, "MARTES"] = "CLASES"        
    
    if not 0 in miercoles_bloq:
        for b in miercoles_bloq:
            calendario.loc[b-1, "MIERCOLES"] = "CLASES"
    
    if not 0 in jueves_bloq:
        for b in jueves_bloq:
            calendario.loc[b-1, "JUEVES"] = "CLASES"
    
    
    if not 0 in viernes_bloq:
        for b in viernes_bloq:
            calendario.loc[b-1, "VIERNES"] = "CLASES"
            
            
            
    return calendario


    
# aaaa=calendario_fun(202510, "TA", 10009,plani)













# Ejemplo de uso en 

plani=lectura()
def main():
    
    st.title("Visualizador de Horarios UAutonoma") 
    
    
    periodos=plani["CODIGO_PERIODO"].drop_duplicates()
    periodo=st.selectbox("Eliga el periodo",periodos)    
    plani_filtros=plani[plani["CODIGO_PERIODO"]==periodo]
    
    
    
    sedes=plani_filtros["SEDE"].drop_duplicates()
    sede=st.selectbox("Eliga la sede",sedes)
    plani_filtros=plani_filtros[plani_filtros["SEDE"]==sede]
    
    cursos=plani_filtros[["NRC","MATERIA","CURSO","TITULO"]].drop_duplicates()
    cursos["NRC"]=cursos["NRC"].astype(str)
    cursos["CURSO"]=cursos["CURSO"].astype(str)
    
    cursos["llave"]=cursos["NRC"]+"--"+cursos["TITULO"]+"  ("+(cursos["MATERIA"]+cursos["CURSO"])+")"

    selector_curso=st.selectbox("Eliga el curso",cursos["llave"])

    nrc=selector_curso[:5]
    
    
    st.write(nrc)
    
    cal=calendario_fun(periodo,sede,nrc,plani)
    st.dataframe(cal,hide_index=True,height=770)
    

if __name__ == '__main__':
    main()

        
        
        










