class Strings:
    @staticmethod
    def ensureNotEndsWith(s, delimiter=","):
        if s.endswith(delimiter):
            return s[:-len(delimiter)]
        else:
            return s

    @staticmethod
    def trim(s):
        return s.strip()

    @staticmethod
    def trimStart(s):
        return s.lstrip()

    @staticmethod
    def trimEnd(s):
        return s.rstrip()

