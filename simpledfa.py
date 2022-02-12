
class DFA:
    
    def __init__(self,start,preprocessor=None):
        self.preprocessor = preprocessor
        self.transitions = {}
        self.accepting = {}
        self.start = start
    
    
    def transition(self,fromstate,inputs,tostate):
        
        """ Adds a transition from `fromstate` to `tostate`
        for all items in sequence `inputs`. """
        
        for item in inputs:
            self.transitions.setdefault(fromstate,{})[item] = tostate
            
            
    def accept(self,state,token):
        
        """ Registers `state` as accepting and defines its `token` returned. """
        
        self.accepting[state] = token
        
        
    def start(self,state):
        
        """ Registers `state` as the starting state of DFA. """
        
        self.start = state
        
    
    def get_char(self,text,pos):
        
        """ Returns char (or char group via custom preprocessor)
        at position `pos` of `text`, or None if out of bounds. """

        if pos<0 or pos>=len(text): return None

        if self.preprocessor is not None:
            return self.preprocessor(text[pos]) 
        
        return text[pos]


    def scan(self,text):
        
        """ Scans `text` from the beginning until no more transitions exist.
        Returns (token,lexeme) if an accepting state was reached or (None,'') otherwise. """
        
        # initial position on text and initial state
        pos,state = 0,self.start
        
        # memory variables for last seen accepting state
        token,lexeme = None,''

        while True:

            c = self.get_char(text,pos)	# get next char (or char group)

            if state in self.transitions and c in self.transitions[state]:
                state = self.transitions[state][c]	# set new state
                pos += 1	# advance to next char

                # remember if current state is accepting
                if state in self.accepting:
                    token,lexeme = self.accepting[state],text[:pos]

            else:	# no transition found, return last match or None
                return token,lexeme