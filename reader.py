
class Reader():
    

    def readFile(self, fileName):
        f = open(fileName,"r")
        content = f.readlines()
        f.close()
        return content

    def readAF(self, fileName: str):
        content = self.readFile(fileName)
        matriz = []
        for line in content:
            line = line.strip('\n')
            matriz.append(line.split(sep='|'))
        return matriz


    def readGr():
        pass

