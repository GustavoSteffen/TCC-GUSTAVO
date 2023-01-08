#  -----------------------------------------------------------------------------------------------------------
#                  TCC GUSTAVO LENHARDT STEFFEN 2022/2023
#                               UFSM - CS
#                         CÓDIGO FINAL MODULO
#   -----------------------------------------------------------------------------------------------------------

#   ------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import serial
from tkinter import *

Port = "COMx"
Baud = "115200"

comport = serial.Serial()

#   Terminadores
EnvioDeDados_On = 255
EnvioDeDados_Off = 254

#   ------------------------------------------------------------------------------------------------------------
#   Classe para controle dos labels e do beep
#   ------------------------------------------------------------------------------------------------------------
class Message:
    def __init__(self, master):

        self.label_port = Label(master, text="COMx", font="Arial 10 bold", bg="light gray")
        self.label_port.place(width=79, height=28, x=33, y=320)

        self.label_V_U = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_V_U.place(width=66, height=29, x=705, y=54)

        self.label_V_V = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_V_V.place(width=66, height=29, x=705, y=97)

        self.label_V_W = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_V_W.place(width=66, height=29, x=705, y=142)

        self.label_I_U = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_I_U.place(width=66, height=29, x=852, y=54)

        self.label_I_V = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_I_V.place(width=66, height=29, x=852, y=97)

        self.label_I_W = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_I_W.place(width=66, height=29, x=852, y=142)

        self.label_FpU = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_FpU.place(width=66, height=29, x=1005, y=54)

        self.label_FpV = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_FpV.place(width=66, height=29, x=1005, y=97)

        self.label_FpW = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_FpW.place(width=66, height=29, x=1005, y=141)

        self.label_Fp = Label(master, text="0.00", font="Arial 14", bg="white")
        self.label_Fp.place(width=96, height=28, x=903, y=185)

        self.label_PotTri = Label(master, text="0.00", font="Arial 14", bg="white")
        self.label_PotTri.place(width=96, height=28, x=903, y=227)

        self.label_Rotacao = Label(master, text="0.00", font="Arial 12", bg="white")
        self.label_Rotacao.place(width=105, height=29, x=901, y=355)

        self.label_Torque = Label(master, text="0.00", font="Arial 14", bg="white")
        self.label_Torque.place(width=97, height=29, x=903, y=398)

        self.label_Rendimento = Label(master, text="0.00", font="Arial 14", bg="white")
        self.label_Rendimento.place(width=97, height=29, x=903, y=441)

        self.label_Escorregamento = Label(master, text="0.00", font="Arial 14", bg="white")
        self.label_Escorregamento.place(width=97, height=29, x=903, y=485)

        self.label_Mensagem = Label(master, text="Status 2:", font="Arial 13 bold", bg="light blue")
        self.label_Mensagem.place(width=919, height=36, x=36, y=564)


    def port(self, color, port):
        global Port
        Port = port
        self.label_port["text"] = port

    def botton(self, Message):
        self.label_Mensagem["text"] = Message

    def corrente_U(self, IU):
        self.label_I_U["text"] = IU + "A"

    def corrente_V(self, IV):
        self.label_I_V["text"] = IV + "A"

    def corrente_W(self, IW):
        self.label_I_W["text"] = IW + "A"

    def FP_U(self, FP_U):
        self.label_FpU["text"] = FP_U

    def FP_V(self, FP_V):
        self.label_FpV["text"] = FP_V

    def FP_W(self, FP_W):
        self.label_FpW["text"] = FP_W

    def rotacao(self, rot):
        self.label_Rotacao["text"] = rot + "RPM"

    def Escorregamento(self, Esco):
        self.label_Escorregamento["text"] = Esco + "%"

    def PotenciaReal(self, PR):
        self.label_PotTri["text"] = PR + "W"

    def FatorDePotencia(self, fp):
        self.label_Fp["text"] = fp

    def Torque(self, torque):
        self.label_Torque["text"] = torque + "Nm"

    def Rendimento(self, rendimento):
        self.label_Rendimento["text"] = rendimento + "%"

    def I_U(self, I_U):
        self.label_I_U["text"] = I_U + "A"

    def V_U(self, V_U):
        self.label_V_U["text"] = V_U + "V"

    def Fp_U(self, Fp_U):
        self.label_FpU["text"] = Fp_U

    def Fp_V(self, Fp_V):
        self.label_FpV["text"] = Fp_V

    def Fp_W(self, Fp_W):
        self.label_FpW["text"] = Fp_W

    def I_V(self, I_V):
        self.label_I_V["text"] = I_V + "A"

    def V_V(self, V_V):
        self.label_V_V["text"] = V_V + "V"

    def I_W(self, I_W):
        self.label_I_W["text"] = I_W + "A"

    def V_W(self, V_W):
        self.label_V_W["text"] = V_W + "V"

#   ------------------------------------------------------------------------------------------------------------
#   Funções
#   ------------------------------------------------------------------------------------------------------------
def open():
    global comport, Port, Baud
    if not comport.is_open:
        try:
            comport = serial.Serial(port=Port, baudrate=Baud)
        except IOError:
            comport.close()
            comport.open()


def close():
    global comport
    comport.close()

def is_open():
    global comport
    return  comport.is_open

def read_line():
    return comport.readline()

def reset_input_buffer():
    if comport.is_open:
        comport.reset_input_buffer()