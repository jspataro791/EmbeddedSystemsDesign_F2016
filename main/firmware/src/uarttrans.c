
/* This task watches for data in the UART0 transmit queue 
    and sends it if available */

#include "uarttrans.h"
#define UART0_TRANS_QUEUE_SIZE 100
#define UART0_TRANS_TASK_DELAY_MS 0

/* uart 0 transmit queue definition */
QueueHandle_t uart0TransQueue;

/* buffer for transmit queue to write to */
char uart0ByteTransBuffer;

/* init */
void UARTTRANS_Initialize( void ) {
    
    /* set GPIO status to this init */
    sendGPIOStatus(STAT_TASK_TX_INIT);
    
    /*init uart0 transmit message queue*/
    uart0TransQueue = xQueueCreate( UART0_TRANS_QUEUE_SIZE, sizeof (char ) );
    
    /* halt if msg queue cannot be created, fatal */
    if(uart0TransQueue == 0) {
        sendGPIOError(ERR_BAD_MQ_CREATE);
    }
}

/* main task */
void UARTTRANS_Tasks( void ) {
    
    /* set GPIO status to this task */
    sendGPIOStatus(STAT_TASK_TX);
    
    /* block until data received on transmit queue */
    int QRcvChk = xQueueReceive( uart0TransQueue, &uart0ByteTransBuffer, portMAX_DELAY );

    /* if queue rcv was successful */
    if ( QRcvChk == pdTRUE ) {

        /* send the byte out on the uart */
        DRV_USART_WriteByte( sysObj.drvUsart0, uart0ByteTransBuffer );
    }

    /* delay this task */
    vTaskDelay( UART0_TRANS_TASK_DELAY_MS );
}



/*******************************************************************************
 End of File
 */
