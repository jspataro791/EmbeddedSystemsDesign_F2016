
#include "tsk_wifly_tx.h"
#include "public_vars.h"
#include "debug.h"

WIFLY_TX_DATA wifly_txData;

char wiflyTransBuffer[MAX_QUEUE_ITEM_SIZE];

void WIFLY_TX_Initialize ( void )
{
   /* set GPIO status to this init */
    sendGPIOStatus(STAT_WIFLY_TX_INIT);
}

void WIFLY_TX_Tasks ( void )
{
   /* set GPIO status to this task */
    sendGPIOStatus(STAT_WIFLY_TX_TASK_ENTER);
    
    /* block until data received on transmit queue */
    int QRcvChk = xQueueReceive( wifly_tx_queue, &wiflyTransBuffer, portMAX_DELAY );

    /* if queue rcv was successful */
    if ( QRcvChk == pdTRUE ) {
        
        /* set GPIO status to transmit buffer rcv good */
        sendGPIOStatus(STAT_WIFLY_TX_GOOD);

        /* take the mutex*/
        xSemaphoreTake(UART_TX_Mutex, portMAX_DELAY);
        
        /* send each byte out on the uart */
        int i = 0;
        while(wiflyTransBuffer[i] != '\0')
        {
           DRV_USART_WriteByte( sysObj.drvUsart0, wiflyTransBuffer[i] );
           i++;
        }
        
        /* send out packet termination character */
        uint8_t pTerm = RVR_MSG_END_BYTE;
        DRV_USART_WriteByte( sysObj.drvUsart0, pTerm );
        
        /* return the mutex */
        xSemaphoreGive(UART_TX_Mutex);
    }
}

 

/*******************************************************************************
 End of File
 */
