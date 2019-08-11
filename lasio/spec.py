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


class MandatorySections(Rule):
    @staticmethod
    def check(las_file):
        return VersionSectionExists.check(las_file) and \
               WellSectionExists.check(las_file) and \
               CurvesSectionExists.check(las_file) and \
               AsciiSectionExists.check(las_file)


class MandatoryLinesInVersionSection(Rule):
    @staticmethod
    def check(las_file):
        if "Version" in las_file.sections:
            return "VERS" in las_file.version and "WRAP" in las_file.version
        return False
