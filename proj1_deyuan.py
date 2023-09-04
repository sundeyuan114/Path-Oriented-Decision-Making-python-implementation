#Deyuan Sun ece6140 proj1 code starting on 9/4/2023
import sys
from enum import Enum


# Limit the input str, making sure weird gates does not exist
class Gate():
    def __init__(self, name = -1, value = -1, number = -1, gate1 = -1, gate2 = -1, gate3 = -1):
        self.name = name
        self.value = value
        self.number = number
        self.gate1 = gate1
        self.gate2 = gate2
        self.gate3 = gate3
    def print_self(self):
        print(self.name, self.value, self.number, self.gate1, self.gate2, self.gate3)
        pass
class Net():
    def __init__(self, number = -1, input_gate = -1, output_gate_list = []):
        self.number = number
        self.input_gate = input_gate
        self.output_gate_list = output_gate_list
    def print_self(self):
        print(self.number, self.input_gate, self.output_gate_list)    

gate_list = []
net_list = {}

def Read_netlist(input_file_name:str):
    with open("./files/" + input_file_name, "r") as infile:
        lineno = 0
        for line in infile:
            temp = line.strip().split()
            gate_node = Gate(name= temp[0], number= lineno, gate1= temp[1], gate2 = temp[2], gate3 = temp[3] if len(temp) > 3 else -1)
            #gate part works fine so far
            for net_num in temp[1:]:
                if net_num not in net_list:
                    net_list[net_num] = Net(number= net_num, input_gate= -1 if net_num < (len(temp)-1) else lineno, output_gate_list=[])

            gate_list.append(gate_node)
            lineno += 1
    pass
    # read the netlist file and build up 2 data structures for gates and nets
    print (gate_list[0].print_self())
    
    #print (gate_list[1].print_self())




def Simulation():
    pass
    # get main simultion process right here







if __name__ == "__main__":
    pass
    # assign input file and output file here.
    input_file_name = sys.argv[1]
    Read_netlist(input_file_name)