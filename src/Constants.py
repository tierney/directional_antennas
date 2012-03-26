# Constants to be used by directional experiment files
# Matt Tierney

NUMTHREADS = 10
NODENUMBERS = range(1,25)

NODESTOEXCLUDE = [13, 17, 22, 23]
for node in NODESTOEXCLUDE:
    NODENUMBERS.remove(node)

OKAYNODES = []
