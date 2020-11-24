import sys

filename = sys.argv[1]
parserFile = open("parser.py")
parser = parserFile.read()
sys.argv = ["parser.py", filename]

exec(parser)

mvFile = open("MaquinaVirtual.py")
mv = mvFile.read()
exec(mv)