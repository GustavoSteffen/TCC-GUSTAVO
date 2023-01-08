#  -----------------------------------------------------------------------------------------------------------
#                  TCC GUSTAVO LENHARDT STEFFEN 2022/2023
#                               UFSM - CS
#                         CÓDIGO FINAL PRINCIPAL
#   -----------------------------------------------------------------------------------------------------------

#   -----------------------------------------------------------------------------------------------------------
#   IMPORTAÇÕES
#   -----------------------------------------------------------------------------------------------------------
from tkinter import *
from math import sqrt, atan, cos
import serial.tools.list_ports_common
import Tcc_Modulo
import threading
import serial.tools.list_ports
from time import sleep



Master = Tk()
SearchingPorts = True

Grafico_Atual = 0

#   -----------------------------------------------------------------------------------------------------------
#   FUNÇÕES
#   -----------------------------------------------------------------------------------------------------------
def ask_to_open_port():
    message.botton("Por favor, abra a porta serial")

def f_receiving_serial():
    while True:
        sleep(0.3)
        if Tcc_Modulo.is_open():
            Tcc_Modulo.reset_input_buffer()
            try:
                serial_data = Tcc_Modulo.read_line()
                #print(serial_data)
                X = str(serial_data).replace("b'","").replace(" \n'","")
                #print(X)
                Y = X.split()
                #print(Y)
                LerSerial_Rot = Y[0]
                LerSerial_PRU = Y[1]
                LerSerial_PAU = Y[2]
                LerSerial_VU = Y[3]
                LerSerial_IU = Y[4]
                LerSerial_PFU = Y[5]
                LerSerial_PRV = Y[6]
                LerSerial_PAV = Y[7]
                LerSerial_VV = Y[8]
                LerSerial_IV = Y[9]
                LerSerial_PFV = Y[10]
                LerSerial_PRW = Y[11]
                LerSerial_PAW = Y[12]
                LerSerial_VW = Y[13]
                LerSerial_IW = Y[14]
                LerSerial_PFW = Y[15]

                message.rotacao(LerSerial_Rot)
                message.I_U(LerSerial_IU)
                message.V_U(LerSerial_VU)
                message.I_V(LerSerial_IV)
                message.V_V(LerSerial_VV)
                message.I_W(LerSerial_IW)
                message.V_W(LerSerial_VW)

                IU = calc_corrente_U(LerSerial_IU)
                message.corrente_U(f"{IU:.2f}")

                IV = calc_corrente_V(LerSerial_IV)
                message.corrente_V(f"{IV:.2f}")

                IW = calc_corrente_W(LerSerial_IW)
                message.corrente_W(f"{IW:.2f}")

                FP_U, FP_V, FP_W = calcFP(LerSerial_PFU, LerSerial_PFV, LerSerial_PFW)
                message.FP_U(f"{FP_U:.2f}")
                message.FP_V(f"{FP_V:.2f}")
                message.FP_W(f"{FP_W:.2f}")

                PR = calc_potencia_real(LerSerial_PRU, LerSerial_PRV, LerSerial_PRW, FP_U, FP_V, FP_W)
                message.PotenciaReal(f"{PR:.2f}")

                ESCO = calc_escorregamento(LerSerial_Rot)
                message.Escorregamento(f"{ESCO:.2f}")

                FP = calc_FP(LerSerial_PRU, LerSerial_PRV, LerSerial_PRW, LerSerial_PAU, LerSerial_PAV, LerSerial_PAW, PR)
                message.FatorDePotencia(f"{FP:.2f}")

                PCONV = calc_PCONV(PR, LerSerial_IU, LerSerial_IV, LerSerial_IW, ESCO)

                TORQUE = calc_Torque(PCONV, LerSerial_Rot)
                message.Torque(f"{TORQUE:.2f}")

                RENDIMENTO = calc_rendimento(LerSerial_VU, LerSerial_VV, LerSerial_VW, LerSerial_IU, LerSerial_IV, LerSerial_IW, PCONV, PR)
                message.Rendimento(f"{RENDIMENTO:.2f}")

            except IOError:
                message.botton("Erro")

def calcFP(PFU, PFV, PFW):
    try:
        PF_U = float(PFU)
        PF_V = float(PFV)
        PF_W = float(PFW)
        if Ligacao.get()==1: #Ligacao Estrela
            PF__U = PF_U
            PF__V = PF_V
            PF__W = PF_W

        else: #Ligacao Triangulo
            PF__U = PF_U - 0.45
            PF__V = PF_V - 0.42
            PF__W = PF_W - 0.42

        return PF__U, PF__V, PF__W

    except:
        return 0.0, 0.0, 0.0

