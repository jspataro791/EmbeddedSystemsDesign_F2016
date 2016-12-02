#include "tsk_debug.h"
#include "debug.h"
#include "public_vars.h"

/* this task basically reports info about the rover every second or so */

char debugTransBuffer[MAX_QUEUE_ITEM_SIZE];

void DEBUG_Initialize() {
    /* send task initialize debug status */
    sendGPIOStatus(STAT_DEBUG_INIT);
}

void DEBUG_Tasks() {
    /* send task enter debug status */
    sendGPIOStatus(STAT_DEBUG_TASK_ENTER);

    /* block until data received on transmit queue */
    int QRcvChk = xQueueReceive(debug_queue, &debugTransBuffer, portMAX_DELAY);

    /* if queue rcv was successful */
    if (RVR_Dbg == 1) {
        if (QRcvChk == pdTRUE) {


            /* take the semaphore */
            xSemaphoreTake(UART_TX_Mutex, portMAX_DELAY);

            /* send each byte out on the uart */
            int i = 0;
            while (debugTransBuffer[i] != MSG_END_CHAR) {
                DRV_USART_WriteByte(sysObj.drvUsart0, debugTransBuffer[i]);
                i++;
            }

            /* send out packet termination character */
            uint8_t pTerm = RVR_MSG_END_BYTE;
            DRV_USART_WriteByte(sysObj.drvUsart0, pTerm);

            /* return the semaphore*/
            xSemaphoreGive(UART_TX_Mutex);

        } else {
            sendGPIOError(ERR_BAD_MQ_RECV);
        }
    }


    // wait a second
    vTaskDelay(100);
}
