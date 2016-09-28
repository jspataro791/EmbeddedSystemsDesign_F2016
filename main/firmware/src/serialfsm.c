
#include "serialfsm.h"
#include "serialresponds.h"

void
runSerialFrame( unsigned char c ) {
    switch ( serialData.state ) {

        case WAITING_START:

            if ( c == SERIAL_START_BYTE ) {

                serialData.state = WAITING_DATA;
                serialData.dataBytesReceived = 0;

            } else if ( c == SERIAL_END_BYTE ) {

                serialData.state = WAITING_START;

            } else {

                serialData.state = WAITING_START;
            }
            break;

        case WAITING_DATA:
            if ( c == SERIAL_START_BYTE ) {

                serialData.state = WAITING_START;

            } else if ( c == SERIAL_END_BYTE ) {

                serialData.state = WAITING_START;

            } else {

                serialData.temporaryBytes[serialData.dataBytesReceived] = c;
                ++serialData.dataBytesReceived;

                if ( serialData.dataBytesReceived >= SERIAL_DATA_BYTES_PER_MESSAGE ) {

                    serialData.state = WAITING_END;

                }
            }
            break;

        case WAITING_END:
            if ( c == SERIAL_START_BYTE ) {

                serialData.state = WAITING_START;

            } else if ( c == SERIAL_END_BYTE ) {
                // write elements 0 through appData.dataBytesReceived from
                // appData.temporaryBytes to queue.

                serialData.state = WAITING_START;
                serial0Respond( SERIAL_RESP_ACK );

            } else {

                serialData.state = WAITING_START;

            }
            break;

    }


}



