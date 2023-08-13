import streamlit as st

st.title('단철근 휨설계')

#As, fy, fck, b, dt 입력
f_ck = st.number_input('f_ck 입력,40 미만의 실수',0.0,40.0)
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
if f_ck <= 40:
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
    st.write('1 - ((0.5-(1/((n+1)*(n+2))*(epsilon_co/epsilon_cu)**2))/alpha)')

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
        if epsilon_t > epsilon_tl:
            PHI = 0.85
            print("인장지배단면") #작업중 PDF 4-1장 2P
            st.write('인장지배단면')
    else:
        epsilon_t = epsilon_cu*((dt-c)/c)
        if epsilon_t < epsilon_tmin:
            print("(et = ",epsilon_t,") <0.004로 최소허용변형률을 만족하지 못함") #작업중 PDF 4-1장 2P
            st.write('et < 0.004로 최소허용변형률을 만족하지 못함')
        elif epsilon_t > epsilon_tl:
            PHI = 0.85
            print("(et = ",epsilon_t,") >0.005로 인장지배단면")#작업중 PDF 4-1장 2P
            st.write('et > 0.005로 인장지배단면')
        else:
            PHI = 0.85 - ((epsilon_tl-epsilon_t)/(epsilon_tl-epsilon_y))*0.2
            print("0.004< (et = ",epsilon_t,") <0.005 이므로 변화구간단면")#작업중 PDF 4-1장 2P
            st.write('0.004 < et = < 0.005 이므로 변화구간단면')

    #공칭휨강도 및 설계휨강도 계산(KN*m 단위)
    import math
    Mn = As*f_y*(dt-a/2)*math.pow(10, -6)
    Md = PHI*Mn
    
    #최소철근량 검토(보통중량콘크리트만 적용가능)
    f_r = 0.63*1*math.pow(f_ck, 0.5)
    I_g = b*math.pow(h, 3)/12
    y_t = h/2
    Mcr = (f_r*I_g/y_t)*math.pow(10, -6)
    if Md >= 1.2*Mcr:
        print("Md = ",Md,", 1.2*Mcr = ",Mcr," (Md >= 1.2*Mcr이므로 적합)")
        st.write('Md >= 1.2*Mcr이므로 적합')
    else:
        print("부적합")
        st.write('Md <= 1.2*Mcr이므로 부적합')
    
    
    view = (B_1)
    view
    print(ETA_s, B_1)
    print(a,c)
    print(epsilon_t, PHI)
    print(Mn, Md)
    print(As)
      
print(As)

st.number.write('As')
st.write('B')
st.write('a')
st.write('c')
st.write('As')