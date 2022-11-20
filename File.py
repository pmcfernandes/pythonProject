from enum import Enum
import os


class FileWrite(Enum):
    Write = 0
    Append = 1


class File:

    @staticmethod
    def readFile(fileName):
        f = open(fileName, "r")
        return f.read()

    @staticmethod
    def writeFile(fileName, content, write=FileWrite.Write):
        if write == FileWrite.Write:
            f = open(fileName, "w")
        else:
            f = open(fileName, "a")

        f.write(content)
        f.close()
        pass

    @staticmethod
    def delete(fileName):
        if os.path.exists(fileName):
            os.remove(fileName)
            return True
        return False

    @staticmethod
    def createDirectory(dirName):
        os.mkdir(dirName)
        pass

    @staticmethod
    def joinPaths(names):
        path = ""
        for s in names:
            path = os.path.join(path, s)
        return path




