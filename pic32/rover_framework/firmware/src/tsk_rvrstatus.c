#include "tsk_rvrstatus.h"
#include "debug.h"
#include "public_vars.h"


char rvrStatusBuffer[MAX_QUEUE_ITEM_SIZE];

void RVRStatus_Initialize() {
    sendGPIOStatus(STAT_RVRSTATUS_INIT);
}


void RVRStatus_Tasks() {
    sendGPIOStatus(STAT_RVRSTATUS_TASK_ENTER);

    int QRcvChk = xQueueReceive(valid_data_queue, &rvrStatusBuffer, portMAX_DELAY);

    if (QRcvChk == pdTRUE) {
        /* get the length of the message based on end char*/
        int i = 0;
        for (i; i < MAX_QUEUE_ITEM_SIZE; ++i) {
            if (rvrStatusBuffer[i] == MSG_END_CHAR) {
                break;
            }
        }

        /* get direct */
        int index = 0;
        for (index; index < i; index++) {
            if (rvrStatusBuffer[index] == DIR_CHAR) {
                RVR_CurDirection = rvrStatusBuffer[index + 1];
                break;
            }
        }

        /* get speed */
        index = 0;
        for (index; index < i; index++) {
            if (rvrStatusBuffer[index] == SPEED_CHAR) {
                RVR_CurSpeed = rvrStatusBuffer[index + 1];
                break;
            }
        }

        /* get debug */
        index = 0;
        for (index; index < i; index++) {
            if (rvrStatusBuffer[index] == DEBUG_CHAR) {
                RVR_Dbg = rvrStatusBuffer[index + 1];
                break;
            }
        }

        sendDirStatus((uint8_t) RVR_CurDirection);
        sendSpdStatus((uint8_t) RVR_CurSpeed);
        
        /* echo back speed */
        char spdStat[5] = "SPD";
        spdStat[3] = (char)RVR_CurSpeed;
        spdStat[4] = MSG_END_CHAR;           
        xQueueSend(debug_queue, spdStat, 0);
        
        /* echo back direction */
        char dirStat[5] = "DIR";
        dirStat[3] = (char)RVR_CurDirection;
        dirStat[4] = MSG_END_CHAR;
        xQueueSend(debug_queue, dirStat, 0);
        
        
        
    } else {
        sendGPIOError(ERR_BAD_MQ_RECV);
    }
}
