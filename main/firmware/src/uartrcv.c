
/* This task simply initializes the UART0 receive message queue,
 *  it does not do anything otherwise, currently */

#include "uartrcv.h"
#define UART0_RCV_QUEUE_SIZE 10

/* define UART0 rcv message queue */
QueueHandle_t uart0RcvQueue;

/* init */
void UARTRCV_Initialize ( void )
{
    /* initialized UART0 rcv message queue */
    uart0RcvQueue = xQueueCreate(UART0_RCV_QUEUE_SIZE, sizeof(char));
}

/* main task */
void UARTRCV_Tasks ( void )
{
    /* nothing to do here */
    
}

 

/*******************************************************************************
 End of File
 */
