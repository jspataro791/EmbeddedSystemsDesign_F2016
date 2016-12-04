
#include "tsk_lfa_decision.h"
#include "public_vars.h"
#include "rvr_config.h"

void LFA_DECISION_Initialize() {

}

char lfaDecBuffer;

void LFA_DECISION_Tasks() {
    switch (LFA_DECISION_DATA.decState) {

        case RECEIVING:
            
            int QRcvChk = xQueueReceive(lfa_rx_queue, &lfaDecBuffer, portMAX_DELAY);

            if (QRcvChk == pdTRUE) {

                LFA_DECISION_DATA.decState = PROCESSING;
                break;
                
            } else {
                sendGPIOError(ERR_BAD_MQ_RECV);
                break;
            }
            
        case PROCESSING:
            
            if(lfaDecBuffer && LFA_STRAIGHT)
            {
                /* straight */
                xQueueSend(motor_ctrl_queue, MOTOR_CTRL_STRAIGHT, 0);
                LFA_DECISION_DATA.decState = RECEIVING;
            }
            else if (lfaDecBuffer && LFA_TWOWAY)
            {
                /* two way intersection */
            }
            else if (lfaDecBuffer && LFA_LEFT)
            {
                /* left intersection */
            }
            else if (lfaDecBuffer && LFA_RIGHT)
            {
                /* right intersection */
            }

    }
}
