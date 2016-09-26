/* If enabled, this task loops back all serial data in UART0 */

#include "uartloopback.h"
#define UART0_LOOPBACK_ENABLE pdTRUE
#define UART0_LOOPBACK_TASK_DELAY_MS 10

/* get external message queues */
extern QueueHandle_t uart0TransQueue;
extern QueueHandle_t uart0RcvQueue;

char loopbackByteBuffer;

void UARTLOOPBACK_Initialize(void) {


}

void UARTLOOPBACK_Tasks(void) {
    
    if (UART0_LOOPBACK_ENABLE) {
        
        /* wait for something to enter the UART0 rcv message queue */
        int QRcvChk = xQueueReceive(uart0RcvQueue, &loopbackByteBuffer, portMAX_DELAY);

        /* if we have a good message queue receive */
        if (QRcvChk == pdTRUE) {

            /* put the data into the UART0 transmit queue */
            xQueueSend(uart0TransQueue, &loopbackByteBuffer, 0);
        }
    }

    /* delay this task */
    vTaskDelay(UART0_LOOPBACK_TASK_DELAY_MS);
}



/*******************************************************************************
 End of File
 */