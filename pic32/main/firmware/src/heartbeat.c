


#include "heartbeat.h"
#include "serialfsm.h"

#define HEARTBEAT_DELAY 250
#define HEARTBEAT_MSG_HEADER 'H'
#define HEARTBEAT_MSG_NUM_ROLLOVER 128

/* external UART0 transmit queue */
extern QueueHandle_t uart0TransQueue;

int heartbeat_msgcount; // message number
unsigned char heartbeat_msgbuff[SERIAL_DATA_BYTES_PER_MESSAGE + 2]; // message buffer

/* init */
void HEARTBEAT_Initialize( void ) {
    
    /* Set GPIO status to this init task */
    sendGPIOStatus(STAT_TASK_HEARTBEAT_INIT);
    
    /* Set up the timer */
    
    /* set msg count to zero */
    heartbeat_msgcount = 0;
    
    /* initialize the message */
    heartbeat_msgbuff[0] = (unsigned char)SERIAL_START_BYTE;
    heartbeat_msgbuff[SERIAL_DATA_BYTES_PER_MESSAGE + 1] = (unsigned char)SERIAL_END_BYTE;
    heartbeat_msgbuff[1] = HEARTBEAT_MSG_HEADER;
    heartbeat_msgbuff[SERIAL_DATA_BYTES_PER_MESSAGE] = heartbeat_msgcount;
    
    /* init remaining bytes with zero */
    int i = 2;
    for(i; i < SERIAL_DATA_BYTES_PER_MESSAGE - 1; i++)
    {
        heartbeat_msgbuff[i] = 0;
    }
    
    
}

/* main task */
void HEARTBEAT_Tasks( void ) {
    
    /* set GPIO status to this task */
    sendGPIOStatus(STAT_TASK_HEARTBEAT);
    
    /* increment message count byte */
    heartbeat_msgbuff[SERIAL_DATA_BYTES_PER_MESSAGE] = (unsigned char)heartbeat_msgcount;
    
    /* send the message byte by byte to the transmit queue*/
    int i = 0;
    for(i; i < sizeof(heartbeat_msgbuff); i++)
    {
        sendGPIOStatus(STAT_TASK_HEARTBEAT_SEND);
        xQueueSend(uart0TransQueue, &heartbeat_msgbuff[i], 0);
    }
       
    /* increment message count number */
    heartbeat_msgcount++;
    
    /* rollover message count */
    if(heartbeat_msgcount == HEARTBEAT_MSG_NUM_ROLLOVER)
    {
        heartbeat_msgcount = 0;
    }
    
    /* set this task to delay before execuating again */
    vTaskDelay(HEARTBEAT_DELAY);

}



/*******************************************************************************
 End of File
 */
