import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("pyneato").version
except Exception:  # pylint: disable=broad-except
    __version__ = "unknown"
