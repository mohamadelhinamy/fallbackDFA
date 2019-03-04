import argparse
class Transition :
    def __init__(self,from_state,to_state,alphabet):
        self.from_state = from_state
        self.to_state = to_state
        self.alphabet = alphabet
class stateExpression :
    def __init__(self,state,expression):
        self.state = state
        self.expression = expression
class expressionAction :
    def __init__(self,expression,action):
        self.action = action
        self.expression = expression        
class DFA : 
    def __init__(self,start_state,end_state,states,transitions , alphabets):
        self.start_state = start_state
        self.end_state = end_state
        self.transitions = transitions
        self.states = states
        self.alphabets = alphabets
expression_action_list = []
state_expression_list = []
def readInputFile(file_name):
    f = open(file_name)
    # read states
    line = f.readline() 
    line = line.replace('\n','')
    states = line.split(',')   
    # print(states)


    # read alphabet
    line1 = f.readline() 
    line1 = line1.replace('\n','')
    alphabet = line1.split(',')   
    # print(alphabet)

    # read start state
    line2 = f.readline() 
    start_state = line2.replace('\n','') 
    # print(start_state)

    # read end states
    line3 = f.readline() 
    end_states = line3.replace('\n','') 
    end_states = end_states.replace(' ','')    
    end_states =  end_states.split(',')
    # end_states = end_states.replace('\n','') 
    # print(end_states)

    # read transitions
    line4 = f.readline() 
    line4 = line4.replace('\n','')
    line4 = line4.replace('), (',';')
    line4 = line4.replace('),  (',';')
    line4 = line4.replace('),(',';')
    line4 = line4.replace('(','')    
    line4 = line4.replace(')','')
    line4 = line4.replace(', ,', ',epislon,')
    line4 = line4.replace(' ', '')
    line4 = line4.replace('􏰀→','')
    line4 = line4.replace(',epislon,', ', ,')
    Transitions = line4.split(';')
    line4 = line4.replace('→','')

    # put transitions in list of transitions
    transition_list = list()
    for transition1 in Transitions : 
        transition1 = transition1.split(',')
        from_state1 = transition1[0]
        to_state1 = transition1[2]
        alphabet1 = transition1[1]
        transition2 = Transition(from_state1,to_state1,alphabet1)
        transition_list.append(transition2)
    #   read state_expression
    line5 = f.readline() 
    line5 = line5.replace('\n','')
    line5 = line5.replace('), (',';')
    line5 = line5.replace('),  (',';')
    line5 = line5.replace('),(',';')
    line5 = line5.replace('(','')    
    line5 = line5.replace(')','')
    line5 = line5.replace('"','')
    line5 = line5.replace('\'','')
    line5 = line5.replace('``','')
    line5 = line5.replace(', ,', ',epislon,')
    line5 = line5.replace(' ', '')
    line5 = line5.replace(',epislon,', ', ,')
    states_expressions = line5.split(';')

    # put states_expression in list of states_expression
    
    for st_ex in states_expressions : 
        st_ex = st_ex.split(',')
        state = st_ex[0]
        expression = st_ex[1]
        st_ex1 = stateExpression(state,expression)
        state_expression_list.append(st_ex1)   

    #   read expression_action
    line6 = f.readline() 
    line6 = line6.replace('\n','')
    line6 = line6.replace('), (',';')
    line6 = line6.replace('),  (',';')
    line6 = line6.replace('),(',';')
    line6 = line6.replace('(','')    
    line6 = line6.replace(')','')
    line6 = line6.replace('"','')
    line6 = line6.replace('\'','')
    line6 = line6.replace('``','')
    line6 = line6.replace(', ,', ',epislon,')
    line6 = line6.replace(' ', '')
    line6 = line6.replace(',epislon,', ', ,')
    expressions_actions = line6.split(';')

    # put expression_action in list of expression_action
    
    for ex_act in expressions_actions : 
        ex_act = ex_act.split(',')
        expression1 = ex_act[0]
        action = ex_act[1]
        ex_act1 = expressionAction(expression1,action)
        expression_action_list.append(ex_act1)         

    result_dfa = DFA(start_state,end_states,states,transition_list,alphabet)
    return result_dfa  

def stack_input(c,DFA,state):

    for transition in DFA.transitions :
        if c == transition.alphabet and state == transition.from_state:
            return transition.to_state

def fallback_dfa(dfa,input_string):
    
    last_accepted_index = -1
    last_accepted_action = ''
    result = ''
    while input_string :
        state = dfa.start_state
        for c in input_string :
            to_state = stack_input(c,dfa,state)
            state = to_state
            if to_state in dfa.end_state :
                last_accepted_index = input_string.index(c)
                for st_exp in state_expression_list :
                    if st_exp.state == state :
                        for exp_act in expression_action_list :
                            if exp_act.expression == st_exp.expression :
                                last_accepted_action = exp_act.action
        if last_accepted_index == -1 :
            for st_exp in state_expression_list :
                    if st_exp.state == state :
                        for exp_act in expression_action_list :
                            if exp_act.expression == st_exp.expression :
                                actionn = exp_act.action
            result += input_string + ', ' + actionn + '\n'
            break 
        else :    
            result += input_string[:last_accepted_index+1] + ', ' +last_accepted_action + '\n'
            input_string = input_string[last_accepted_index+1:]
                
       
        last_accepted_action = ''
        last_accepted_index = -1
    return result   


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--dfa-file', action="store", help="path of file to take as input to construct DFA", nargs="?", metavar="dfa_file")
    parser.add_argument('--input-file', action="store", help="path of file to take as input to test strings in on DFA", nargs="?", metavar="input_file")
    
    args = parser.parse_args()

    print(args.dfa_file)

    dfa1 = readInputFile(args.dfa_file)
    input_file1 = open(args.input_file)
    inputt = input_file1.readline()
    inputt1 = inputt .replace(' ','')
    actionString = fallback_dfa(dfa1,inputt1)
    print(actionString)
    f = open("task_3_1_result.txt", "w")
    f.write(actionString)
      
    f.close()
    print(pattern)



    
