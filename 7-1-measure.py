import RPi.GPIO as gp
import time
import matplotlib.pyplot as plt
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
        gp.output(dac, [int(bit) for bit in bin(i0 + 2**i)[2:].zfill(8)])
        time.sleep(0.004)
        compVal = gp.input(comp)
        if compVal == 0:
            i0 += 2**i
    return i0

gp.setup(troyka_V, gp.OUT, initial= gp.HIGH)
#gp.setup(troyka_S, gp.IN)
gp.setup(comp, gp.IN)

U = []
durations = []

try:
    for idx in range(1):
        U.append([])
        t_start = time.time()

        #возрастание напряжения на конденсаторе
        gp.output(troyka_V, gp.HIGH)
        U[idx].append(adc())
        while U[idx][-1] < 204:
            U[idx].append(adc())
            gp.output(leds, [int(bit) for bit in bin(U[idx][-1])[2:].zfill(8)])
            #print(U[idx][-1])
        
        #падение напряжения на конденсаторе
        gp.output(troyka_V, gp.LOW)
        while U[idx][-1] > 195:
            U[idx].append(adc())
            gp.output(leds, [int(bit) for bit in bin(U[idx][-1])[2:].zfill(8)])
            #print(U[idx][-1])

        t_end = time.time()
        durations.append(t_end - t_start)
        #print(durations)

        plt.plot(U[idx])
        plt.show()

        with open("//home//b03-404//Desktop//7.lab_automated_measurements//data.txt", "w") as outfile:
            outfile.write("\n".join([str(item) for item in U[idx]]))
        
        print(f"длительность эксперимента: {durations[idx]}")
        n = len(U[idx])
        print(f'количество измерений: {n}')
        sampling_frequency = n / durations[idx]
        print(f'частота дискретизации: {sampling_frequency}')
        quantization_frequency = 3.3 / 256
        print(f'шаг квантования: {quantization_frequency}')

        with open("//home//b03-404//Desktop//7.lab_automated_measurements//settings.txt", "w") as outfile:
            outfile.write("\n".join([str(durations[idx]), str(sampling_frequency), str(1/sampling_frequency), str(quantization_frequency)]))
        
        


finally:
    gp.output(dac, 0)
    gp.output(troyka_V, 0)
    gp.cleanup()