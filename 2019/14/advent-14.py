from collections import defaultdict

def ceil(a,b):
    return -(-a // b)

class Reaction:
    def __init__(self,desc:str):
        def typsep(s:str):
            sep = s.split()
            n = int(sep[0])
            s = sep[1]
            return (n, s)
        
        splitline = desc.split('=>')
        inp = splitline[0]
        self.input = [typsep(x) for x in inp.split(',')]
        out = splitline[1]
        output = typsep(out)
        self.increment = output[0]
        self.output = output[1]
    
    def __repr__(self):
        return f"Reaction: {self.output} from {self.input}"

class ReactionChain:
    def __init__(self,filename:str):
        all_reactions = []
        with open(filename) as f:
            content = f.readlines()
        for line in content:
            r = Reaction(line)
            all_reactions.append(r)
        self.reactions = {x.output:(x.increment,x.input) for x in all_reactions}
        self.pantry = defaultdict(int)

    def how_much(self,ingredient,n:int=1):
        recipe = self.reactions[ingredient]
        already_got = self.pantry.pop(ingredient, 0)
        need = n - already_got
        batch = (ceil(need,recipe[0]),recipe)
        #batch_nos  = [(ceil(n-already_got,x[0]), x) for x in recipes]
        #if len(batch_nos) > 1:
        #    batches = min(batch_nos)
        #else:
        times = batch[0]
        increment = batch[1][0]
        amounts = batch[1][1]
        requirements = [((x*times),y) for (x,y) in amounts]
        leftovers = (((times*increment) % n), ingredient)
        self.pantry[leftovers[1]] = leftovers[0]
        return requirements, leftovers

fu = ReactionChain("test.txt")
print(fu.how_much('A',7))
print(fu.how_much('E',1))
print()
print(fu.pantry)