
#include "serialfsm.h"
#include "serialresponds.h"
#include "debug.h"
#include "system_definitions.h"
#include "public_vars.h"

void
runSerialFrame(unsigned char c) {
    switch (serialData.state) {

            /* STATE: Waiting for start byte*/
        case WAITING_START1:

            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_START2;
                serialData.dataBytesReceived = 0;

            } else if (c == SERIAL_END_BYTE) {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);

            } else {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);
            }
            break;

        case WAITING_START2:

            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_START3;
                serialData.dataBytesReceived = 0;

            } else if (c == SERIAL_END_BYTE) {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);

            } else {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);
            }
            break;

        case WAITING_START3:

            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_DATA_LENGTH;
                serialData.dataBytesReceived = 0;

            } else if (c == SERIAL_END_BYTE) {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);

            } else {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);
            }
            break;

        case WAITING_DATA_LENGTH:

            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_START1;
                serialData.dataBytesReceived = 0;

            } else if (c == SERIAL_END_BYTE) {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);

            } else {

                serialData.dataBytesPerMsg = c;
                serialData.state = WAITING_DATA;
            }
            break;

        case WAITING_DATA:

            /* STATE: Waiting for data byte */
            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_DATA;
                serialData.dataBytesReceived = 0;
                sendGPIOStatus(STAT_SERIAL_NACK);

                vPortFree(serialData.temporaryBytes);

            } else if (c == SERIAL_END_BYTE) {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);


            } else {

                serialData.temporaryBytes[serialData.dataBytesReceived] = c;
                ++serialData.dataBytesReceived;

                if (serialData.dataBytesReceived >= serialData.dataBytesPerMsg) {

                    serialData.state = WAITING_END1;

                }
            }
            break;

        case WAITING_END1:

            /* STATE: Waiting for end byte */
            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);


            } else if (c == SERIAL_END_BYTE) {

                serialData.state = WAITING_END2;

            } else {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);



            }
            break;

        case WAITING_END2:

            /* STATE: Waiting for end byte */
            if (c == SERIAL_START_BYTE) {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);


            } else if (c == SERIAL_END_BYTE) {

                int sStat = xQueueSend(valid_data_queue, serialData.temporaryBytes, 0);

                if (sStat == NULL) {
                    sendGPIOError(ERR_BAD_MQ_SEND);
                }

                serialData.state = WAITING_START1;
                serial0Respond(SERIAL_RESP_ACK);
                sendGPIOStatus(STAT_SERIAL_ACK);


            } else {

                serialData.state = WAITING_START1;
                sendGPIOStatus(STAT_SERIAL_NACK);

            }
            break;
    }


}




