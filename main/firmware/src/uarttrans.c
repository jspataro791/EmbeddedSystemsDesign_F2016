
/* This task watches for data in the UART0 transmit queue 
    and sends it if available */

#include "uarttrans.h"
#define UART0_TRANS_QUEUE_SIZE 10
#define UART0_TRANS_TASK_DELAY_MS 10

/* uart 0 transmit queue definition */
QueueHandle_t uart0TransQueue;

char uart0ByteTransBuffer;

/* init */
void UARTTRANS_Initialize ( void )
{
    /*init uart0 transmit message queue*/
    uart0TransQueue = xQueueCreate( UART0_TRANS_QUEUE_SIZE, sizeof(char) );
}

/* main task */
void UARTTRANS_Tasks ( void )
{
    /* block until data received on transmit queue */
    int QRcvChk = xQueueReceive(uart0TransQueue, &uart0ByteTransBuffer, portMAX_DELAY);
    
    /* if queue rcv was successful */
    if(QRcvChk == pdTRUE) {
        
        /* send the byte out on the uart */
        DRV_USART_WriteByte(sysObj.drvUsart0, uart0ByteTransBuffer);
    }
    
    /* delay this task */
    vTaskDelay(UART0_TRANS_TASK_DELAY_MS);
}

 

/*******************************************************************************
 End of File
 */
