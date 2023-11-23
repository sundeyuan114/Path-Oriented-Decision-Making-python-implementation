# Deyuan Sun ece6140 proj1 code starting on 9/4/2023
# Finished in 10-15 hrs
# Last modified 9/16/2023

# usage: put all files in a folder called 'files' parallel to this python file
# python3 .\proj1_deyuan.py s27.txt s27_input.txt >> out_s27.txt
# python3 .\proj1_deyuan.py s298f_2.txt s298f_2_input.txt >> out_s298f_2.txt
# python3 .\proj1_deyuan.py s344f_2.txt s344f_2_input.txt >> out_s344f_2.txt
# python3 .\proj1_deyuan.py s349f_2.txt s349f_2_input.txt >> out_s349f_2.txt

from matplotlib import pyplot as plt
import random
import sys

def test_print(gate_list:[], net_dict:{}):
    print (net_dict.keys())
    print("self.number, self.value, self.input_gate, self.output_gate_list")    
    for value in net_dict.keys():
        net_dict[value].print_self()
    print("----------------")
    print("self.name, self.value, self.number, self.net1, self.net2, self.net3")
    for gate in gate_list:
        gate.print_self()
    print("----------------")
def clear_all_values():
    for key in net_dict.keys():
        net_dict[key].value = -1
        net_dict[key].fault_list = []

# Limit the input str, making sure weird gates does not exist
class Gate():
    def __init__(self, name = -1, value = -1, number = -1, net1 = -1, net2 = -1, net3 = -1, net_amount = -1):
        self.name = name
        self.value = value
        self.number = number
        self.net1 = net1
        self.net2 = net2
        self.net3 = net3
        self.net_amount = net_amount
    def print_self(self):
        print(self.name, self.value, self.number, self.net1, self.net2, self.net3)
        
class Net():
    def __init__(self, number = -1, value = -1, input_gate = -1, output_gate_list = [], fault_list = []):
        self.number = number
        self.value = value
        self.input_gate = input_gate
        self.output_gate_list = output_gate_list
        self.fault_list = fault_list
    def print_self(self):
        print(self.number, self.value, self.fault_list)    
    def print_fault_list(self):
        print(self.fault_list)

gate_list = []
net_dict = {}
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
                gate_node = Gate(name= temp[0], number= lineno, net1= temp[1], net2 = temp[2], net3 = temp[3] if len(temp) > 3 else -1, net_amount= 3 if len(temp) > 3 else 2)
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
                    if net_num not in net_dict:
                        if int(net_num_index) < (len(temp)-1):
                            net_dict[net_num] = Net(number= net_num, input_gate= -1
                                                , output_gate_list= [lineno], fault_list=[])
                        else:
                            net_dict[net_num] = Net(number= net_num, input_gate= lineno
                                                , output_gate_list= [], fault_list=[])
                        
                    else:
                    #extend the dict values
                        if int(net_num_index) == (len(temp)-1):
                            net_dict[net_num].input_gate = lineno
                        else:
                            net_dict[net_num].output_gate_list.append(lineno)
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
    # test_print(gate_list = gate_list, net_dict = net_dict)
    # print (net_dict['1'].number, net_dict['1'].input_gate, net_dict['1'].output_gate_list)




    # print(self.name, self.value, self.number, self.net1, self.net2, self.net3)
    # for gate in gate_list:
    #     gate.print_self()
    # AND -1 0 1 2 4
    # OR -1 1 2 3 5
    # INV -1 2 4 6 -1
    # XOR -1 3 4 5 7

    #gate looks fine
    

def encypt(number, value):
    return (int(number) << 1 | 1 ^ value)

