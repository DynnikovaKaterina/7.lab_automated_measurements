import RPi.GPIO as gp
import time
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [9, 10, 22, 27, 17, 4, 3, 2]
gp.setmode(gp.BCM) 
gp.setup(dac, gp.OUT) #настраиваем все пины из области dac на выход
gp.setup(leds, gp.OUT) #настраиваем все пины из области leds на выход
comp = 14
troyka_V = 13
#troyka_S = 

#функция перевода из десятичного числа в двоичное 
def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

#функция выводит в область leds двоичное представление числа
def dem2leds(value):
    gp.output(leds, decimal2binary(value))


def adc():
    i0 = 0
    for i in range (7, -1, -1):
        gp.output(dac, decimal2binary(i0 + 2**i))
        time.sleep(0.001)
        compVal = gp.input(comp)
        if compVal == 0:
            i0 += 2**i
    return i0

gp.setup(troyka_V, gp.OUT, initial= gp.HIGH)
#gp.setup(troyka_S, gp.IN)
#gp.setup(comp, gp.IN)

U = []
durations = []

try:
    for idx in range(3):
        U.append([])
        t_start = time.time()

        gp.output(troyka_V, gp.HIGH)
        while U[-1] < 0.97 * gp.HIGH:
            U[idx].append(adc())
            print(U[-1])
            
        gp.output(troyka_V, gp.LOW)
        while U[-1] > 0.02 * gp.HIGH:
            U[idx].append(adc())
            print(U[-1])

        t_end = time.time()
        durations.append(t_end - t_start)


finally:
    gp.output(dac, 0)
    gp.output(troyka_V, 0)
    gp.cleanup()