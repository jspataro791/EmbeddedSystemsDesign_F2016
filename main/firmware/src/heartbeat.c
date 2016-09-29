


#include "heartbeat.h"
#include "serialfsm.h"

#define HEARTBEAT_DELAY 250
#define HEATBEAT_MSG_HEADER 'H'

extern QueueHandle_t uart0TransQueue;

int heartbeat_msgcount;
unsigned char heartbeat_msgbuff[SERIAL_DATA_BYTES_PER_MESSAGE + 2];

/* init */
void HEARTBEAT_Initialize( void ) {
    
    sendGPIOStatus(STAT_TASK_HEARTBEAT_INIT);
    
    heartbeat_msgcount = 0;
    
    heartbeat_msgbuff[0] = (unsigned char)SERIAL_START_BYTE;
    heartbeat_msgbuff[SERIAL_DATA_BYTES_PER_MESSAGE + 1] = (unsigned char)SERIAL_END_BYTE;
    heartbeat_msgbuff[1] = HEATBEAT_MSG_HEADER;
    heartbeat_msgbuff[SERIAL_DATA_BYTES_PER_MESSAGE] = heartbeat_msgcount;
    
    int i = 2;
    for(i; i < SERIAL_DATA_BYTES_PER_MESSAGE - 1; i++)
    {
        heartbeat_msgbuff[i] = 0;
    }
    
    
}

/* main task */
void HEARTBEAT_Tasks( void ) {
    
    sendGPIOStatus(STAT_TASK_HEARTBEAT);
    
    heartbeat_msgbuff[SERIAL_DATA_BYTES_PER_MESSAGE] = (unsigned char)heartbeat_msgcount;
    
    int i = 0;
    for(i; i < sizeof(heartbeat_msgbuff); i++)
    {
        xQueueSend(uart0TransQueue, &heartbeat_msgbuff[i], 0);
    }
       
    heartbeat_msgcount++;
    
    if(heartbeat_msgcount == 128)
    {
        heartbeat_msgcount = 0;
    }
    
    vTaskDelay(HEARTBEAT_DELAY);

}



/*******************************************************************************
 End of File
 */