def calc(gate):
    #print("calclclclclc" , net_dict[str(gate.net1)].number)
    if gate.net_amount == 2:
        if gate.name == 'BUF':
            return net_dict[str(gate.net1)].value
        elif gate.name == 'INV':
            return 1 ^ net_dict[str(gate.net1)].value
    elif gate.net_amount == 3:
        if gate.name == 'AND':
            return net_dict[str(gate.net1)].value & net_dict[str(gate.net2)].value
        elif gate.name == 'NAND':
            return 1 ^ (net_dict[str(gate.net1)].value & net_dict[str(gate.net2)].value)
        elif gate.name == 'OR':
            return net_dict[str(gate.net1)].value | net_dict[str(gate.net2)].value
        elif gate.name == 'NOR':
            return 1 ^ (net_dict[str(gate.net1)].value | net_dict[str(gate.net2)].value)
        elif gate.name == 'XOR':
            return net_dict[str(gate.net1)].value ^ net_dict[str(gate.net2)].value
    else:
        print("shouldn't ever be -1")
def update_queue(used_net_tracking_list, gateQ):
    for gate in gate_list:
        if gate.number in used_net_tracking_list:
            pass
        else:
            if gate.net_amount == 2:
                if net_dict[gate.net1].value != -1:
                    gateQ.append(gate)
                    used_net_tracking_list.append(gate.number)
            elif gate.net_amount == 3:
                if net_dict[gate.net1].value != -1 and net_dict[gate.net2].value != -1:
                    gateQ.append(gate)
                    used_net_tracking_list.append(gate.number)
def deduction(gate):
    ans_list = []
    if gate.net_amount == 2:
        ans_list = net_dict[str(gate.net1)].fault_list+[encypt(net_dict[str(gate.net2)].number, net_dict[str(gate.net2)].value)]

    elif gate.net_amount == 3:
        if gate.name == 'AND' or gate.name == 'NAND':
            if net_dict[str(gate.net1)].value == 1 and net_dict[str(gate.net2)].value == 1:
                ans_list = list(set(net_dict[str(gate.net1)].fault_list) | set(net_dict[str(gate.net2)].fault_list))+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
            if net_dict[str(gate.net1)].value == 0 and net_dict[str(gate.net2)].value == 0:
                ans_list = list(set(net_dict[str(gate.net1)].fault_list) & set(net_dict[str(gate.net2)].fault_list))+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
            if net_dict[str(gate.net1)].value == 1 and net_dict[str(gate.net2)].value == 0:
                ans_list = list(set(net_dict[str(gate.net2)].fault_list) - set(net_dict[str(gate.net1)].fault_list))+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
            if net_dict[str(gate.net1)].value == 0 and net_dict[str(gate.net2)].value == 1:
                ans_list = list(set(net_dict[str(gate.net1)].fault_list) - set(net_dict[str(gate.net2)].fault_list))+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
        elif gate.name == 'OR' or gate.name == 'NOR':
            if net_dict[str(gate.net1)].value == 0 and net_dict[str(gate.net2)].value == 0:
                ans_list = list(set(net_dict[str(gate.net1)].fault_list) | set(net_dict[str(gate.net2)].fault_list))+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
            if net_dict[str(gate.net1)].value == 1 and net_dict[str(gate.net2)].value == 1:
                ans_list = list(set(net_dict[str(gate.net1)].fault_list) & set(net_dict[str(gate.net2)].fault_list))+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
            if net_dict[str(gate.net1)].value == 0 and net_dict[str(gate.net2)].value == 1:
                ans_list = list(set(net_dict[str(gate.net2)].fault_list) - set(net_dict[str(gate.net1)].fault_list))+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
            if net_dict[str(gate.net1)].value == 1 and net_dict[str(gate.net2)].value == 0:
                ans_list = list(set(net_dict[str(gate.net1)].fault_list) - set(net_dict[str(gate.net2)].fault_list))+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
        elif gate.name == 'XOR':
            ans_list = list(   (set(net_dict[str(gate.net1)].fault_list)-set(net_dict[str(gate.net2)].fault_list)) | (set(net_dict[str(gate.net2)].fault_list)-set(net_dict[str(gate.net1)].fault_list)) )+[encypt(net_dict[str(gate.net3)].number, net_dict[str(gate.net3)].value)]
    #print("ans_list", ans_list)
    return ans_list
    pass
