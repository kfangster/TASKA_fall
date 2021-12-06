import time
import sys
import numpy as np

if sys.platform == 'win32': import bluetooth
elif sys.platform == 'linux': import socket
else: raise RuntimeError( 'Bluetooth not supported for this OS:' , sys.platform )


# from . import AbstractBaseOutput

class TASKA():
    """ Python implementation of a TASKA prosthetic hand driver using bluetooth """
    NUM_MOTORS = 6

    @staticmethod
    def checksum( array ):
        chk = 0
        for item in array: chk += item
        return chk & 0xFF

    def __init__( self, port = 3, com = 'COM3', mac = '68:0a:e2:74:67:62' ):
        """
        Constructor

        Parameters
        ----------
        port : str
            The named communication port for the connection (e.g. COM9 on Windows, /dev/ttyACM1 on linux)
        mac : str
            The MAC address of the desired TASKA hand (if None, connect to first one found)

        Returns
        -------
        obj
            A TASKA interface object
        """
        if sys.platform == 'win32':
            self._bt = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        else:
            self._bt = socket.socket( socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM )
        
        self._bt.connect( ( mac, port ) )
        # self._ser = serial.Serial( port = com, baudrate = 4800, timeout = 0.5 )
        
        # self._ser.write( 'ats'.encode( 'utf-8' ) )
        # # time.sleep( 1 )
        # self._ser.write( 'ath'.encode( 'utf-8' ) )

        self._init_bt()
        cmd = 'atd'
        if mac is not None: cmd += ' %s\r\n' % mac.upper()
        else: cmd += '\r\n'
        self._bt.send( cmd.encode( 'utf-8' ) )
        # time.sleep( 2 )

        resp = self._bt.recv( size = 1000 ) # 31 )
        print( resp )

        # define grip and finger IDs
        self._grip_dict = { 'interim' : 0, 'relaxed' : 1, 'open' : 2, 'keyboard' : 3, 'dondoff' : 4,
                            'pointer' : 5, 'key' : 6, 'opposition' : 7, 'handshake' : 8, 'tripod' : 9,
                            'mug_close' : 10, 'pincer' : 11, 'tablet' : 12, 'flex' : 13, 'precision' : 14,
                            'grab_go' : 15, 'mouse' : 16, 'active_index_1' : 17, 'active_index_2' : 18,
                            'custom_1' : 19, 'custom_2' : 20, 'custom_3' : 21, 'custom_4' : 22, 'custom_5' : 23 }
        self._finger_dict = { 'index' : 0, 'middle' : 1, 'ring' : 2, 'pinky' : 3, 'thumb' : 4, 'rotator' : 5 }

        # keep track of movement
        self._last_move = None

        # enable motor encoder access
        for i2c in [ 11, 12, 13 ]:
            for motor in [ 1, 2 ]:
                pkt = [ 35, 77, i2c, 11, motor, 64, 0, 0, 10, 127 ]
                pkt.append( TASKA.checksum( pkt ) )
                pkt = bytes( pkt )

                self._bt.send( pkt )
                resp = self._bt.recv( size = 6 ) # expected response packet: [ 64, 77, I2C, 6, 11, CHKSUM ]

    def __del__(self):
        try:
            pkt = [ 35, 82, 14, 5 ]
            pkt.append( TASKA.checksum( pkt ) )
            pkt = bytes( pkt )
        
            self._bt.send( pkt )
        except AttributeError:
            pass

    def _select_grip_pattern( self, grip ):
        """
        Parameters
        ----------
        grip : str
            ID for the desired grip pattern (defined as key in self._grip_dict)

        Notes
        -----
        The expected response packet: [ 64, 71, 2, 5, CHKSUM ]
        """
        pkt = [ 35, 71, 2, 6, self._grip_dict[grip] ]
        pkt.append( TASKA.checksum( pkt ) )
        pkt = bytes( pkt )

        self._bt.send( pkt )
        resp = self._bt.recv( size = 5 )

    def _move_grip_pattern( self, position ):
        """
        Parameters
        ----------
        position : int [0, 255]
            The proportional value for the current grip where 0 is fully open and 255 is fully closed
        
        Notes
        -----
        The expected response packet: [ 64, 71, 3, 5, CHKSUM ]
        """
        pkt = [ 35, 71, 3, 6, position ]
        pkt.append( TASKA.checksum( pkt ) )
        pkt = bytes( pkt )

        self._bt.send( pkt )
        resp = self._bt.recv( size = 5 )

    def _move_finger_single( self, finger, speed, position, amps = 10, stall = 20 ):
        """
        Parameters
        ----------
        finger : str
            ID for the finger motor to control (defined as key in self._finger_dict)
        speed : int [0, 255]
            The speed for the finger movement (in rps) where 0 is no movement and 255 is as fast as possible
        position : int [0, 255]
            The finger motor position where 0 is fully open and 255 is fully closed
        amps : int
            The maximum current draw of a digit (10s of mA)
        stall : int
            The period of time the digit will maintain a stall position or current draw at the configured amperage (10s of ms)

        Notes
        -----
        The expected response packet: [ 64, 70, FINGER_IDX, 5, CHKSUM ]
        Excessive stall time will potentially burn out the motors of the TASKA hand. Normal values are considered to be <500 ms
        """
        pkt = [ 35, 70, self._finger_dict[finger], 10, speed, position, amps, 0, stall ]
        pkt.append( TASKA.checksum( pkt ) )
        pkt = bytes( pkt )

        self._bt.send( pkt )
        self._bt.recv( size = 5 )

    def _move_finger_group( self, positions, speeds, amps = 20, stall = 20 ):
        #changed amps from 10 to 20 amps
        """
        Parameters
        ----------
        positions : iterable of ints (6,) [0, 255]
            List of finger motor positions where 0 is fully open and 255 is fully closed
        speeds : iterable of ints (6,) [0, 255]
            List of finger motor speeds where 0 is no movement and 255 is as fast as possible
        amps : int
            The maximum current draw of a digit (10s of mA)
        stall : int
            The period of time the digit will maintain a stall position or current draw at the configured amperage (10s of ms)

        Notes
        -----
        The expected response packet: [ 64, 70, 255, 5, CHKSUM ]
        Iterables should be in the following finger order: [Index, Middle, Ring, Little, Thumb, Rotator]
        Excessive stall time will potentially burn out the motors of the TASKA hand. Normal values are considered to be <500 ms
        """
        pkt = [ 35, 70, 255, 20 ]
        for pos in positions:
            pkt.append( pos )
        for spd in speeds:
            pkt.append( spd )

        # pkt.extend( positions )
        # pkt.extend( speeds )
        pkt.extend( [ amps, 0, stall ] )
        pkt.append( TASKA.checksum( pkt ) )
        pkt = bytes( pkt )

        
        print(pkt)

        self._bt.send( pkt )
        resp = self._bt.recv( size = 5 )

    def publish( self, move = None, prop = 1.0, angles = None, speed = 1.0 ):
        """
        Parameters
        ----------
        move : str
            The ID of the desired movement classification
        prop : float [0, 1]
            The proportion to actuate the desired grip where 0 is fully open, 1 is fully closed
        angles : iterable of floats (6,) [0, 1]
            The proportion to actuate each individual finger where 0 is fully open, 1 is fully closed
        speed : iterable of floats (6,) [0,1]
            The speed at which to actuate each individual finger where 0 is no movement, 1 is full speed

        Notes
        -----
        Iterables should be in the following finger order: [Index, Middle, Ring, Little, Thumb, Rotator]
        """
        if move is not None and move in self._grip_dict:
            prop = max( 0.0, min( 1.0, prop ) )
            if move != self._last_move: 
                self._select_grip_pattern( move )
                self._last_move = move
            self._move_grip_pattern( round( 255 * prop ) )
        elif angles is not None:
            self._last_move = None
            # set finger speeds appropriately
            if isinstance( speed, float ):
                speed = max( 0.0, min( 1.0, speed ) )
                speeds = [ speed ] * TASKA.NUM_MOTORS
            # check to make sure dimensions are appropriate
            if len( angles ) == TASKA.NUM_MOTORS and len( speeds ) == TASKA.NUM_MOTORS:
                for i in range( TASKA.NUM_MOTORS ):
                    angles[i] = max( 0.0, min( 1.0, angles[i] ) )
                #need to add this to bring the range from 0 to 255 now
                angles = [ int( 255 * x ) for x in angles ]
                speeds = [ int( 255 * x ) for x in speeds ]

                self._move_finger_group( angles, speeds )

    @property
    def encoders(self):
        """
        Returns
        -------
        numpy.ndarray (6,)
            The encoder positions for each motor

        Notes
        -----
        Encoder positions are raito of total encoder range
        Encoder positions are in the following order: [Index, Middle, Ring, Little, Thumb, Rotator]
        """
        pos = []
        for i2c in [ 11, 12, 13 ]:
            # construct packet
            pkt = [ 35, 109, i2c, 5 ]
            pkt.append( TASKA.checksum( pkt ) )
            pkt = bytes( pkt )

            # send / receive info
            self._bt.send( pkt )
            recv_1 = self._bt.recv( size = 21 )
            recv_2 = self._bt.recv( size = 26 )

            # extract position information
            pos.append( ( 256 * recv_1[8] + recv_1[7] ) / ( 256 * recv_1[14] + recv_1[13] ) )
            pos.append( ( 256 * recv_2[8] + recv_2[7] ) / ( 256 * recv_2[14] + recv_2[13] ) )
        return np.array( pos[ [ 4, 3, 2, 1, 5, 0 ] ] )
        
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
    #changed from getargspec to getfullargspec
    class_init = inspect.getfullargspec( TASKA.__init__ )
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

    taska = TASKA( args.com )
    moves = [ 'interim', 'relaxed', 'open', 'keyboard', 'dondoff',
              'pointer', 'key', 'opposition', 'handshake', 'tripod',
              'mug_close', 'pincer', 'tablet', 'flex', 'precision',
              'grab_go', 'mouse', 'active_index_1', 'active_index_2',
              'custom_1', 'custom_2', 'custom_3', 'custom_4', 'custom_5' ]
    
    print( '------------ Movement Commands ------------' )
    print( '| 00  -----  INTERIM                      |' )
    print( '| 01  -----  RELAXED                      |' )
    print( '| 02  -----  OPEN PALM                    |' )
    print( '| 03  -----  KEYBOARD                     |' )
    print( '| 04  -----  DON DOFF                     |' )
    print( '| 05  -----  POINTER                      |' )
    print( '| 06  -----  KEY                          |' )
    print( '| 07  -----  OPPOSITION                   |' )
    print( '| 08  -----  HANDSHAKE                    |' )
    print( '| 09  -----  TRIPOD                       |' )
    print( '| 10  -----  MUG CLOSE ONLY               |' )
    print( '| 11  -----  PINCER                       |' )
    print( '| 12  -----  ADDUCTION TABLET             |' )
    print( '| 13  -----  FLEX TOOL                    |' )
    print( '| 14  -----  OPPOSITION PRECISION         |' )
    print( '| 15  -----  GRAB N GO                    |' )
    print( '| 16  -----  MOUSE                        |' )
    print( '| 17  -----  ACTIVE INDEX                 |' )
    print( '| 18  -----  ACTIVE INDEX 2               |' )
    print( '| 19  -----  CUSTOM 1                     |' )
    print( '| 20  -----  CUSTOM 2                     |' )
    print( '| 21  -----  CUSTOM 3                     |' )
    print( '| 22  -----  CUSTOM 4                     |' )
    print( '| 23  -----  CUSTOM 5                     |' )
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
                    taska.publish( moves[ idx ], prop = 1.0 )
            except ValueError:
                pass
    print( 'Bye-bye!' )
