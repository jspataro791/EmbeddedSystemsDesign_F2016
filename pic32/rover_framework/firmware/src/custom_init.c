#include "custom_init.h"
#include "debug.h"
#include "FreeRTOS.h"
#include "semphr.h"

void initPublicQueues()
{
    wifly_rx_queue = xQueueCreate(MAX_QUEUE_LENGTH, sizeof(char));
    wifly_tx_queue = xQueueCreate(MAX_QUEUE_LENGTH, MAX_QUEUE_ITEM_SIZE);
    lfa_rx_queue   = xQueueCreate(MAX_QUEUE_LENGTH, sizeof(char));
    valid_data_queue = xQueueCreate(MAX_QUEUE_LENGTH, MAX_QUEUE_ITEM_SIZE);
    debug_queue = xQueueCreate(MAX_QUEUE_LENGTH, MAX_QUEUE_ITEM_SIZE);
    motor_ctrl_queue = xQueueCreate(MAX_QUEUE_LENGTH, sizeof(char));
    
    if(wifly_rx_queue == NULL || wifly_rx_queue == NULL || lfa_rx_queue == NULL || valid_data_queue == NULL || debug_queue == NULL
       || motor_ctrl_queue == NULL) 
    {
        /* send critical error */
        sendGPIOError(ERR_BAD_MQ_CREATE);
    }
    
}

void initRvrStatus()
{
    RVR_CurDirection = RVR_STRAIGHT; // straight
    RVR_CurSpeed = 16; // max speed
    
    sendDirStatus((uint8_t)RVR_CurDirection);
    sendSpdStatus((uint8_t)RVR_CurSpeed);
}

void initMutexes()
{
    UART_TX_Mutex = xSemaphoreCreateMutex();
    
    if(UART_TX_Mutex == NULL)
    {
        /* do some critical error here */
    }
}