def Simulation(input_output_lists:[], input_vector:str):
    used_net_tracking_list = []
    gateQ = []

    


    # get main simultion process right here
    # assign logic value to input nets
    for index in range(len(input_output_lists[0])-1):
        net_dict[input_output_lists[0][index]].value = int(input_vector[index])
        net_dict[input_output_lists[0][index]].fault_list.append(encypt(net_dict[input_output_lists[0][index]].number
                            , net_dict[input_output_lists[0][index]].value))
    
    
    # net_dict['1'].print_self()   
    # net_dict['2'].print_self()
    # net_dict['3'].print_self()
    # assign seems to work
    
    # update queue
    update_queue(used_net_tracking_list=used_net_tracking_list, gateQ=gateQ)
    # update seems to work
    
    while len(gateQ) != 0:
        
        curr_gate = gateQ.pop(0)
        #print(curr_gate.number)
        if curr_gate.net_amount == 2:
            net_dict[str(curr_gate.net2)].value = calc(curr_gate)
            net_dict[str(curr_gate.net2)].fault_list = deduction(curr_gate)
        elif curr_gate.net_amount == 3:
            net_dict[str(curr_gate.net3)].value = calc(curr_gate)
            net_dict[str(curr_gate.net3)].fault_list = deduction(curr_gate)
        update_queue(used_net_tracking_list=used_net_tracking_list, gateQ=gateQ)

        # 
        # for item in gateQ:
        #     item.print_self()
        # for x in used_net_tracking_list:
        #     print(x)

if __name__ == "__main__":
    pass
    # assign input file and output file here.
    input_file_name = sys.argv[1]
    input_vector_file = sys.argv[2]
    flag = "-sim"
    if len(sys.argv) > 3:
        flag = sys.argv[3]
        percentage = sys.argv[4]

    #print(input_vector)

    #read_netlist done
    input_output_lists = Read_netlist(input_file_name)
    
    fault_amount = len(net_dict.keys()) * 2

    # test_print(gate_list = gate_list, net_dict = net_dict)
    # 读完之后的faultlist没有问题

    with open("./files/"+input_vector_file, 'r') as file:
        existed_vector_list = []
        cummulate_fault_set = set()

        if flag != "-r":
            for input_vector in file:
                Simulation(input_output_lists, input_vector)
                rtstr = ""
                comb_fault_list = []
                for output_port in input_output_lists[1][:len(input_output_lists[1])-1]:
                    rtstr += str(net_dict[output_port].value)
                    comb_fault_list += net_dict[output_port].fault_list
                print("Circuit: "+ input_vector_file, "Input Vector: "+input_vector)
                print("--------Fault Detected--------")
                for item in set(comb_fault_list):
                    print(item >> 1,"stuck at", item & 1)
                print("--------End of Detection------")
                clear_all_values()
        else:
            input_vector = file.readline()
            input_vector_len = len(input_vector)
            coverage = 0
            coverage_tracker = []
            while(float(coverage) * 100 < int(percentage)):
                while(True):
                    r = random.randint(0, 2**input_vector_len - 1)
                    if r not in existed_vector_list:
                        existed_vector_list.append(r)
                        break
                
                input_vector = bin(r)[2:].zfill(input_vector_len)

                Simulation(input_output_lists, input_vector)
                comb_fault_list = []
                for output_port in input_output_lists[1][:len(input_output_lists[1])-1]:
                    comb_fault_list += net_dict[output_port].fault_list
                comb_fault_list = set(comb_fault_list)
                cummulate_fault_set = cummulate_fault_set | comb_fault_list
                coverage = len(cummulate_fault_set) / fault_amount
                coverage_tracker.append(coverage)
                clear_all_values()
                
            print(len(coverage_tracker))
            plt.plot(coverage_tracker)
            plt.xlabel("Random Vector Input (Round)")
            plt.ylabel("Coverage (range(0,1))")
            plt.show()