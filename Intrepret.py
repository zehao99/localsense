import numpy as np 
import csv
import matplotlib
import matplotlib.pyplot as plt 

def str2float(InString):
    Converted = 0.0
    (Coefficient, Power) = InString.split('E')
    Converted = float(Coefficient) / np.power(10, -int(Power))
    return Converted

def read_csv(sample_number,exp_number):
    data = []
    time = []
    if exp_number < 10:
        exp_number = '0' + str(exp_number)
    else:
        exp_number = str(exp_number)
    with open('scope_1'+str(sample_number)+exp_number+'.csv',  newline='') as datafile:
        csv_reader = csv.reader(datafile)
        line_count = 0
        for line in csv_reader:
            line_count += 1
            if line_count <= 6:
                continue
            if line[3] != '':
                data.append(str2float(line[3]))
                time.append(str2float(line[0]))
            else:
                break
    return data, time

def max_fft(data,time):
    data_fft_original = np.fft.fft(data)
    data_fft = np.abs(data_fft_original)/len(data)*2000
    max_Amp = data_fft[2]
    max_f = 2 #np.argmax(data_fft)
    max_phase = np.angle(data_fft_original[2])/np.pi*180
    return max_Amp, max_f, max_phase

def read_data():
    All_Amp = []
    All_f = []
    All_phase = []
    for j in [23,24,34]:
        Amp_list = []
        f_list = []
        phase_list = []
        for i in range(12):
            data_return, time_return = read_csv(j,i+1)
            Amp, f, phase = max_fft(data_return, time_return)
            Amp_list.append(Amp)
            f_list.append(f)
            phase_list.append(phase)
        All_Amp.append(Amp_list)
        All_f.append(f)
        All_phase.append(phase_list)
    return All_Amp,All_f,All_phase

All_Amp, All_f, All_phase = read_data()
x = np.array([35,30,25,20,15,10,5,3,2,1.5,1.2,1])
r = 13.5
x = x + r
d = 2 * x
x = 1+(r/(np.power(d,1)))+r*r/(np.power(d,2)-r*r) + r*r*r/(np.power(d,3)-2*r*r) + np.power(r,4)/(np.power(d,4)-3*r*r*d*d+np.power(r,4))
x = list(x)

#Save to File
'''
with open('Data.csv', mode='w') as outfile:
    data_writer = csv.writer(outfile, delimiter=',')
    data_writer.writerow(x)
    for i in range(6):
        data_writer.writerow(All_Amp[i])
        data_writer.writerow(All_phase[i])

'''
#Plotting
fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(x,All_Amp[0], label = 'A_23',marker = 'o')
#ax1.plot(x,All_Amp[1], label = 'A_13')
#ax1.plot(x,All_Amp[2], label = 'A_14')
ax1.set_ylabel('Amplitude of Voltage signal(mV)')
#ax1.set_title('Comparison of Two Positions A_14')
ax1.set_title('Hemispere at Center(Current Injected at 1)')
ax1.set_xlim([1,2])
#ax1.set_ylim([0,1])
ax1.legend()
ax2 = fig.add_subplot(312)
ax2.plot(x,All_Amp[1], label = 'A_24',marker = 'o')
ax2.set_ylabel('Amplitude of Voltage signal(mV)')
ax2.set_xlim([1,2])
ax2.legend()
ax3 = fig.add_subplot(313)
ax3.plot(x,All_Amp[2], label = 'A_34',marker = 'o')
ax3.set_ylabel('Amplitude of Voltage signal(mV)')
ax3.set_xlabel('Coefficient D')
ax3.set_xlim([1,2])
ax3.legend()
for i in range(3):
    print(np.polyfit(x,All_Amp[i],1))
    print(np.corrcoef(x,All_Amp[i])[0][1])

plt.show() 