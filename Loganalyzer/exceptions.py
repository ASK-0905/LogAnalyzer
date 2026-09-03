class LogAnalyzerError(Exception):
    pass


class LogFileNotFoundError(LogAnalyzerError):
    pass


class MalformedLineError(LogAnalyzerError):
    pass


class InvalidLogLevelError(LogAnalyzerError):
    pass


class InvalidDateFormatError(LogAnalyzerError):
    pass