
class Boolean:
    @staticmethod
    def parse(s: str) -> bool:
        return False if s == "0" or s.lower() == "false" else True
