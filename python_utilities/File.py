import shutil
from enum import Enum
from shutil import copytree
import os


class FileWrite(Enum):
    Write = 0
    Append = 1


class File:

    @staticmethod
    def readFile(fileName: str) -> str:
        f = open(fileName, "r")
        return f.read()

    @staticmethod
    def writeFile(fileName: str, content: str, write=FileWrite.Write):
        if write == FileWrite.Write:
            f = open(fileName, "w")
        else:
            f = open(fileName, "a")

        f.write(content)
        f.close()
        pass

    @staticmethod
    def delete(fileName: str) -> bool:
        if os.path.exists(fileName):
            os.remove(fileName)
            return True
        return False

    @staticmethod
    def createDirectory(dirName: str):
        os.mkdir(dirName, exist_ok=True)
        pass

    @staticmethod
    def copyDir(srcDir: str, destDir: str):
        shutil.copytree(srcDir, destDir)
        pass

    @staticmethod
    def joinPaths(names) -> str:
        path = ""
        for s in names:
            path = os.path.join(path, s)
        return path
