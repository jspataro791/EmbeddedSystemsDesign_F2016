
/* This file contains all public variables used across tasks */

#ifndef _PUBLIC_VARS_H    
#define _PUBLIC_VARS_H

#include "FreeRTOS.h"
#include "queue.h"
#include "semphr.h"
#include "system_definitions.h"


/* PUBLIC QUEUES */
QueueHandle_t wifly_rx_queue;
QueueHandle_t wifly_tx_queue;
QueueHandle_t lfa_rx_queue;
QueueHandle_t valid_data_queue;
QueueHandle_t debug_queue;

/* STATUS */
uint8_t RVR_CurDirection;
uint8_t RVR_CurSpeed;

/* UART TX MUTEX */
SemaphoreHandle_t uartTxMutexHandle;



#endif

