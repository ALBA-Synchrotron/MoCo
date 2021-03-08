def main():
    import sys
    import logging
    import tango.server
    from .moco import Moco
    args = ['Moco'] + sys.argv[1:]
    fmt = '%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    tango.server.run((Moco,), args=args)


main()
