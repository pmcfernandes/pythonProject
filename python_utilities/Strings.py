class Strings:
    @staticmethod
    def ensureNotEndsWith(s: str, delimiter: str = ",") -> str:
        if s.endswith(delimiter):
            return s[:-len(delimiter)]
        else:
            return s

    @staticmethod
    def trim(s: str) -> str:
        return s.strip()

    @staticmethod
    def trimStart(s: str) -> str:
        return s.lstrip()

    @staticmethod
    def trimEnd(s: str) -> str:
        return s.rstrip()

    @staticmethod
    def slugify(s: str):
        return s.replace(r'\W+', '-', regex=True)
    