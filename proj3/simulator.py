# Deyuan Sun ece6140 proj1 code starting on 9/4/2023
# Finished in 10-15 hrs
# Last modified 9/16/2023

# usage: put all files in a folder called 'files' parallel to this python file
# python3 .\proj1_deyuan.py s27.txt s27_input.txt >> out_s27.txt
# python3 .\proj1_deyuan.py s298f_2.txt s298f_2_input.txt >> out_s298f_2.txt
# python3 .\proj1_deyuan.py s344f_2.txt s344f_2_input.txt >> out_s344f_2.txt
# python3 .\proj1_deyuan.py s349f_2.txt s349f_2_input.txt >> out_s349f_2.txt

import sys



# ONLY SCHOOL PROJECT - I might not USE this at all xD

type_dict = {'invalid': -1 , 'zero': 0, 'one': 1, 'D':2, 'Dbar':3 , 'X':4}
value_dict = {-1 : 'invalid' , 0 :  '0' , 1 : '1', 2: 'D', 3: 'Dbar' , 4:'X'}
#  value_types(Enum):
#     invalid = -1
#     zero = 0
#     one = 1
#     D = 2
#     Dbar = 3
#     X = 4
#


def test_print(gate_list:[], net_list:{}):
    print (net_list.keys())
    print("self.number, self.value, self.input_gate, self.output_gate_list")    
    for value in net_list.keys():
        net_list[value].print_self()
    print("----------------")
    print("self.name, self.value, self.number, self.net1, self.net2, self.net3")
    for gate in gate_list:
        gate.print_self()
    print("----------------")
def clear_all_values():
    for key in net_list.keys():
        net_list[key].value = -1

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
    def __init__(self, number = -1, value = -1, input_gate = -1, output_gate_list = []):
        self.number = number
        self.value = value
        self.input_gate = input_gate
        self.output_gate_list = output_gate_list
    def print_self(self):
        print(self.number, self.value, self.input_gate, self.output_gate_list)    
        
gate_list = []
net_list = {}
D_frontier = []
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
    #gate looks fine
def INV(i):
    if i == 2:
        return 3
    if i == 3:
        return 2
    if i == 4:
        return 4
    return 1 ^ i

