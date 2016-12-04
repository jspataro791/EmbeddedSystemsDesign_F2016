
#include "tsk_lfa_decision.h"
#include "public_vars.h"
#include "rvr_config.h"

void LFA_DECISION_Initialize() {

}

char lfaDecBuffer;

char lfa_recv()
{
    int QRcvChk = xQueueReceive(lfa_rx_queue, &lfaDecBuffer, portMAX_DELAY);

    if (QRcvChk == pdTRUE) {

        return lfaDecBuffer;

    } else {
        sendGPIOError(ERR_BAD_MQ_RECV);
    }
}

void LFA_DECISION_Tasks() {
    switch (LFA_DECISION_DATA.decState) {

        

    }
}