def calc_corrente_U(IU):
    try:
        Ia = float(IU)
        if Ligacao.get()==1: #Ligacao Estrela
            Iu=Ia

        else: #Ligacao Triangulo
            Iu = Ia/1.732050807

        return Iu

    except:
        return 0.0

def calc_corrente_V(IV):
    try:
        Ib = float(IV)
        if Ligacao.get()==1: #Ligacao Estrela
            Iv=Ib

        else: #Ligacao Triangulo
            Iv = Ib/1.732050807

        return Iv

    except:
        return 0.0

def calc_corrente_W(IW):
    try:
        Ic = float(IW)
        if Ligacao.get()==1: #Ligacao Estrela
            Iw=Ic

        else: #Ligacao Triangulo
            Iw = Ic/1.732050807

        return Iw

    except:
        return 0.0

def calc_potencia_real(PRU, PRV, PRW, FP_U, FP_V, FP_W):
    try:
        PU = float(PRU)
        PV = float(PRV)
        PW= float(PRW)
        FPU = FP_U
        FPV = FP_V
        FPW = FP_W
        if Ligacao.get() == 1:  # Ligacao Estrela
            PR = float(PRU) + float(PRV) + float(PRW)

        else:  # Ligacao Triangulo
            PR = ((float(PRU)/1.732050807)*(FPU*1.40)) + ((float(PRV)/1.732050807)*(FPV*1.40)) + ((float(PRW)/1.732050807)*(FPW*1.40))

        return PR

    except:
        return 0.0


def calc_escorregamento(rot):
    try:
        VelSinc = float(EntryVelSin.get())
        return (1-(float(rot)/VelSinc))*100

    except:
        return 0.0

def calc_FP(PRU, PRV, PRW, PAU, PAV, PAW, PR):
    try:
        PQU = sqrt(abs((float(PAU)*float(PAU))-(float(PRU)*float(PRU))))
        PQV = sqrt(abs((float(PAV)*float(PAV))-(float(PRV)*float(PRV))))
        PQW = sqrt(abs((float(PAW)*float(PAW))-(float(PRW)*float(PRW))))
        PQ = PQU + PQV + PQW
        return cos(atan(PQ/PR))

    except:
        return 0.0

def calc_PCONV(PR, IU, IV, IW, ESCO):
    try:
        R1 = float(EntryR1.get())
        if Ligacao.get()==1: #Ligacao Estrela
            Il = (float(IU) + float(IV) + float(IW)) / 3

        else: #Ligacao Triangulo
            Il = ((float(IU) + float(IV) + float(IW)) / 3) / 1.7320508075

        Pcobre = float(3 * Il * Il * R1)
        Pentreferro = float(float(PR) - Pcobre)
        return float((1 - (ESCO/100)) * Pentreferro)
    except:
        return 0.0

def calc_Torque(P_Conv, ROT):
    try:
        Po_Conv = float (P_Conv)
        Velocidade = float(ROT) / 9.5492965964254
        return float(Po_Conv / Velocidade)

    except:
        return 0.0

def calc_rendimento (VU, VV, VW, IU, IV, IW, PCONV, PR):
    try:
        R1 = float(EntryR1.get())
        jX1 = float(EntryjX1.get())
        R2 = float(EntryR2.get())

        if Ligacao.get()==1: #Ligacao Estrela
            Il = (float(IU) + float(IV) + float(IW)) / 3

        else: #Ligacao Triangulo
            Il = ((float(IU) + float(IV) + float(IW)) / 3) / 1.7320508075

        return ((PCONV) / PR) * 100
    except:
        return 0.0

def f_searching_ports():
    global SearchingPorts
    while True:
        sleep(0.3)
        if SearchingPorts:
            message.botton('Aguarde, procurando COM ports...')
            ports = serial.tools.list_ports.comports(include_links=False)
            port_list.delete('0', 'end')
            idx = 0
            for port in sorted(ports):
                port_list.insert(idx, port.device)
                idx = idx + 1
            port_list["height"] = idx
            SearchingPorts = False
            message.botton('Escolha a porta em que o micro está conectado')