def calc(gate):
    if gate.net_amount == 2:
        if net_list[str(gate.net1)].value < 2:
            if gate.name == 'BUF':
                return net_list[str(gate.net1)].value
            elif gate.name == 'INV':
                return 1 ^ net_list[str(gate.net1)].value
        else:
            # type_dict = {'invalid': -1 , 'zero': 0, 'one': 1, 'D':2, 'Dbar':3 , 'X':4}
            if gate.name == 'BUF':
                return net_list[str(gate.net1)].value
            elif gate.name == 'INV':
                if net_list[str(gate.net1)].value == 2:
                    return 3
                elif net_list[str(gate.net1)].value == 3:
                    return 2
                elif net_list[str(gate.net1)].value == 4:
                    return 4
            pass
    elif gate.net_amount == 3:
        if (net_list[str(gate.net1)].value < 2) and (net_list[str(gate.net2)].value < 2):
            if gate.name == 'AND':
                return net_list[str(gate.net1)].value & net_list[str(gate.net2)].value
            elif gate.name == 'NAND':
                return 1 ^ (net_list[str(gate.net1)].value & net_list[str(gate.net2)].value)
            elif gate.name == 'OR':
                return net_list[str(gate.net1)].value | net_list[str(gate.net2)].value
            elif gate.name == 'NOR':
                return 1 ^ (net_list[str(gate.net1)].value | net_list[str(gate.net2)].value)
            elif gate.name == 'XOR':
                return net_list[str(gate.net1)].value ^ net_list[str(gate.net2)].value
        else:
            # type_dict = {'invalid': -1 , 'zero': 0, 'one': 1, 'D':2, 'Dbar':3 , 'X':4}
            if net_list[str(gate.net1)].value == 4 and (net_list[str(gate.net2)].value == 2 or net_list[str(gate.net2)].value == 3):
                D_frontier.append(gate)
            elif net_list[str(gate.net2)].value == 4 and (net_list[str(gate.net1)].value == 2 or net_list[str(gate.net1)].value == 3):
                D_frontier.append(gate)

            if gate.name == 'AND':
                if (net_list[str(gate.net1)].value == 0) or (net_list[str(gate.net2)].value == 0):
                    return 0
                if (net_list[str(gate.net1)].value == 4) or (net_list[str(gate.net2)].value == 4):
                    return 4
                if (net_list[str(gate.net1)].value == 1):
                    return net_list[str(gate.net2)].value
                if (net_list[str(gate.net2)].value == 1):
                    return net_list[str(gate.net1)].value
                if (net_list[str(gate.net1)].value == 2) and (net_list[str(gate.net2)].value == 2):
                    return 2
                if (net_list[str(gate.net1)].value == 3) and (net_list[str(gate.net2)].value == 3):
                    return 3
                if (net_list[str(gate.net1)].value == 2) and (net_list[str(gate.net2)].value == 3):
                    return 0
                if (net_list[str(gate.net1)].value == 3) and (net_list[str(gate.net2)].value == 2):
                    return 0
            elif gate.name == 'NAND':
                if (net_list[str(gate.net1)].value == 0) or (net_list[str(gate.net2)].value == 0):
                    return INV(0)
                if (net_list[str(gate.net1)].value == 4) or (net_list[str(gate.net2)].value == 4):
                    return INV(4)
                if (net_list[str(gate.net1)].value == 1):
                    return INV(net_list[str(gate.net2)].value)
                if (net_list[str(gate.net2)].value == 1):
                    return INV(net_list[str(gate.net1)].value)
                if (net_list[str(gate.net1)].value == 2) and (net_list[str(gate.net2)].value == 2):
                    return INV(2)
                if (net_list[str(gate.net1)].value == 3) and (net_list[str(gate.net2)].value == 3):
                    return INV(3)
                if (net_list[str(gate.net1)].value == 2) and (net_list[str(gate.net2)].value == 3):
                    return INV(0)
                if (net_list[str(gate.net1)].value == 3) and (net_list[str(gate.net2)].value == 2):
                    return INV(0)
            # type_dict = {'invalid': -1 , 'zero': 0, 'one': 1, 'D':2, 'Dbar':3 , 'X':4}
            elif gate.name == 'OR':
                if (net_list[str(gate.net1)].value == 1) or (net_list[str(gate.net2)].value == 1):
                    return 1
                if (net_list[str(gate.net1)].value == 4) or (net_list[str(gate.net2)].value == 4):
                    return 4
                if (net_list[str(gate.net1)].value == 0):
                    return net_list[str(gate.net2)].value
                if (net_list[str(gate.net2)].value == 0):
                    return net_list[str(gate.net1)].value
                if (net_list[str(gate.net1)].value == 2) and (net_list[str(gate.net2)].value == 2):
                    return 2
                if (net_list[str(gate.net1)].value == 3) and (net_list[str(gate.net2)].value == 3):
                    return 3
                if (net_list[str(gate.net1)].value == 2) and (net_list[str(gate.net2)].value == 3):
                    return 1
                if (net_list[str(gate.net1)].value == 3) and (net_list[str(gate.net2)].value == 2):
                    return 1
            elif gate.name == 'NOR':
                if (net_list[str(gate.net1)].value == 1) or (net_list[str(gate.net2)].value == 1):
                    return INV(1)
                if (net_list[str(gate.net1)].value == 4) or (net_list[str(gate.net2)].value == 4):
                    return INV(4)
                if (net_list[str(gate.net1)].value == 0):
                    return INV(net_list[str(gate.net2)].value)
                if (net_list[str(gate.net2)].value == 0):
                    return INV(net_list[str(gate.net1)].value)
                if (net_list[str(gate.net1)].value == 2) and (net_list[str(gate.net2)].value == 2):
                    return INV(2)
                if (net_list[str(gate.net1)].value == 3) and (net_list[str(gate.net2)].value == 3):
                    return INV(3)
                if (net_list[str(gate.net1)].value == 2) and (net_list[str(gate.net2)].value == 3):
                    return INV(1)
                if (net_list[str(gate.net1)].value == 3) and (net_list[str(gate.net2)].value == 2):
                    return INV(1)
            elif gate.name == 'XOR':
                if (net_list[str(gate.net1)].value == 4) or (net_list[str(gate.net2)].value == 4):
                    return 4 
                if (net_list[str(gate.net1)].value >= 2) and (net_list[str(gate.net2)].value < 2):
                    if (net_list[str(gate.net2)].value == 1):
                        return INV(net_list[str(gate.net1)].value)
                    return net_list[str(gate.net1)].value
                if (net_list[str(gate.net1)].value < 2) and (net_list[str(gate.net2)].value >= 2):
                    if (net_list[str(gate.net1)].value == 1):
                        return INV(net_list[str(gate.net2)].value)
                    return net_list[str(gate.net2)].value
                if (net_list[str(gate.net1)].value) == (net_list[str(gate.net2)].value):
                    return 0
                else:
                    return 1
                
            pass
