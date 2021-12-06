import sys

import serial
from serial import Serial
#from . import AbstractBaseOutput

class ActiveWristserial():
    """Implementation of controller and active wrist movements"""
    def __init__( self, com = 'COM6', mac = 'ec:fe:7e:1d:8e:a1', elbow = False ): #specificed MAC address for controller
        """
        Constructor

        Parameters
        ----------
        com : str
            The COM port of the controller board (found in control panel)
        mac : str
            The MAC address of the controller board for the TASKA
        elbow : bool
            True if a powered elbow is connected, False else

        Returns
        -------
        obj
            A TASKA object
        """
        self._elbow = elbow

        self._ser = serial.Serial(port = com, baudrate = 9600, timeout = 0.5 )

        # cmd = 'atd'
        # if mac is not None: cmd += ' %s\r\n' % mac.upper()
        # else: cmd += '\r\n'
        # self._ser.write( cmd.encode( 'utf-8' ) )

        resp = self._ser.read( size = 1000 ) # 31 )
        print( resp )

        self._ser.write( b'\xff\x02\x9e\x9f' )   # stop movement command
        self._ser.write( b'\xff\x02\x9b\x9c' )   # clear movement command
        self._move_dict = { 'rest'         : b'\xff\x02\x9b\x9c',
                            'pronate'      : b'\xff\x04\x9c\x24\x01\xc4',
                            'supinate'     : b'\xff\x04\x9c\x23\x01\xc3',
                            'elbow_flex'   : b'\xff\x04\x9c\x2d\x01\xcd',
                            'elbow_extend' : b'\xff\x04\x9c\x2e\x01\xce'}
        self._last_move = None
    
    def __del__( self ):
        """
        Destructor

        Stops the ActiveWrist from any movements its currently doing and closes communication.
        """
        try:
            self._ser.write( b'\xff\x02\x9e\x9f' )   # stop movement command
            self._ser.write( b'\xff\x02\x9b\x9c' )   # clear movement command
            self._ser.close()                       # close communication
        except (AttributeError, OSError):
            # did not open the bluetooth communication
            pass
    
    def _init_bt( self ):
        """
        Initializes the bluetooth connection and registers all available grips
        """

        self._ser.write( b'\xff\x06\x80\x00\x00\x00\x00\x85' )                           # connect
        self._ser.write( b'\xff\x02\x00\x01' )
        self._ser.write( b'\xff\x02\x83\x84' )
        self._ser.write( b'\xff\x02\x00\x01' )

        if not self._elbow:
            self._ser.write( b'\xff\x16\x93\x23\xff\x09\x00\x00\x00\x01\x01\x46\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x1b' )    # supinate
            self._ser.write( b'\xff\x16\x93\x24\xff\x09\x00\x00\x00\x02\x01\x46\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x1d' )    # pronate
        else:
            self._ser.write( b'\xff\x16\x93\x23\xff\x03\x00\x00\x00\xff\x01\x46\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x13' )    # supinate
            self._ser.write( b'\xff\x16\x93\x24\xff\x04\x00\x00\x00\xff\x01\x46\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x15' )    # pronate
            self._ser.write( b'\xff\x16\x93\x2d\xff\x05\x00\x00\x00\xff\x01\x46\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x1f' )    # elbow bend
            self._ser.write( b'\xff\x16\x93\x2e\xff\x06\x00\x00\x00\xff\x01\x46\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x21' )    # elbow extend

    def _send_movement_command( self, move ):
        """
        Send a movement command to the ActiveWrist

        Parameters
        ----------
        move : str
            Name of the desired movement class

        Raises
        ------
        RuntimeError
            Invalid movement class name is given
        """
        if move in self._move_dict:
            self._ser.write( b'\xff\x02\x9e\x9f' )        # stop last movement command
            self._ser.write( self._move_dict['rest'] )    # clear last movement command
            self._ser.write( self._move_dict[ move ] )    # send current movement command
            self._ser.write( self._move_dict[ move ] )    # must send active movement commands twice
        else:
            raise RuntimeError( 'Invalid movement class for the Bebionic3: ', move )

    def publish( self, msg ):
        """
        Publish output to the ActiveWrist

        Parameters
        ----------
        msg : str
            The name of the output movement class to send

        Notes
        -----
        If the ActiveWrist is already doing the desired movement class, no command is sent to save on bandwidth
        """
        if msg is not self._last_move:
            self._send_movement_command( msg )
            self._last_move = msg    
        

if __name__ == '__main__':
    import sys
    import inspect
    import argparse

    # helper function for booleans
    def str2bool( v ):
        if v.lower() in [ 'yes', 'true', 't', 'y', '1' ]: return True
        elif v.lower() in [ 'no', 'false', 'n', 'f', '0' ]: return False
        else: raise argparse.ArgumentTypeError( 'Boolean value expected!' )

    # parse commandline entries
    class_init = inspect.getfullargspec( ActiveWristserial.__init__ )
    arglist = class_init.args[1:]   # first item is always self
    defaults = class_init.defaults
    parser = argparse.ArgumentParser()
    for arg in range( 0, len( arglist ) ):
        try: tgt_type = type( defaults[ arg ][ 0 ] )
        except: tgt_type = type( defaults[ arg ] )
        if tgt_type is bool:
            parser.add_argument( '--' + arglist[ arg ], 
                             type = str2bool, nargs = '?',
                             action = 'store', dest = arglist[ arg ],
                             default = defaults[ arg ] )
        else:
            parser.add_argument( '--' + arglist[ arg ], 
                                type = tgt_type, nargs = '+',
                                action = 'store', dest = arglist[ arg ],
                                default = defaults[ arg ] )
    args = parser.parse_args()
    for arg in range( 0, len( arglist ) ):
        attr = getattr( args, arglist[ arg ] )
        if isinstance( attr, list ) and not isinstance( defaults[ arg ], list ):
            setattr( args, arglist[ arg ], attr[ 0 ]  )

    activewristmov = ActiveWristserial( args.mac, args.elbow )
    moves = ['rest','pronate', 'supinate', 'elbow_flex', 'elbow_extend']
    
    print( '------------ Movement Commands ------------' )
    print( '| 00  -----  NOGRIP                       |' )
    print( '| 01  -----  PRONATE                      |' )
    print( '| 02  -----  SUPINATE                     |' )
    print( '| 03  -----  ELBOW FLEXION                |' )
    print( '| 04  -----  ELBOW EXTENSION              |' )     
    print( '-------------------------------------------' )
    print( '| Press [Q] to quit!                      |' )
    print( '-------------------------------------------' )

    done = False  
    while not done:
        cmd = input( 'Command: ' )
        if cmd.lower() == 'q':
            done = True
        else:
            try:
                idx = int( cmd )
                if idx in range( 0, len( moves ) ):
                    activewristmov.publish( moves[ idx ] )
            except ValueError:
                pass
    print( 'Bye-bye!' )
