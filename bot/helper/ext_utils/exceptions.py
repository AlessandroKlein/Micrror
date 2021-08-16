class DirectDownloadLinkException(Exception):
    """No se encontró un método para extraer el enlace de descarga directa del enlace http"""
    pass


class NotSupportedExtractionArchive(Exception):
    """El formato de archivo que se está intentando extraer no es compatible"""
    pass
