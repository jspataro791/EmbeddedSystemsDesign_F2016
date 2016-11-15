
#include "tsk_wifly_rx.h"
#include "serialfsm.h"
#include "debug.h"
#include "public_vars.h"

WIFLY_RX_DATA wifly_rxData;

char wiflyRcvByteBuffer;

char testMsg[MAX_QUEUE_ITEM_SIZE];

void WIFLY_RX_Initialize ( void )
{
   /* set GPIO status */
   sendGPIOStatus(STAT_WIFLY_RX_INIT); 
   
   strcpy(testMsg, "This is a test!");
    
   /* reset serial state machine*/
   serialData.state = WAITING_START;
}

void WIFLY_RX_Tasks ( void )
{
    /* set GPIO status to this task */
    sendGPIOStatus(STAT_WIFLY_RX_TASK_ENTER);
        
    /* wait for something to enter the UART0 rcv message queue */
    int QRcvChk = xQueueReceive( wifly_rx_queue, &wiflyRcvByteBuffer, portMAX_DELAY );
        
    /* if we have a good message queue receive */
    if ( QRcvChk == pdTRUE ) {
        
        /* set GPIO status to a good read */
        sendGPIOStatus(STAT_WIFLY_RX_GOOD);

        /* check byte by byte in serial fsm for complete frame */
        runSerialFrame( wiflyRcvByteBuffer );

    }

}
