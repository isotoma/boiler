from twisted.application.service import ServiceMaker

YaybuServer = ServiceMaker(
    "yaybuserver",
    "yaybu.server.main",
    "Yaybu Server",
    "yaybuserver"
    )

