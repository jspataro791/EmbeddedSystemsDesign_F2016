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
    
    if(wifly_rx_queue == NULL || wifly_rx_queue == NULL || lfa_rx_queue == NULL || valid_data_queue == NULL || debug_queue == NULL) 
    {
        /* send critical error */
        sendGPIOError(ERR_BAD_MQ_CREATE);
    }
    
}

void initRvrStatus()
{
    RVR_CurDirection = RVR_STRAIGHT; // straight
    RVR_CurSpeed = 16; // max speed
}

void initMutexes()
{
    uartTxMutexHandle = xSemaphoreCreateMutex();
    
    if(uartTxMutexHandle == NULL)
    {
        /* do some critical error here */
    }
}