def update_queue(used_net_tracking_list, gateQ):
    for gate in gate_list:
        if gate.number in used_net_tracking_list:
            pass
        else:
            if gate.net_amount == 2:
                if net_list[gate.net1].value != -1:
                    gateQ.append(gate)
                    used_net_tracking_list.append(gate.number)
            elif gate.net_amount == 3:
                if net_list[gate.net1].value != -1 and net_list[gate.net2].value != -1:
                    gateQ.append(gate)
                    used_net_tracking_list.append(gate.number)

def Simulation(input_output_lists:[], input_vector:str, fault:[]):
    clear_all_values() # clear all the previous values on the circuit
    global D_frontier
    D_frontier = []
    used_net_tracking_list = []
    gateQ = []

    input_vector = input_vector.replace("X", "4") 
    # get main simultion process right here
    # assign logic value to input nets
    for index in range(len(input_output_lists[0])-1):
        net_list[input_output_lists[0][index]].value = int(input_vector[index])
        if input_output_lists[0][index] == fault[0]:
            if net_list[input_output_lists[0][index]].value == 1 and fault[1] == '0':
                net_list[input_output_lists[0][index]].value = 2 
            elif net_list[input_output_lists[0][index]].value == 0 and fault[1] == '1':
                net_list[input_output_lists[0][index]].value = 3
            elif net_list[input_output_lists[0][index]].value == 4:
                net_list[input_output_lists[0][index]].value = 2 + int(fault[1]) # remember 2 is D, 3 is Dbar
    # assign seems to work
    
    # update queue
    update_queue(used_net_tracking_list=used_net_tracking_list, gateQ=gateQ)
    # update seems to work

    while len(gateQ) != 0:
        curr_gate = gateQ.pop(0)
        #print(curr_gate.number)
        if curr_gate.net_amount == 2:
            print("Input of NO", curr_gate.number, curr_gate.name, value_dict[net_list[curr_gate.net1].value])
            net_list[str(curr_gate.net2)].value = calc(curr_gate)
            if str(curr_gate.net2) == fault[0]:
                if net_list[str(curr_gate.net2)].value == 1 and fault[1] == '0':
                    net_list[str(curr_gate.net2)].value = 2 # == D
                elif net_list[str(curr_gate.net2)].value == 0 and fault[1] == '1':
                    net_list[str(curr_gate.net2)].value = 3 # == Dbar
                elif net_list[str(curr_gate.net2)].value == 4:
                    net_list[str(curr_gate.net2)].value = 2 + int(fault[1])
            print("Output", value_dict[net_list[curr_gate.net2].value])
            print()
        elif curr_gate.net_amount == 3:
            print("Input of NO", curr_gate.number,curr_gate.name, value_dict[net_list[curr_gate.net1].value]," ",value_dict[net_list[curr_gate.net2].value])
            net_list[str(curr_gate.net3)].value = calc(curr_gate)
            if str(curr_gate.net3) == fault[0]: # if fault happens on current output net
                if net_list[str(curr_gate.net3)].value == 1 and fault[1] == '0':
                    net_list[str(curr_gate.net3)].value = 2 # sa0 => D
                elif net_list[str(curr_gate.net3)].value == 0 and fault[1] == '1':
                    net_list[str(curr_gate.net3)].value = 3 # sa1 -> Db
                elif net_list[str(curr_gate.net3)].value == 4:
                    net_list[str(curr_gate.net3)].value = 2 + int(fault[1])
            print("net numbers", curr_gate.net1, curr_gate.net2)
            print("Output", value_dict[net_list[curr_gate.net3].value])
            print()
        update_queue(used_net_tracking_list=used_net_tracking_list, gateQ=gateQ)
    #print_D_frontier()
def print_D_frontier():
    print("----DF start----")
    for df in D_frontier:
        df.print_self()
    print("----DF end------")

