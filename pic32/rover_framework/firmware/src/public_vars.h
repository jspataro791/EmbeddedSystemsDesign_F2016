
/* This file contains all public variables used across tasks */

#ifndef _PUBLIC_VARS_H    
#define _PUBLIC_VARS_H

#include "FreeRTOS.h"
#include "queue.h"
#include "semphr.h"
#include "system_definitions.h"


/* PUBLIC QUEUES */
QueueHandle_t wifly_rx_queue; // receive queue (byte by byte over wifly)
QueueHandle_t wifly_tx_queue; // transmit queue (string)
QueueHandle_t lfa_rx_queue; // receive queue (byte by byte from lfa)
QueueHandle_t valid_data_queue; // verified data from wifly
QueueHandle_t debug_queue; // strings to be sent back to the server as debug
QueueHandle_t motor_ctrl_queue; // L,R,S,B (Left, Right, Straight, Back/Reverse)

/* STATUS */
uint8_t RVR_CurDirection;
uint8_t RVR_CurSpeed;
uint8_t RVR_Dbg;
uint8_t RVR_LFA;

/* UART TX MUTEX */
SemaphoreHandle_t UART_TX_Mutex; // this mutex makes sure that multiple tasks can't
// write strings to the UART transmit at the same time.



#endif

