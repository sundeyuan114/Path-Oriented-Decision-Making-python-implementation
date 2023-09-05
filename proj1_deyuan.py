#Deyuan Sun ece6140 proj1 code starting on 9/4/2023
import sys

def test_print(gate_list:[], net_list:{}):
    print (net_list.keys())
    for value in net_list.keys():
        net_list[value].print_self()
    print("----------------")
    for gate in gate_list:
        gate.print_self()
    print("----------------")
    

# Limit the input str, making sure weird gates does not exist
class Gate():
    def __init__(self, name = -1, value = -1, number = -1, net1 = -1, net2 = -1, net3 = -1):
        self.name = name
        self.value = value
        self.number = number
        self.net1 = net1
        self.net2 = net2
        self.net3 = net3
    def print_self(self):
        print(self.name, self.value, self.number, self.net1, self.net2, self.net3)
        
class Net():
    def __init__(self, number = -1, input_gate = -1, output_gate_list = []):
        self.number = number
        self.input_gate = input_gate
        self.output_gate_list = output_gate_list
    def print_self(self):
        print(self.number, self.input_gate, self.output_gate_list)    
        
gate_list = []
net_list = {}
# input_gate_list = []
# output_gate_list = []

def Read_netlist(input_file_name:str) -> []:
    with open("./files/" + input_file_name, "r") as infile:
        lineno = 0
        
        for line in infile:
            temp = line.strip().split()
            if (temp[0] != "INPUT" and temp[0] != "OUTPUT"):
                #
                # gate part 
                #
                gate_node = Gate(name= temp[0], number= lineno, net1= temp[1], net2 = temp[2], net3 = temp[3] if len(temp) > 3 else -1)
                gate_list.append(gate_node)
                #
                # gate part 
                #

                #
                # net part below
                #
                for net_num_index in range(1, len(temp)):
                    # if first time seen in dict
                    net_num = temp[net_num_index]
                    if net_num not in net_list:
                        if int(net_num_index) < (len(temp)-1):
                            net_list[net_num] = Net(number= net_num, input_gate= -1
                                                , output_gate_list= [lineno])
                        else:
                            net_list[net_num] = Net(number= net_num, input_gate= lineno
                                                , output_gate_list= [])
                        
                    else:
                    #extend the dict values
                        if int(net_num_index) == (len(temp)-1):
                            net_list[net_num].input_gate = lineno
                        else:
                            net_list[net_num].output_gate_list.append(lineno)
                        pass
                #
                # net part above
                #
            else:
                if temp[0] == "INPUT":
                    ilist = [temp[x] for x in range(1,len(temp))]
                else:
                    olist = [temp[x] for x in range(1,len(temp))]
                    return [ilist, olist]
            lineno += 1
    # read the netlist file and build up 2 data structures for gates and nets
    # test_print(gate_list = gate_list, net_list = net_list)
    # print (net_list['1'].number, net_list['1'].input_gate, net_list['1'].output_gate_list)




    # print(self.name, self.value, self.number, self.net1, self.net2, self.net3)
    # for gate in gate_list:
    #     gate.print_self()
    # AND -1 0 1 2 4
    # OR -1 1 2 3 5
    # INV -1 2 4 6 -1
    # XOR -1 3 4 5 7

    #gate looks fine

def Simulation():
    pass
    # get main simultion process right here







if __name__ == "__main__":
    pass
    # assign input file and output file here.
    input_file_name = sys.argv[1]
    input_output_lists = Read_netlist(input_file_name)
    test_print(gate_list = gate_list, net_list = net_list)
    print(input_output_lists)