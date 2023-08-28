import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('단철근 휨설계')
st.header('f_ck 증가에 따른 Mcr 변화 그래프 ')

#As, fy, fck, b, dt 입력
f_ck =np.arange(1,40)
f_y = st.number_input('f_y 입력')
As = st.number_input('As 입력')
b =st.number_input('b 입력')
dt =st.number_input('dt 입력')
h =st.number_input('h 입력')

E_s = 2*(10**6)
st.write('E_s = 2*(10**6)')
epsilon_y = f_y/E_s
st.write('epsilon_y = f_y/E_s')
epsilon_tl = 0.005
st.write('epsilon_tl = 0.005')
epsilon_tmin = 0.004
st.write('epsilon_tmin = 0.004')

st.write('fck가 40Mpa보다 작은 경우')
n = 2
epsilon_co = 0.002
epsilon_cu = 0.0033

st.write('n = 2')
st.write('epsilon_co = 0.002')
st.write('epsilon_cu = 0.0033')
    
#fck(설계기준압축강도)에 따른 변수 구하기
alpha = round(1 - (1)/(n+1)*(epsilon_co/epsilon_cu),1)
B = round(1 - ((0.5-(1/((n+1)*(n+2))*(epsilon_co/epsilon_cu)**2))/alpha),1)

st.write('alpha=1 - (1)/(n+1)*(epsilon_co/epsilon_cu)')
st.write('B = 1 - ((0.5-(1/((n+1)*(n+2))*(epsilon_co/epsilon_cu)**2))/alpha)')

    #n1, B1구하기
ETA_s = alpha/(2*B)
B_1 = 2*B
    
st.write('ETA_s = alpha/(2*B)')
st.write('B_1 = 2*B')

    #a, c계산(a=압축응력깊이, c=중립축 깊이)
a = (As*f_y)/(ETA_s*0.85*f_ck*b)
c = a/B_1

st.write('a = (As*f_y)/(ETA_s*0.85*f_ck*b)')
st.write('c = a/B_1')


    #지배단면과 강도감소계수(PHI) 결정 
if f_y > 400:#
        epsilon_t = 2*epsilon_y#2를 곱해야하는지 2.5를 곱해야하는지 모르겠음
        st.write('epsilon_t = 2*epsilon_y')
        if epsilon_t > epsilon_tl:
            st.write('psilon_t > epsilon_tl')
            PHI = 0.85
            st.write('PHI = 0.85')
            print("인장지배단면") #작업중 PDF 4-1장 2P
            st.write('인장지배단면')
else:
        epsilon_t = epsilon_cu*((dt-c)/c)
        st.write('epsilon_t = epsilon_cu*((dt-c)/c)')

        if all(epsilon_t < epsilon_tmin):
            st.write('epsilon_t < epsilon_tmin')
            print("(et = ",epsilon_t,") <0.004로 최소허용변형률을 만족하지 못함") #작업중 PDF 4-1장 2P
            st.write('et < 0.004로 최소허용변형률을 만족하지 못함')
        elif all(epsilon_t > epsilon_tl):
            st.write('epsilon_t > epsilon_tl')
            PHI = 0.85
            st.write('PHI = 0.85')
            print("(et = ",epsilon_t,") >0.005로 인장지배단면")#작업중 PDF 4-1장 2P
            st.write('et > 0.005로 인장지배단면')
        else:
            PHI = 0.85 - ((epsilon_tl-epsilon_t)/(epsilon_tl-epsilon_y))*0.2
            st.write('PHI = 0.85 - ((epsilon_tl-epsilon_t)/(epsilon_tl-epsilon_y))*0.2')
            print("0.004< (et = ",epsilon_t,") <0.005 이므로 변화구간단면")#작업중 PDF 4-1장 2P
            st.write('0.004 < et = < 0.005 이므로 변화구간단면')

    #공칭휨강도 및 설계휨강도 계산(KN*m 단위)
import math
Mn = As*f_y*(dt-a/2)*math.pow(10, -6)
st.write('As*f_y*(dt-a/2)*10^-6')
Md = PHI*Mn
st.write('Md = PHI*Mn')


    #최소철근량 검토(보통중량콘크리트만 적용가능)
f_r = 0.63*1*f_ck**0.5
st.write('f_r = 0.63*1*f_ck^0.5')

I_g = b*math.pow(h, 3)/12
st.write('I_g = b*math.pow(h, 3)/12')

y_t = h/2
st.write('y_t = h/2')

Mcr = (f_r*I_g/y_t)*math.pow(10, -6)
st.write('Mcr = (f_r*I_g/y_t)*10^-6')

if all(Md >= 1.2*Mcr):
        print("Md = ",Md,", 1.2*Mcr = ",Mcr," (Md >= 1.2*Mcr이므로 적합)")
        st.write('Md >= 1.2*Mcr이므로 적합')
else:
        print("부적합")
        st.write('Md <= 1.2*Mcr이므로 부적합')
    
    
print(ETA_s, B_1)
print(a,c)
print(epsilon_t, PHI)
print(Mn, Md)
print(As)
      

st.header('숫자')


st.write('n=')
n
st.write('epsilon_co=')
epsilon_co
st.write('epsilon_cu=')
epsilon_cu
st.write('epsilon_y=')
epsilon_y
st.write('epsilon_tl=')
epsilon_tl
st.write('epsilon_tmin=')
epsilon_tmin
st.write('alpha=')
alpha
st.write('B=')
B
st.write('ETA_s=')
ETA_s
st.write('B_1=')
B_1
st.write('a=')
a
st.write('c=')
c
st.write('epsilon_t=')
epsilon_t
st.write('Mn=')
Mn
st.write('Md=')
Md
st.write('f_r=')
f_r
st.write('I_g=')
I_g
st.write('y_t=')
y_t
st.write('Mcr=')
Mcr
#v1




df = pd.DataFrame({
    "f_ck": f_ck,
    "Mcr": Mcr})

st.dataframe(df)

fig, ax = plt.subplots()
ax.bar(df["f_ck"], df["Mcr"])
st.pyplot(fig)