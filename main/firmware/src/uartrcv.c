
/* This task simply initializes the UART0 receive message queue,
 *  it does not do anything otherwise, currently */

#include "uartrcv.h"
#include "serialfsm.h"

#define UART0_RCV_QUEUE_SIZE 100

/* define UART0 rcv message queue */
QueueHandle_t uart0RcvQueue;
char rcvTaskByteBuffer;

/* serial state setup*/
extern SERIAL_DATA serialData;
        
/* init */
void UARTRCV_Initialize ( void )
{
    /* initialized UART0 rcv message queue */
    uart0RcvQueue = xQueueCreate(UART0_RCV_QUEUE_SIZE, sizeof(char));
    serialData.state = WAITING_START;
    
}

/* main task */
void UARTRCV_Tasks ( void )
{
    /* wait for something to enter the UART0 rcv message queue */
        int QRcvChk = xQueueReceive(uart0RcvQueue, &rcvTaskByteBuffer, portMAX_DELAY);

        /* if we have a good message queue receive */
        if (QRcvChk == pdTRUE) {

            /**/
            runSerialFrame(rcvTaskByteBuffer);
            
        }
    
}

 

/*******************************************************************************
 End of File
 */
