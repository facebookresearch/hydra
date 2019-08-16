import re


class Utils:
    @staticmethod
    def get_valid_filename(s):
        s = str(s).strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", s)
