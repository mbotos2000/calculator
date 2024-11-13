from __future__ import print_function
#from mailmerge import MailMerge
from datetime import date
import streamlit as st
from channelflowlib.openchannellib import Trapezoidal, Circular, IrregularSection
import ezdxf  
from pandas import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import math
import time


def auto_cad(d):
    doc = ezdxf.new('R2000',setup=True)
    msp = doc.modelspace()

    doc.layers.new(name='Linie_teren', dxfattribs={'linetype': 'Continuous', 'color': 2})
    doc.layers.new(name='ajutatoare', dxfattribs={'linetype': 'DASHED', 'color': 4})
    doc.layers.new(name='tabel', dxfattribs={'linetype': 'Continuous', 'color': 7})
    doc.layers.new(name='text', dxfattribs={'color': 3})

    
    records = d.to_records(index=False)
    dz=1
    dx=6
    msp.add_lwpolyline(records,dxfattribs={'layer': 'Linie_teren'})
    i=0
    for index, row in d.iterrows():
        i=i+1
        points = [(row['dc'], row['z']), (row['dc'], int(d['z'].min()-2))]
        msp.add_lwpolyline(points,dxfattribs={'layer': 'ajutatoare'})
        msp.add_text(str(i),
                 dxfattribs={'layer': 'text',
                     'style': 'LiberationSerif',
                     'height': 0.35,
                      'width':0.5}
                 ).set_pos((row['dc'], int(d['z'].min()-2)-dz/2), align='MIDDLE_CENTER')
        msp.add_text(str(row['dc']),
                 dxfattribs={'layer': 'text',
                     'style': 'LiberationSerif',
                     'height': 0.35,
                      'width':0.5}
                 ).set_pos((row['dc'], int(d['z'].min()-2-dz)-dz/2), align='MIDDLE_CENTER')
        msp.add_text(str(row['z']),
                 dxfattribs={'layer': 'text',
                     'style': 'LiberationSerif',
                     'height': 0.35,
                      'width':0.5}
                 ).set_pos((row['dc'], int(d['z'].min()-2-2*dz)-dz/2), align='MIDDLE_CENTER')
    n=int(d['z'].max()+1)-int(d['z'].min()-2)
    poz=int(d['dc'].min()-1)-0.5
    msp.add_lwpolyline([(int(d['dc'].min()-1), int(d['z'].min())-2),(int(d['dc'].min()-1), int(d['z'].min())-2+n)],dxfattribs={'layer': 'tabel'})
    for j in range(n):
        if not(j==0):
            msp.add_text(int(d['z'].min())-2+j,
                     dxfattribs={'layer': 'text',
                         'style': 'LiberationSerif',
                         'height': 0.35,
                          'width':0.7}
                     ).set_pos((poz, int(d['z'].min())-2+j), align='MIDDLE_RIGHT')
            msp.add_lwpolyline([(poz+0.3, int(d['z'].min())-2+j),(poz+0.5, int(d['z'].min())-2+j)],dxfattribs={'layer': 'tabel'})

    lista=['Nr. punct', 'Distanta cumulata', 'Cota teren','','','','']
    for i in range(5):
        msp.add_text(lista[i],
                 dxfattribs={'layer': 'text',
                     'style': 'LiberationSerif',
                     'height': 0.35,
                      'width':0.7}
                 ).set_pos(((int(d['dc'].min()-1-dx/2), int(d['z'].min()-2-i*dz)-dz/2)), align='MIDDLE_CENTER')
        msp.add_lwpolyline([(int(d['dc'].min()-dx), int(d['z'].min()-2)-i*dz),(int(d['dc'].min()-1), int(d['z'].min()-2)-i*dz)],dxfattribs={'layer': 'tabel'})
        msp.add_lwpolyline([(int(d['dc'].min()-1), int(d['z'].min()-2)-i*dz), (int(d['dc'].max()+1), int(d['z'].min()-2)-i*dz)],dxfattribs={'layer': 'tabel'})
    msp.add_lwpolyline([(int(d['dc'].min()-1), int(d['z'].min()-2)), (int(d['dc'].min()-1), int(d['z'].min()-2)-i*dz)],dxfattribs={'layer': 'tabel'})
    msp.add_lwpolyline([(int(d['dc'].max()+1), int(d['z'].min()-2)), (int(d['dc'].max()+1), int(d['z'].min()-2)-i*dz)],dxfattribs={'layer': 'tabel'})
    msp.add_lwpolyline([(int(d['dc'].min()-dx), int(d['z'].min()-2)),(int(d['dc'].min()-dx), int(d['z'].min()-2)-i*dz)],dxfattribs={'layer': 'tabel'})

    doc.saveas("d:/1/lwpolyline1.dxf")     

