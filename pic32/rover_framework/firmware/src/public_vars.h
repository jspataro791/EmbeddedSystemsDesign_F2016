
/* This file contains all public variables used across tasks */

#ifndef _PUBLIC_VARS_H    
#define _PUBLIC_VARS_H

#include "FreeRTOS.h"
#include "queue.h"

/* DEFINES */
#define MAX_QUEUE_ITEM_SIZE  32
#define MAX_QUEUE_LENGTH  64

/* PUBLIC QUEUES */
QueueHandle_t wifly_rx_queue;
QueueHandle_t wifly_tx_queue;
QueueHandle_t lfa_rx_queue;
QueueHandle_t valid_data_queue;

/* STATUS */
uint8_t RVR_CurDirection;
uint8_t RVR_CurSpeed;



#endif

