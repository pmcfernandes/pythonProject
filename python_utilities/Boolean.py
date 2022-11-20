
class Boolean:
    @staticmethod
    def parse(s: str) -> bool:
        if s == "0" or s.lower() == "false":
            return False
        return True

