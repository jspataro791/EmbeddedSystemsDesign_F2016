#include "custom_init.h"
#include "debug.h"

void initPublicQueues()
{
    wifly_rx_queue = xQueueCreate(MAX_QUEUE_LENGTH, sizeof(char));
    wifly_tx_queue = xQueueCreate(MAX_QUEUE_LENGTH, MAX_QUEUE_ITEM_SIZE);
    lfa_rx_queue   = xQueueCreate(MAX_QUEUE_LENGTH, sizeof(char));
    valid_data_queue = xQueueCreate(MAX_QUEUE_LENGTH, MAX_QUEUE_ITEM_SIZE);
    
    if(wifly_rx_queue == NULL || wifly_rx_queue == NULL || lfa_rx_queue == NULL) 
    {
        sendGPIOError(ERR_BAD_MQ_CREATE);
    }
    
}

void initRvrStatus()
{
    RVR_CurDirection = 0; // straight
    RVR_CurSpeed = 16; // max speed
}