def graf(ad,pt,b,garda):
  xpoints = np.array([0,1,1+pt*garda,1+pt*garda+ad*pt,1+pt*garda+ad*pt+b,1+pt*garda+2*ad*pt+b,1+2*pt*garda+2*ad*pt+b,2+2*pt*garda+2*ad*pt+b])
  ypoints = np.array([ad+garda,ad+garda,ad,0,0,ad,ad+garda,ad+garda])
  fig, ax = plt.subplots()
  ax.plot(xpoints,ypoints)
  ax.plot([1+pt*garda,1+pt*garda+2*ad*pt+b],[ad,ad])
  ax.set_title("Linia terenului")
  return fig
  
def graf_c(r,h):
  circ=plt.Circle((r, r), r,fill = False)
  fig, ax = plt.subplots()
  ax.add_patch( circ )
  ax.plot([(2*r-math.sqrt(4*r*r-4*(h-r)*(h-r)))/2,(2*r+math.sqrt(4*r*r-4*(h-r)*(h-r)))/2],[h,h])
  #ax.plot([1+pt*garda,1+pt*garda+2*ad*pt+b],[ad,ad])
  ax.set_title("Linia terenului")
  return fig   


st.title("Calcul hidraulic")
st.write('{:%d-%b-%Y}'.format(date.today()))
add_selectbox_Tip_sectiune_reg = st.sidebar.selectbox(
    'Tipul sectiunii',
    ('','Regulata', 'Neregulata')
    )
