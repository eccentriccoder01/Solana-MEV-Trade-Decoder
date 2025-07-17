class MEVAnalyzerError(Exception):
    """Base exception for MEV analyzer"""
    pass

class APIError(MEVAnalyzerError):
    """API-related errors"""
    pass

class ValidationError(MEVAnalyzerError):
    """Data validation errors"""
    pass
