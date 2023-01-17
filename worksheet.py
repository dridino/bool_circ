from modules.open_digraph import *
import inspect

# print(dir(open_digraph))
# print(dir(node))

print(inspect.getsource(open_digraph.__init__) + "\n\n\n" +
      inspect.getsourcefile(open_digraph.__init__))
