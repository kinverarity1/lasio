class Rule:
    pass


class WellSectionExists(Rule):
    @staticmethod
    def check(las_file):
        return "Well" in las_file.sections


class VersionSectionExists(Rule):
    @staticmethod
    def check(las_file):
        return "Version" in las_file.sections


class CurvesSectionExists(Rule):
    @staticmethod
    def check(las_file):
        return "Curves" in las_file.sections


class AsciiSectionExists(Rule):
    @staticmethod
    def check(las_file):
        if "Curves" in las_file.sections:
            for curve in las_file.curves:
                if len(curve.data) == 0:
                    return False
            return True
        else:
            return False
