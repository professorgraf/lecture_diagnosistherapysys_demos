# ECG data simulator
#
#  based on dataset 100 of
#  Moody GB, Mark RG. The impact of the MIT-BIH Arrhythmia Database. IEEE Eng in Med and Biol 20(3):45-50 (May-June 2001). (PMID: 11446209)
#
#  (c) 2024 - Prof. Dr. Markus Graf
#  Faculty of Informatics, University of Applied Sciences Heilbronn
#
#  Gnu GPL 3.0
#
import matplotlib.pyplot as plt
import numpy as np
import math
import base64

import socket
HOST = "192.168.1.28"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

class EcgSim:
    def __init__(self, dataset_name):
        self.filename = dataset_name
        self.sample_mlii = []
        self.sample_v1 = []

    def load_data_212(self):
        with open(self.filename, "rb") as f:
            b = f.read(3)
            while len(b) == 3:
                part1 = (b[1] >> 4) * 256 + b[0]
                part2 = (b[1] & 0x0f) * 256 + b[2]
                # print(f"val1 {part1} / val2 {part2}")
                self.sample_mlii.append(part1)
                self.sample_v1.append(part2)
                b = f.read(3)

    def get_MLii(self, millisecond):
        while millisecond > 30 * 60000 * 360:
            millisecond -= (30 * 60000 * 360)
        try:
            # tick position is: t [in ms] * 360/1000
            val = self.sample_mlii[ int(millisecond * 360/1000) ]
        except:
            val = 0
        return val


def start_server(sim):
    # serve via socket and return the value of a certain milliseconds
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                bytes_in = list(conn.recv(4))
                while len(bytes_in) < 4:
                    bytes_in.append(list(conn.recv(1))[0])
                if len(bytes_in) == 4:
                    #print(bytes_in)
                    if not bytes:
                        print("no data incoming")
                    else:
                        ms = bytes_in[0] + (bytes_in[1] << 8) + (bytes_in[2] << 16) + (bytes_in[3] << 24)
                        if ms > 1000 * 60 * 360 * 5:
                            ms = divmod(ms, 1000 * 60 * 360 * 5)[1]
                        #print(f"Millis: {ms}")
                        data = sim.get_MLii(ms)
                        bytes_data = bytearray(((data & 0xFF), ((data >> 8) & 0xFF)))
                        #print("Sending")
                        #print(bytes_data)
                        conn.sendall(bytes_data)
                else:
                    print("bytes not enough")


def export_matplot(sim):
    # plot with matplotlib
    plt.figure(figsize=(12, 6))
    plt.title(f"ECG simulation")
    plt.xlabel("t [in seconds]")
    plt.ylabel("y [ADC mV]")
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    # n = len(sim.sample_mii)
    n = 360 * 5
    plt.plot(np.arange(0, n) / 360, sim.sample_mlii[:n], 'r:', linewidth=2.0)
    # plt.plot(np.arange(0, n) / 360, sim.sample_v1[:n], 'b:', linewidth=1.0)
    plt.show()


def export_data(sim, filename, total_ticks=1024, delta_millis=20):
    with open(filename, "wb") as f:
        for i in range(total_ticks):
            value = sim.get_MLii(delta_millis * i)
            byt = value.to_bytes(2)
            f.write(base64.b64encode(byt))
        f.close()


if __name__ == '__main__':
    sim = EcgSim("data/100.dat")
    sim.load_data_212()
    export_data(sim, "data/export.bytes")






