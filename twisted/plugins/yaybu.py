from twisted.application.service import ServiceMaker

YaybuServer = ServiceMaker(
    "yaybuserver",
    "yaybuserver.main",
    "Yaybu Server",
    "yaybuserver"
    )