def Objective():
    # Random select Df? 
    # No, always select the first Df gate :D decrease performance?? but easier to debug

    # Remember Df only possible when it is a 2 input gate
    # Remember 1 of input must be X and the other input must be D or Db
    # So we find the X and change it to non-controlling value.
    if net_list[D_frontier[0].net1].value == 4:
        if D_frontier[0].name == "AND" or D_frontier[0].name == "NAND":
            return [D_frontier[0].net1, 1] # [string, int]
        if D_frontier[0].name == "OR" or D_frontier[0].name == "NOR":
            return [D_frontier[0].net1, 0]
    elif net_list[D_frontier[0].net2].value == 4:
        if D_frontier[0].name == "AND" or D_frontier[0].name == "NAND":
            return [D_frontier[0].net2, 1] # [string, int]
        if D_frontier[0].name == "OR" or D_frontier[0].name == "NOR":
            return [D_frontier[0].net2, 0]
    pass

def Backtrace(j, cbar): 
    parity = 0
    current_gate_number = net_list[j].input_gate
    print((current_gate_number) )
    if int(current_gate_number) == -1: # idk it's int or str LOL
        return [j, cbar]
    current_gate = gate_list[current_gate_number]
    if current_gate.name == "NAND" or current_gate.name == "NOR":
        parity = parity ^ 1
    while(True):
        print(current_gate_number)
        if net_list[current_gate.net1].value == 4:
            current_gate_number = net_list[current_gate.net1].input_gate
            if int(current_gate_number) == -1:
                return [current_gate.net1, cbar ^ parity]
        elif net_list[current_gate.net2].value == 4:
            current_gate_number = net_list[current_gate.net2].input_gate
            if int(current_gate_number) == -1:
                return [current_gate.net2, cbar ^ parity]
        current_gate = gate_list[current_gate_number]
        parity = 1 ^ parity
    pass

def PODEM():
    global input_vector
    print("test vector in PODEM b4 assign == " + input_vector)
    #print(input_vector)
    #if D or Dbar at PO
    for output_port in input_output_lists[1][:len(input_output_lists[1])-1]:
        if net_list[output_port].value == 2 or net_list[output_port].value == 3:
            return True
    #if D_frontier is empty, Im not going to do the df prediction thing LOL
    if len(D_frontier) == 0:
        return False
    # Objective
    [j,cbar] = Objective() # lecture notes defintion of J cbar is messed up in diff slides
    # Backtrace
    [k, v] = Backtrace(j,cbar)
    # IMPLY which is simultion with input
    input_index = -1 # -1 needs to be changed
    cnt = 0
    for input_net_number in input_output_lists[0]: # example input_port_list = [1,3,2,4], i have input_net_number = 4
        # this should give the input index of 3, which means the index 3 (4th item) in the list
        if input_net_number == k:
            input_index = cnt
        cnt += 1
    assert input_index != -1
    #String3 = String1[0:2] + 'p' + String1[3:] 
    
    input_vector = input_vector[0:input_index] + str(v) + input_vector[input_index+1:]
    print("test vector in PODEM after assign == " + input_vector)
    

    Simulation(input_output_lists, input_vector, fault)
    if PODEM():
        return True
    
    input_vector = input_vector[0:input_index] + str(1 ^ v) + input_vector[input_index:]
    Simulation(input_output_lists, input_vector, fault)
    if PODEM():
        return True
    
    input_vector = input_vector[0:input_index] + str(4) + input_vector[input_index:]
    Simulation(input_output_lists, input_vector, fault)
    return False
    pass
if __name__ == "__main__":
    pass
    # assign input file and output file here.
    input_file_name = sys.argv[1]
    global input_vector
    input_vector = sys.argv[2]
    fault_name = '0sa0' # WE DONT HAVE NET 0, this is just a placeholder
    if (len(sys.argv) > 3):
        fault_name = sys.argv[3] ## use format net + "sa" + 1/0   i.e. 15sa0, 9sa1
    global input_output_lists
    input_output_lists = Read_netlist(input_file_name)

    global fault
    fault = fault_name.split("sa", 1)
    Simulation(input_output_lists, input_vector, fault)
    test_print(gate_list, net_list)
    #Call Podem
    #indicator = True
    #
    

    
    #print_D_frontier()
    rtstr = ""
    for output_port in input_output_lists[1][:len(input_output_lists[1])-1]:
        rtstr += str(net_list[output_port].value)

    print(rtstr)

    print(fault_name)

    # if indicator:
    #     print("test vector is " + input_vector)
    # else:
    #     print("undetectable")

    clear_all_values()