if add_selectbox_Tip_sectiune_reg=='Regulata':
    add_selectbox_Tip_calcul = st.sidebar.selectbox(
        'Tip calcul',
        ('','Capacitate de transport Q=?', 'Nivel de calcul h=?', 'Latimea la baza b=?','Panta hidraulica i=?','Panta hidraulica pentru miscarea neuniforma i=?'),
        help='Q ,h, i sunt obtinute pentru miscarea uniforma')

    add_selectbox_Tip_sectiune = st.sidebar.selectbox(
        'Tipul sectiunii regulate',
        ('','Trapezoidala', 'Dreptunghiulara', 'Triunghiulara','Circulara')
        )



    if add_selectbox_Tip_calcul=='Capacitate de transport Q=?' and add_selectbox_Tip_sectiune=='Trapezoidala':
            st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
            Panta_t=st.sidebar.number_input(
                'Panta canalului',
                min_value=0.0, max_value=0.10,step=0.001,format='%f',
                help='Introduceti panta canalului in  [m/m]')
            Rugozitatea=st.sidebar.number_input(
                'Introduceti rugozitatea ponderata',
                min_value=0.000, max_value=0.200,step =0.005,format='%f',
                help=' ')
            Latime=st.sidebar.number_input(
                'Introduceti latimea la baza asectiunii',
                min_value=0.0, max_value=300.0,step =0.01,format='%f',
                help=' ')
            Panta_taluz=st.sidebar.number_input(
                'Introduceti coeficientul de panta a taluzului',
                min_value=0.0, max_value=10.0,step =0.01,format='%f',
                help='')
            adancime=st.sidebar.number_input(
                'Introduceti adancimea normala',
                min_value=0.0, max_value=50.0,step =0.01,format='%f',
                help='')
            a=st.sidebar.button('Hit me')
            if a:
                st.title(add_selectbox_Tip_calcul)
                st.title(add_selectbox_Tip_sectiune)
                # Initialize Trapezoidal Channel instance
                trap = Trapezoidal(unknown='discharge')

                # Set the inputs
                trap.set_channel_slope(Panta_t)
                trap.set_sideslope(Panta_taluz)
                trap.set_channel_base(Latime)
                trap.set_roughness(Rugozitatea)
                trap.set_water_depth(adancime)

                # Analyze
                trap.analyze()

                # Show the outputs
                st.write('Debitul : ', round(trap.discharge, 2),' [mc/s]')
                st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                st.pyplot(graf(adancime,Panta_taluz,Latime,1.0))
    if add_selectbox_Tip_calcul=='Capacitate de transport Q=?' and  add_selectbox_Tip_sectiune=='Dreptunghiulara':
            st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
            Panta_t=st.sidebar.number_input(
                'Panta canalului',
                min_value=0.0, max_value=0.10,step=0.001,format='%f',
                help='Introduceti panta canalului in  [m/m]')
            Rugozitatea=st.sidebar.number_input(
                'Introduceti rugozitatea ponderata',
                min_value=0.000, max_value=0.200,step =0.005,format='%f',
                help=' ')
            Latime=st.sidebar.number_input(
                'Introduceti latimea la baza asectiunii',
                min_value=0.0, max_value=300.0,step =0.01,format='%f',
                help=' ')
            Panta_taluz=0.0
            adancime=st.sidebar.number_input(
                'Introduceti adancimea normala',
                min_value=0.0, max_value=50.0,step =0.01,format='%f',
                help='')
            a=st.sidebar.button('Hit me')
            if a:
                st.title(add_selectbox_Tip_calcul)
                st.title(add_selectbox_Tip_sectiune)
                # Initialize Trapezoidal Channel instance
                trap = Trapezoidal(unknown='discharge')

                # Set the inputs
                trap.set_channel_slope(Panta_t)
                trap.set_sideslope(Panta_taluz)
                trap.set_channel_base(Latime)
                trap.set_roughness(Rugozitatea)
                trap.set_water_depth(adancime)

                # Analyze
                trap.analyze()

                # Show the outputs
                st.write('Debitul : ', round(trap.discharge, 2),' [mc/s]')
                st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                st.pyplot(graf(adancime,0,Latime,1.0))
    if add_selectbox_Tip_calcul=='Capacitate de transport Q=?' and  add_selectbox_Tip_sectiune=='Triunghiulara':
            st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
            Panta_t=st.sidebar.number_input(
                'Panta canalului',
                min_value=0.0, max_value=0.10,step=0.001,format='%f',
                help='Introduceti panta canalului in  [m/m]')
            Rugozitatea=st.sidebar.number_input(
                'Introduceti rugozitatea ponderata',
                min_value=0.000, max_value=0.200,step =0.005,format='%f',
                help=' ')
            Latime=0.0
            Panta_taluz=st.sidebar.number_input(
                'Introduceti coeficientul de panta a taluzului',
                min_value=0.0, max_value=10.0,step =0.01,format='%f',
                help='')
            adancime=st.sidebar.number_input(
                'Introduceti adancimea normala',
                min_value=0.0, max_value=50.0,step =0.01,format='%f',
                help='')
            a=st.sidebar.button('Hit me')
            if a:
                st.title(add_selectbox_Tip_calcul)
                st.title(add_selectbox_Tip_sectiune)
                # Initialize Trapezoidal Channel instance
                trap = Trapezoidal(unknown='discharge')

                # Set the inputs
                trap.set_channel_slope(Panta_t)
                trap.set_sideslope(Panta_taluz)
                trap.set_channel_base(Latime)
                trap.set_roughness(Rugozitatea)
                trap.set_water_depth(adancime)

                # Analyze
                trap.analyze()

                # Show the outputs
                st.write('Debitul : ', round(trap.discharge, 2),' [mc/s]')
                st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                st.pyplot(graf(adancime,Panta_taluz,0.0,1.0))
    if add_selectbox_Tip_calcul=='Capacitate de transport Q=?' and  add_selectbox_Tip_sectiune=='Circulara':
            st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
            Panta_t=st.sidebar.number_input(
                'Panta canalului',
                min_value=0.0, max_value=0.10,step=0.001,format='%f',
                help='Introduceti panta canalului in  [m/m]')
            Rugozitatea=st.sidebar.number_input(
                'Introduceti rugozitatea ponderata',
                min_value=0.000, max_value=0.200,step =0.005,format='%f',
                help=' ')
            
            Diametru=st.sidebar.number_input(
                'Introduceti diametrul',
                min_value=0.0, max_value=10.0,step =0.01,format='%f',
                help='')
            adancime=st.sidebar.number_input(
                'Introduceti adancimea normala',
                min_value=0.0, max_value=Diametru,step =0.01,format='%f',
                help='')
            a=st.sidebar.button('Hit me')
            if a:
                st.title(add_selectbox_Tip_calcul)
                st.title(add_selectbox_Tip_sectiune)
                # Initialize Trapezoidal Channel instance
                circ = Circular()

                # Set the inputs
                circ.set_slope(Panta_t)
                circ.set_diameter(Diametru)
                
                circ.set_roughness(Rugozitatea)
                circ.set_water_depth(adancime)

                # Analyze
                circ.calculate_discharge()

                # Show the outputs
                st.write('Debitul : ', round(circ.discharge, 4),' [mc/s]')
                st.write('Aria vie  : ', round(circ.wetted_area, 3),' [mp]')
                st.write('Perimetrul udat: ', round(circ.wetted_perimeter, 3),' [m]')
                st.write('Raza hidraulica: ', round(circ.hydraulic_radius, 4),' [m]')
                st.write('Gradul de umplere: ', round(adancime/2*circ.hydraulic_radius, 4))
                st.write('Viteza medie: ', round(circ.velocity, 3),' [m/s]')
                st.pyplot(graf_c(Diametru/2,adancime))
    if add_selectbox_Tip_calcul=='Nivel de calcul h=?'and add_selectbox_Tip_sectiune=='Trapezoidala':
                st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
                Panta_t=st.sidebar.number_input(
                    'Panta canalului',
                    min_value=0.0, max_value=0.10,step=0.001,format='%f',
                    help='Introduceti panta canalului in  [m/m]')
                Rugozitatea=st.sidebar.number_input(
                    'Introduceti rugozitatea ponderata',
                    min_value=0.000, max_value=0.200,step =0.005,format='%f',
                    help=' ')
                Latime=st.sidebar.number_input(
                    'Introduceti latimea la baza asectiunii',
                    min_value=0.0, max_value=300.0,step =0.01,format='%f',
                    help=' ')
                Panta_taluz=st.sidebar.number_input(
                    'Introduceti coeficientul de panta a taluzului',
                    min_value=0.0, max_value=10.0,step =0.01,format='%f',
                    help='')
                debit=st.sidebar.number_input(
                    'Introduceti debitul',
                    min_value=0.0, max_value=1000.0,step =0.01,format='%f',
                    help='')
                a=st.sidebar.button('Hit me')
                if a:
                    st.title(add_selectbox_Tip_calcul)
                    st.title(add_selectbox_Tip_sectiune)
                    # Initialize Trapezoidal Channel instance
                    trap = Trapezoidal(unknown='water_depth')

                    # Set the inputs
                    trap.set_channel_slope(Panta_t)
                    trap.set_sideslope(Panta_taluz)
                    trap.set_channel_base(Latime)
                    trap.set_roughness(Rugozitatea)
                    trap.set_discharge(debit)

                    # Analyze
                    trap.analyze()

                    # Show the outputs
                    st.write('Adancimea normala : ', round(trap.water_depth, 2),' [m]')
                    st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                    st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                    st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                    st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                    st.pyplot(graf(trap.water_depth,Panta_taluz,Latime,1.0))
    if add_selectbox_Tip_calcul=='Nivel de calcul h=?'and add_selectbox_Tip_sectiune=='Dreptunghiulara':
                st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
                Panta_t=st.sidebar.number_input(
                    'Panta canalului',
                    min_value=0.0, max_value=0.10,step=0.001,format='%f',
                    help='Introduceti panta canalului in  [m/m]')
                Rugozitatea=st.sidebar.number_input(
                    'Introduceti rugozitatea ponderata',
                    min_value=0.000, max_value=0.200,step =0.005,format='%f',
                    help=' ')
                Latime=st.sidebar.number_input(
                    'Introduceti latimea la baza asectiunii',
                    min_value=0.0, max_value=300.0,step =0.01,format='%f',
                    help=' ')
                Panta_taluz=0.0
                debit=st.sidebar.number_input(
                    'Introduceti debitul',
                    min_value=0.0, max_value=1000.0,step =0.01,format='%f',
                    help='')
                a=st.sidebar.button('Hit me')
                if a:
                    st.title(add_selectbox_Tip_calcul)
                    st.title(add_selectbox_Tip_sectiune)
                    # Initialize Trapezoidal Channel instance
                    trap = Trapezoidal(unknown='water_depth')

                    # Set the inputs
                    trap.set_channel_slope(Panta_t)
                    trap.set_sideslope(Panta_taluz)
                    trap.set_channel_base(Latime)
                    trap.set_roughness(Rugozitatea)
                    trap.set_discharge(debit)

                    # Analyze
                    trap.analyze()

                    # Show the outputs
                    st.write('Adancimea normala : ', round(trap.water_depth, 2),' [m]')
                    st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                    st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                    st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                    st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                    st.pyplot(graf(trap.water_depth,0,Latime,1.0))
    if add_selectbox_Tip_calcul=='Nivel de calcul h=?'and add_selectbox_Tip_sectiune=='Triunghiulara':
                st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
                Panta_t=st.sidebar.number_input(
                    'Panta canalului',
                    min_value=0.0, max_value=0.10,step=0.001,format='%f',
                    help='Introduceti panta canalului in  [m/m]')
                Rugozitatea=st.sidebar.number_input(
                    'Introduceti rugozitatea ponderata',
                    min_value=0.000, max_value=0.200,step =0.005,format='%f',
                    help=' ')
                Latime=0.0
                Panta_taluz=st.sidebar.number_input(
                    'Introduceti coeficientul de panta a taluzului',
                    min_value=0.0, max_value=10.0,step =0.01,format='%f',
                    help='')
                debit=st.sidebar.number_input(
                    'Introduceti debitul',
                    min_value=0.0, max_value=1000.0,step =0.01,format='%f',
                    help='')
                a=st.sidebar.button('Hit me')
                if a:
                    st.title(add_selectbox_Tip_calcul)
                    st.title(add_selectbox_Tip_sectiune)
                    # Initialize Trapezoidal Channel instance
                    trap = Trapezoidal(unknown='water_depth')

                    # Set the inputs
                    trap.set_channel_slope(Panta_t)
                    trap.set_sideslope(Panta_taluz)
                    trap.set_channel_base(Latime)
                    trap.set_roughness(Rugozitatea)
                    trap.set_discharge(debit)

                    # Analyze
                    trap.analyze()

                    # Show the outputs
                    st.write('Adancimea normala : ', round(trap.water_depth, 2),' [m]')
                    st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                    st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                    st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                    st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                    st.pyplot(graf(trap.water_depth,Panta_taluz,0.0,1.0))
    if add_selectbox_Tip_calcul=='Nivel de calcul h=?'and add_selectbox_Tip_sectiune=='Circulara':
                st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
                Panta_t=st.sidebar.number_input(
                    'Panta canalului',
                    min_value=0.0, max_value=0.10,step=0.001,format='%f',
                    help='Introduceti panta canalului in  [m/m]')
                Rugozitatea=st.sidebar.number_input(
                    'Introduceti rugozitatea ponderata',
                    min_value=0.000, max_value=0.200,step =0.005,format='%f',
                    help=' ')
                
                Diametru=st.sidebar.number_input(
                    'Introduceti diametrul',
                    min_value=0.0, max_value=10.0,step =0.01,format='%f',
                    help='')
                adancime=st.sidebar.number_input(
                    'Introduceti adancimea normala',
                    min_value=0.0, max_value=Diametru,step =0.01,format='%f',
                    help='')
                a=st.sidebar.button('Hit me')
                if a:
                    st.title(add_selectbox_Tip_calcul)
                    st.title(add_selectbox_Tip_sectiune)
                    # Initialize Trapezoidal Channel instance
                    circ = Circular()

                    # Set the inputs
                    circ.set_slope(Panta_t)
                    circ.set_diameter(Diametru)
                    
                    circ.set_roughness(Rugozitatea)
                    circ.set_water_depth(adancime)

                    # Analyze
                    circ.calculate_discharge()

                    # Show the outputs
                    st.write('Debitul : ', round(circ.discharge, 4),' [mc/s]')
                    st.write('Aria vie  : ', round(circ.wetted_area, 3),' [mp]')
                    st.write('Perimetrul udat: ', round(circ.wetted_perimeter, 3),' [m]')
                    st.write('Raza hidraulica: ', round(circ.hydraulic_radius, 4),' [m]')
                    st.write('Gradul de umplere: ', round(adancime/2*circ.hydraulic_radius, 4))
                    st.write('Viteza medie: ', round(circ.velocity, 3),' [m/s]')
                    st.pyplot(graf_c(Diametru/2,adancime))
        #text_4_1=st.sidebar.text_area('4.1 Preconditii din curriculul',value='')
    if add_selectbox_Tip_calcul=='Latimea la baza b=?'and add_selectbox_Tip_sectiune=='Trapezoidala':
                st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
                Panta_t=st.sidebar.number_input(
                    'Panta canalului',
                    min_value=0.0, max_value=0.10,step=0.001,format='%f',
                    help='Introduceti panta canalului in  [m/m]')
                Rugozitatea=st.sidebar.number_input(
                    'Introduceti rugozitatea ponderata',
                    min_value=0.000, max_value=0.200,step =0.005,format='%f',
                    help=' ')
                Adancime=st.sidebar.number_input(
                    'Introduceti adancimea normala a curentului',
                    min_value=0.0, max_value=300.0,step =0.01,format='%f',
                    help=' ')
                Panta_taluz=st.sidebar.number_input(
                    'Introduceti coeficientul de panta a taluzului',
                    min_value=0.0, max_value=10.0,step =0.01,format='%f',
                    help='')
                debit=st.sidebar.number_input(
                    'Introduceti debitul',
                    min_value=0.0, max_value=1000.0,step =0.01,format='%f',
                    help='')
                a=st.sidebar.button('Hit me')
                if a:
                    st.title(add_selectbox_Tip_calcul)
                    st.title(add_selectbox_Tip_sectiune)
                    # Initialize Trapezoidal Channel instance
                    trap = Trapezoidal(unknown='channel_base')

                    # Set the inputs
                    trap.set_channel_slope(Panta_t)
                    trap.set_sideslope(Panta_taluz)
                    trap.set_water_depth(Adancime)
                    trap.set_roughness(Rugozitatea)
                    trap.set_discharge(debit)

                    # Analyze
                    trap.analyze()

                    # Show the outputs
                    st.write('Latimea la baza : ', round(trap.channel_base, 2),' [m]')
                    st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                    st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                    st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                    st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                    st.pyplot(graf(Adancime,Panta_taluz,trap.channel_base,1.0))
    if add_selectbox_Tip_calcul=='Latimea la baza b=?'and add_selectbox_Tip_sectiune=='Dreptunghiulara':
                st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
                Panta_t=st.sidebar.number_input(
                    'Panta canalului',
                    min_value=0.0, max_value=0.10,step=0.001,format='%f',
                    help='Introduceti panta canalului in  [m/m]')
                Rugozitatea=st.sidebar.number_input(
                    'Introduceti rugozitatea ponderata',
                    min_value=0.000, max_value=0.200,step =0.005,format='%f',
                    help=' ')
                Adancime=st.sidebar.number_input(
                    'Introduceti adancimea normala a curentului',
                    min_value=0.0, max_value=300.0,step =0.01,format='%f',
                    help=' ')
                
                Panta_taluz=0.0
                debit=st.sidebar.number_input(
                    'Introduceti debitul',
                    min_value=0.0, max_value=1000.0,step =0.01,format='%f',
                    help='')
                a=st.sidebar.button('Hit me')
                if a:
                    st.title(add_selectbox_Tip_calcul)
                    st.title(add_selectbox_Tip_sectiune)
                    # Initialize Trapezoidal Channel instance
                    trap = Trapezoidal(unknown='channel_base')

                    # Set the inputs
                    trap.set_channel_slope(Panta_t)
                    trap.set_sideslope(Panta_taluz)
                    trap.set_water_depth(Adancime)
                    trap.set_roughness(Rugozitatea)
                    trap.set_discharge(debit)

                    # Analyze
                    trap.analyze()

                    # Show the outputs
                    st.write('Latimea la baza : ', round(trap.channel_base, 2),' [m]')
                    st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                    st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                    st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                    st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                    st.pyplot(graf(Adancime,0.0,trap.channel_base,1.0))
    if add_selectbox_Tip_calcul=='Latimea la baza b=?'and add_selectbox_Tip_sectiune=='Triunghiulara':
        st.write('???????????????')
    if add_selectbox_Tip_calcul=='Latimea la baza b=?'and add_selectbox_Tip_sectiune=='Circulara':
        st.write('???????????????')
    if add_selectbox_Tip_calcul=='Panta hidraulica i=?' and add_selectbox_Tip_sectiune=='Trapezoidala':
            st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
            debit=st.sidebar.number_input(
                'Introduceti debitul de transportat',
                min_value=0.0, max_value=1000.0,step=0.5,format='%f',
                help='Debitul   [mc/s]')
            Rugozitatea=st.sidebar.number_input(
                'Introduceti rugozitatea ponderata',
                min_value=0.000, max_value=0.200,step =0.005,format='%f',
                help=' ')
            Latime=st.sidebar.number_input(
                'Introduceti latimea la baza asectiunii',
                min_value=0.0, max_value=300.0,step =0.01,format='%f',
                help=' ')
            Panta_taluz=st.sidebar.number_input(
                'Introduceti coeficientul de panta a taluzului',
                min_value=0.0, max_value=10.0,step =0.01,format='%f',
                help='')
            adancime=st.sidebar.number_input(
                'Introduceti adancimea normala',
                min_value=0.0, max_value=50.0,step =0.01,format='%f',
                help='')
            a=st.sidebar.button('Hit me')
            if a:
                st.title(add_selectbox_Tip_calcul)
                st.title(add_selectbox_Tip_sectiune)
                # Initialize Trapezoidal Channel instance
                trap = Trapezoidal(unknown='channel_slope')

                # Set the inputs
                trap.set_discharge(debit)
                trap.set_sideslope(Panta_taluz)
                trap.set_channel_base(Latime)
                trap.set_roughness(Rugozitatea)
                trap.set_water_depth(adancime)

                # Analyze
                trap.analyze()

                # Show the outputs
                st.write('Panta : ', round(trap.channel_slope*100, 2),' [%]')
                st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                st.pyplot(graf(adancime,Panta_taluz,Latime,1.0))
    if add_selectbox_Tip_calcul=='Panta hidraulica i=?' and  add_selectbox_Tip_sectiune=='Dreptunghiulara':
            st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
            debit=st.sidebar.number_input(
                'Introduceti debitul de transportat',
                min_value=0.0, max_value=1000.0,step=0.5,format='%f',
                help='Debitul   [mc/s]')
            Rugozitatea=st.sidebar.number_input(
                'Introduceti rugozitatea ponderata',
                min_value=0.000, max_value=0.200,step =0.005,format='%f',
                help=' ')
            Latime=st.sidebar.number_input(
                'Introduceti latimea la baza asectiunii',
                min_value=0.0, max_value=300.0,step =0.01,format='%f',
                help=' ')
            Panta_taluz=0.0
            adancime=st.sidebar.number_input(
                'Introduceti adancimea normala',
                min_value=0.0, max_value=50.0,step =0.01,format='%f',
                help='')
            a=st.sidebar.button('Hit me')
            if a:
                st.title(add_selectbox_Tip_calcul)
                st.title(add_selectbox_Tip_sectiune)
                # Initialize Trapezoidal Channel instance
                trap = Trapezoidal(unknown='channel_slope')

                # Set the inputs
                trap.set_discharge(debit)
                trap.set_sideslope(Panta_taluz)
                trap.set_channel_base(Latime)
                trap.set_roughness(Rugozitatea)
                trap.set_water_depth(adancime)

                # Analyze
                trap.analyze()

                # Show the outputs
                st.write('Panta : ', round(trap.channel_slope*100, 2),' [%]')
                st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                st.pyplot(graf(adancime,Panta_taluz,0,1.0))
    if add_selectbox_Tip_calcul=='Panta hidraulica i=?' and  add_selectbox_Tip_sectiune=='Triunghiulara':
            st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
            debit=st.sidebar.number_input(
                'Introduceti debitul de transportat',
                min_value=0.0, max_value=1000.0,step=0.5,format='%f',
                help='Debitul   [mc/s]')
            Rugozitatea=st.sidebar.number_input(
                'Introduceti rugozitatea ponderata',
                min_value=0.000, max_value=0.200,step =0.005,format='%f',
                help=' ')
            Latime=0.0
            Panta_taluz=st.sidebar.number_input(
                'Introduceti coeficientul de panta a taluzului',
                min_value=0.0, max_value=10.0,step =0.01,format='%f',
                help='')
            adancime=st.sidebar.number_input(
                'Introduceti adancimea normala',
                min_value=0.0, max_value=50.0,step =0.01,format='%f',
                help='')
            a=st.sidebar.button('Hit me')
            if a:
                st.title(add_selectbox_Tip_calcul)
                st.title(add_selectbox_Tip_sectiune)
                # Initialize Trapezoidal Channel instance
                trap = Trapezoidal(unknown='channel_slope')

                # Set the inputs
                trap.set_discharge(debit)
                trap.set_sideslope(Panta_taluz)
                trap.set_channel_base(Latime)
                trap.set_roughness(Rugozitatea)
                trap.set_water_depth(adancime)

                # Analyze
                trap.analyze()

                # Show the outputs
                st.write('Panta : ', round(trap.channel_slope*100, 2),' [%]')
                st.write('Aria vie  : ', round(trap.wetted_area, 3),' [mp]')
                st.write('Perimetrul udat: ', round(trap.wetted_perimeter, 3),' [m]')
                st.write('Raza hidraulica: ', round(trap.hydraulic_radius, 4),' [m]')
                st.write('Viteza medie: ', round(trap.velocity, 3),' [m/s]')
                st.pyplot(graf(adancime,Panta_taluz,0,1.0))
    if add_selectbox_Tip_calcul=='Panta hidraulica pentru miscarea uniforma i=?XXXXXXXXX' and  add_selectbox_Tip_sectiune=='Circulara':
            st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
            debit=st.sidebar.number_input(
                'Introduceti debitul de transportat',
                min_value=0.0, max_value=100.0,step=0.5,format='%f',
                help='Debitul   [mc/s]')
            Rugozitatea=st.sidebar.number_input(
                'Introduceti rugozitatea ponderata',
                min_value=0.000, max_value=0.200,step =0.005,format='%f',
                help=' ')
            
            Diametru=st.sidebar.number_input(
                'Introduceti diametrul',
                min_value=0.0, max_value=10.0,step =0.01,format='%f',
                help='')
            adancime=st.sidebar.number_input(
                'Introduceti adancimea normala',
                min_value=0.0, max_value=Diametru,step =0.01,format='%f',
                help='')
            a=st.sidebar.button('Hit me')
            if a:
                st.title(add_selectbox_Tip_calcul)
                st.title(add_selectbox_Tip_sectiune)
                # Initialize Circular Channel instance
                circ = Circular()

                # Set the inputs
                circ.discharge(debit)
                circ.set_diameter(Diametru)
                
                circ.set_roughness(Rugozitatea)
                circ.set_water_depth(adancime)

                # Analyze
                circ.calculate_discharge()

                # Show the outputs
                st.write('Debitul : ', round(circ.discharge, 4),' [mc/s]')
                st.write('Aria vie  : ', round(circ.wetted_area, 3),' [mp]')
                st.write('Perimetrul udat: ', round(circ.wetted_perimeter, 3),' [m]')
                st.write('Raza hidraulica: ', round(circ.hydraulic_radius, 4),' [m]')
                st.write('Gradul de umplere: ', round(adancime/2*circ.hydraulic_radius, 4))
                st.write('Viteza medie: ', round(circ.velocity, 3),' [m/s]')
                st.pyplot(graf_c(Diametru/2,adancime))
