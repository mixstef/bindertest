class NFA:
    
    def __init__(self,start,preprocessor=None,verbose=False):
        self.preprocessor = preprocessor
        self.verbose = verbose
        self.transitions = {}
        self.accepting = {}
        self.start = start
        
        self.acceptset = set()	# set containing all states declared as accepting
        
        self.rev_e_closure = {}	# keyed by a state, value holds set of all states that have this state in their e-closures
        
        self.fwd_e_closure = {} # keyed by a state, value is as set of all states in e-closure of this state
    
    
    def transition(self,fromstate,inp,tostate):
        
        """ Adds a transition from `fromstate` to `tostate`
        for `inp` (if a string) or for all items in sequence `inp`
        (if a sequence). An `inp` equal to None adds an epsilon transition. """
        
        if inp is None:
            self.register_e_transition(fromstate,tostate)
        
        elif isinstance(inp,str):
            self.register_transition(fromstate,inp,tostate)
        
        else:
            for item in inp:
            	self.register_transition(fromstate,item,tostate)
            
            
    def accept(self,state,token,priority=0):
        
        """ Registers `state` as accepting and defines its `token` returned.
        An optional `priority` number can be assigned to the `state`. """

        # state and all states that have state in their e-closures (until now)
        states = set([state]) | self.rev_e_closure.get(state,set())
        for st in states:
            self.accepting[st] = (priority,token)
            self.acceptset.add(st)

    
    def register_transition(self,fromstate,inp,tostate):
        """ Adds a normal transition from `fromstate` to `tostate`
        on a non-epsilon input `inp` """
        
        # fromstate and all states that have fromstate in their e-closures
        states = set([fromstate]) | self.rev_e_closure.get(fromstate,set()) 
        
        for state in states:
            if state not in self.transitions:
                self.transitions[state] = {inp:set([tostate])}
            else:
                self.transitions[state].setdefault(inp,set()).add(tostate)


    def register_e_transition(self,fromstate,tostate):
        """ Adds an epsilon transition from `fromstate` to `tostate` """
        
        # fromstate and all states that have fromstate in their e-closures
        frm_states = set([fromstate]) | self.rev_e_closure.get(fromstate,set())
        
        # tostate and all states that are it its e-closure
        to_states = set([tostate]) | self.fwd_e_closure.get(tostate,set())
        
        # add each state of to_states to the e-closure of each state of frm_states
        for state in frm_states:
            self.fwd_e_closure.setdefault(state,set()).update(to_states)
        for state in to_states:
            self.rev_e_closure.setdefault(state,set()).update(frm_states)

        # add normal transitions of tostate (and its e-closure's) to all states in frm_states
        if tostate in self.transitions:
            for state in frm_states:
                if state not in self.transitions:
                    self.transitions[state] = dict(self.transitions[tostate])
                else:
                    for inp,stateset in self.transitions[tostate].items(): 
                        self.transitions[state].setdefault(inp,set()).update(stateset)
        
        # if tostate is an accepting state, mark all states in frm_states as accepting too
        if tostate in self.accepting:
        	priority,token = self.accepting[tostate]
        	for st in frm_states:
                    self.accepting[st] = (priority,token)
                    self.acceptset.add(st)


    def get_char(self,text,pos):
        
        """ Returns char (or char group via custom preprocessor)
        at position `pos` of `text`, or None if out of bounds. """

        if pos<0 or pos>=len(text): return None

        if self.preprocessor is not None:
            return self.preprocessor(text[pos]) 
        
        return text[pos]


    def scan(self,text,startpos=0):
        
        """ Scans `text` from the starting position `startpos` until no more transitions exist.
        Returns (token,lexeme) if an accepting state was reached or (None,'') otherwise.
        In case of multiple accepting states, returns the one with greater priority """
        
        # initial position on text
        pos = startpos
        
        # initial set of states
        stateset = set([self.start]) | self.fwd_e_closure.get(self.start,set())
        
        if self.verbose:
            print('Starting state set is {}'.format(self.stateset_fmt(stateset)))
        
        # memory variable for last seen accepting set of states (and position in text after reaching them)
        lastacceptset,lastposafter = set(),0

        while True:

            c = self.get_char(text,pos)	# get next char (or char group)
            
            # compute the next set of states after transition (if any)
            nextset = set()
            for state in stateset:
                if state in self.transitions and c in self.transitions[state]:
                    nextset.update(self.transitions[state][c])
                    
            if nextset:	# if nextset not empty
            
                if self.verbose:
                    print('Input is "{}", moving to new state set {}'.format(c,self.stateset_fmt(nextset)))
            
                stateset = nextset
                pos += 1
                # store any accepting state in memory
                accepts = self.acceptset & stateset	# intersection of 'all accept states' with current states
                if accepts:	# there are accepting states after this step, store them (else keep older)
                    lastacceptset = accepts
                    lastposafter = pos	# store also position after reaching these states

            else:	# no transition found, return last match (prioritized) or None
            
                if self.verbose:
                    print('No more transition possible or end of input')
            
                if lastacceptset:	# if lastaccept set is not empty
                    lexeme = text[startpos:lastposafter]	# text matched
                    # sort accepting states by priority
                    sl = []
                    for state in lastacceptset:
                        sl.append(self.accepting[state])
                    sl.sort(key=lambda x:(-x[0],x[1]))	# "descending" priority, lexicographically state
                    
                    if self.verbose:
                        print('Accept state(s) encountered: {}, returning {}'.format(self.stateset_fmt(lastacceptset),sl[0][1]))
                    
                    return sl[0][1],lexeme
                    
                else:
                
                    if self.verbose:
                        print("No accept state encountered, returning ERROR")
                
                    return None,''
                    
                    
    def stateset_fmt(self,stateset):
    
        """ Utility function for pretty-printing of `stateset` """
        
        l = list(stateset)
        l.sort()
        return '{'+', '.join(l)+'}'
