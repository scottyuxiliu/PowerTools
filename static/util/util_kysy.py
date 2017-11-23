import KysyEnvironment, Kysy

class util_kysy(object):
    """
    Kysy related utility functions:

    kysy_init
    kysy_connect
    """
    def __init__(self):
        try:
            Kysy.StubPlatform.create
        except RuntimeError as e:
            print("Exception: %s\n" % str(e))
    def kysy_connect(self,connect_type=None,ip=None,username=None,password=None,platform=None,wombat=None,hdt=None,sim=None):
        """
        arguments:
        connect_type=None
        ip=None
        username=None
        password=None
        platform=None
        wombat=None
        hdt=None
        sim=None

        returns:
        wombat
        platform
        """
        if(connect_type is None):
            parser = argparse.ArgumentParser(description='Sample parser of args to support different target access methods')
            parser.add_argument('--yaap', action="store", dest="yaap", help='Wombat IP address')
            parser.add_argument('--hdt', action="store", dest="hdt", help='Wombat IP address (deprecated)')
            parser.add_argument('--sim', nargs='?', const='sim', default='default')
        
            args = parser.parse_args()

            # Parse out the args and construct a platform instance
            if (args.yaap != None):
                wombat = Kysy.Wombat.create(args.yaap)
                platform = wombat.platform()
                #enter debug mode before the sample test
                ##wombat.cpuDebug().requestDebug()
            elif (args.hdt != None):
              hdt = Kysy.HDTYaapDevice.create(args.hdt)
              platform = hdt.platform()
              # Enter debug mode before the sample test
              #hdt.cpuDebug().requestDebug()
            elif (args.sim != None and args.sim == 'sim'):
              # We connect to an existing SimNow session. Hence passing in an empty string.
              sim = Kysy.SimNowDevice.create('')
              platform = sim.platform()
              #sim.cpuDebug().requestDebug()
            else:
              # Construct a native platform
              platform = Kysy.Platform.create()
        else:
            if(connect_type == 'yaap'):
                wombat = Kysy.Wombat.create(ip,username,password)
                platform = wombat.platform()
                return wombat,platform