if add_selectbox_Tip_sectiune_reg=='Neregulata':
    add_selectbox_Tip_calcul_n = st.sidebar.selectbox(
        'Tip calcul',
        ('','Capacitate de transport Q=?', 'Nivel de calcul h=?', 'Panta hidraulica i=?','Panta hidraulica pentru miscarea neuniforma i=?'),
        help='Q ,h, i sunt obtinute pentru miscarea uniforma')
    if add_selectbox_Tip_calcul_n=='Capacitate de transport Q=?':
        data_file = st.sidebar.file_uploader("Upload CSV",type=['csv'])
        if data_file is not None:
                df=pd.read_csv(data_file)
                st.write(df)
                records = df.to_records(index=False)

                st.write(tuple(zip(df['dc'], df['z'])))
                adresa_mail=st.sidebar.text_input('Introdu adresa de mail')
                st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
                Panta_t=st.sidebar.number_input(
                    'Panta canalului',
                    min_value=0.0, max_value=0.10,step=0.001,format='%f',
                    help='Introduceti panta canalului in  [m/m]')
                Rugozitatea=st.sidebar.number_input(
                    'Introduceti rugozitatea ponderata',
                    min_value=0.000, max_value=0.200,step =0.005,format='%f',
                    help=' ')
                adancime=st.sidebar.number_input(
                    'Introduceti adancimea normala',
                    min_value=0.0, max_value=270.0,step =0.01,format='%f',
                    help='')
                a=st.sidebar.button('Hit me')
                if a:
                    df['z'].min()
                    channel = IrregularSection(records)
                    channel.set_average_rougness(Rugozitatea)
                    channel.set_bed_slope(Panta_t)
                    channel.set_water_elevation(df['z'].min()+adancime)
                    channel.analyze()
                    

                    st.write('Discharge : ', round(channel.discharge, 2))
                    st.write('Wet Area  : ', round(channel.wetted_area, 2))

                    # Plot a water rating curve
                    max_elev = df['z'].max()
                    min_elev = df['z'].min()
                    interval = 0.1
                    intervals = ((max_elev - min_elev) / interval)
                    st.write(max_elev)
                    st.write(min_elev)
                    elevs = []
                    discharges = []

                    for i in range(int(intervals)):
                        elev = min_elev + ((1+i)* interval)
                        channel.set_water_elevation(elev)
                        channel.analyze()
                        discharge = channel.discharge
                        elevs.append(elev)
                        discharges.append(discharge)

                    #p = figure(title='simple line example',x_axis_label='x',y_axis_label='y')
                    #p.line(discharges, elevs, legend_label='Trend', line_width=2)
                    #plt.plot()
                    

                    fig1, ax1 = plt.subplots()
                    ax1.plot(discharges,elevs)
                    ax1.set_title("Cheie limnimetrica")
                    st.pyplot(fig1)
                    fig, ax = plt.subplots()
                    ax.plot(df['dc'],df['z'])
                    ax.set_title("Linia terenului")
                    st.pyplot(fig)
                    auto_cad(df)
                    time.sleep(5)
                    body = "Salut. Folosesti o aplicatie aflata in faza de testare"
                    filename = "d:/1/lwpolyline1.dxf"

                    yag = yagmail.SMTP(user="mfisaut@gmail.com",password="berila2000")

                    yag.send(
                        to=adresa_mail,
                        subject="in atasament este transversalul",
                        contents=body
                        ,attachments=filename,
                        )
    if add_selectbox_Tip_calcul_n=='Nivel de calcul h=?':
        data_file = st.sidebar.file_uploader("Upload CSV",type=['csv'])
        if data_file is not None:
                df=pd.read_csv(data_file)
                st.write(df)
                records = df.to_records(index=False)

                st.write(tuple(zip(df['dc'], df['z'])))
                adresa_mail=st.sidebar.text_input('Introdu adresa de mail')
                st.sidebar.write('Introduceti datele pentru calculul hidraulic:')
                Panta_t=st.sidebar.number_input(
                    'Panta canalului',
                    min_value=0.0, max_value=0.10,step=0.001,format='%f',
                    help='Introduceti panta canalului in  [m/m]')
                Rugozitatea=st.sidebar.number_input(
                    'Introduceti rugozitatea ponderata',
                    min_value=0.000, max_value=0.200,step =0.005,format='%f',
                    help=' ')
                debit=st.sidebar.number_input(
                    'Introduceti debitul de transportat',
                    min_value=0.0, max_value=1000.0,step=0.5,format='%f',
                    help='Debitul   [mc/s]')
                a=st.sidebar.button('Hit me')
                if a:
                    
                    channel = IrregularSection(records)
                    channel.set_average_rougness(Rugozitatea)
                    channel.set_bed_slope(Panta_t)
                    channel.set_water_elevation(df['z'].min()+0.001)
                    channel.analyze()
                    

                    

                    # Plot a water rating curve
                    max_elev = df['z'].max()
                    min_elev = df['z'].min()
                    interval = 0.001
                    intervals = ((max_elev - min_elev) / interval)
                    st.write(max_elev)
                    st.write(min_elev)
                    min_elev=min_elev+0.001
                    elevs = []
                    discharges = []
                    cota=0

                    for i in range(int(intervals)):
                        elev = min_elev + ((1+i)* interval)
                        channel.set_water_elevation(elev)
                        channel.analyze()
                        discharge = channel.discharge
                        elevs.append(elev)
                        discharges.append(discharge)
                        if abs(discharge-debit)<0.01:
                            cota=elev
                    st.write('Debit : ', round(debit, 2))
                    st.write('Adancime  : ', round(cota, 2))   
                   

                    fig1, ax1 = plt.subplots()
                    ax1.plot(discharges,elevs)
                    ax1.set_title("Cheie limnimetrica")
                    st.pyplot(fig1)
                    fig, ax = plt.subplots()
                    ax.plot(df['dc'],df['z'])
                    ax.set_title("Linia terenului")
                    st.pyplot(fig)
                    auto_cad(df)
                    time.sleep(5)
                    body = "Salut. Folosesti o aplicatie aflata in faza de testare"
)                    
                   
                

                

    