def F1():
   if Tcc_Modulo.Port == 'COMx':
       message.botton('Escolha a porta em que o micro está conectado')
       return None
   if not Tcc_Modulo.is_open():
       Tcc_Modulo.open()
       if Tcc_Modulo.is_open():
           message.botton('Conectado!!!')
           Botao1["image"] = botao1_fechado
           if not receiving_serial.is_alive():
               receiving_serial.start()
   else:
       Tcc_Modulo.close()
       message.botton("Microcontrolador Desconectado!!!")
       Botao1["image"] = botao1_aberto

def F2():
    global SearchingPorts
    SearchingPorts = True

#   -----------------------------------------------------------------------------------------------------------
#   WIDGETS
#   -----------------------------------------------------------------------------------------------------------
back_img = PhotoImage(file="Fundo.png")
botao1_aberto = PhotoImage(file="Nao_Conectado.png")
botao1_fechado = PhotoImage(file="Conectado.png")
botao2 = PhotoImage(file="Atualizar.png")

label_fundo = Label(Master, image=back_img)
label_fundo.place(x=0, y=0)

Botao1 = Button(Master, image=botao1_aberto, bd=0, command=F1)
Botao1.place(width=56, height=45, x=25, y=501)

Botao2 = Button(Master, image=botao2, bd=0, command=F2)
Botao2.place(width=52, height=37, x=108, y=503)

EntryR1 = Entry(Master, font="Arial 14", bg="white", bd=0)
EntryR1.place(width=90, height=30, x=458, y=53)
EntryR1.insert(END, 0.00)

EntryR2 = Entry(Master, font="Arial 14", bg="white", bd=0)
EntryR2.place(width=94, height=28, x=458, y=98)
EntryR2.insert(END, 0.00)

EntryjX1 = Entry(Master, font="Arial 14", bg="white", bd=0)
EntryjX1.place(width=94, height=28, x=458, y=143)
EntryjX1.insert(END, 0.00)

EntryjX2 = Entry(Master, font="Arial 14", bg="white", bd=0)
EntryjX2.place(width=94, height=28, x=458, y=185)
EntryjX2.insert(END, 0.00)

EntryjXm = Entry(Master, font="Arial 14", bg="white", bd=0)
EntryjXm.place(width=94, height=28, x=458, y=230)
EntryjXm.insert(END, 0.00)

EntryVelSin = Entry(Master, font="Arial 14", bg="white", bd=0)
EntryVelSin.place(width=127, height=28, x=219, y=266)
EntryVelSin.insert(END, 00.00)

Ligacao = IntVar()
Ligacao.set(1)

CheckEstrela = Checkbutton(Master,  variable=Ligacao, onvalue=1, bg="#ffbd59")
CheckEstrela.place(x=108, y=271)

CheckTriangulo = Checkbutton(Master,  variable=Ligacao, onvalue=0, bg="#ffbd59")
CheckTriangulo.place(x=27, y=271)

port_list = Listbox(Master, height=1, width=7, bd=0, font="Arial 12", bg="white",
                    highlightcolor="black",
                    highlightthickness=0,
                    selectbackground="light gray",
                    )

port_list.place(width=90, height=90, x=26, y=370)
port_list.insert(END, "COM5")
port_list.bind('<Double-Button>', lambda e: message.port("green", port_list.get(ANCHOR)))

#Threads para busca das portas
SearchingPorts = threading.Thread(target=f_searching_ports)
SearchingPorts.daemon = True
SearchingPorts.start()

#Thread recepção serial
receiving_serial = threading.Thread(target=f_receiving_serial)
receiving_serial.daemon = True

# Comandos do mouse para o posicionador de Widgets
#Master.bind('<Button-1>', lambda e: ulwplace1.m_btn1(e, Master))
#Master.bind('<Button-3>', lambda e: ulwplace1.m_btn3(e, Master))
#Master.bind('<ButtonRelease-1>', lambda e: ulwplace1.m_btn1_release(e, Master))

message = Tcc_Modulo.Message(Master)


#   -----------------------------------------------------------------------------------------------------------
#   CONFIGURAÇÕES DA TELA MASTER
#   -----------------------------------------------------------------------------------------------------------
Master.title("Analisador de Parâmetros Motor de Indução Trifásico")
Master.iconbitmap(default='Icon.ico')
Master.resizable(width=FALSE, height=FALSE)
Master.geometry("1105x630+201+9")
Master.mainloop()
