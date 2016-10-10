
#include "serialfsm.h"
#include "serialresponds.h"
#include "system_definitions.h"

void
runSerialFrame(unsigned char c) {
    switch (serialData.state) {

        /* STATE: Waiting for start byte*/
        case WAITING_START:

            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_DATA;
                serialData.dataBytesReceived = 0;

            } else if (c == SERIAL_END_BYTE) {

                serialData.state = WAITING_START;
                sendGPIOStatus(STAT_SERIAL_NACK);

            } else {

                serialData.state = WAITING_START;
                sendGPIOStatus(STAT_SERIAL_NACK);
            }
            break;

        case WAITING_DATA:
            
            /* STATE: Waiting for data byte */
            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_DATA;
                serialData.dataBytesReceived = 0;
                sendGPIOStatus(STAT_SERIAL_NACK);


            } else if (c == SERIAL_END_BYTE) {

                serialData.state = WAITING_START;
                sendGPIOStatus(STAT_SERIAL_NACK);

            } else {

                serialData.temporaryBytes[serialData.dataBytesReceived] = c;
                ++serialData.dataBytesReceived;

                if (serialData.dataBytesReceived >= SERIAL_DATA_BYTES_PER_MESSAGE) {

                    serialData.state = WAITING_END;

                }
            }
            break;

        case WAITING_END:
            
            /* STATE: Wiaiting for end byte */
            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_START;
                sendGPIOStatus(STAT_SERIAL_NACK);

            } else if (c == SERIAL_END_BYTE) {
                // write elements 0 through appData.dataBytesReceived from
                // appData.temporaryBytes to queue.

                serialData.state = WAITING_START;
                serial0Respond(SERIAL_RESP_ACK);
                sendGPIOStatus(STAT_SERIAL_ACK);

            } else {

                serialData.state = WAITING_START;
                sendGPIOStatus(STAT_SERIAL_NACK);

            }
            break;

    }


}



