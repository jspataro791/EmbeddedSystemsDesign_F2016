/* 
 * File:   app_public.h
 * Author: john
 *
 * Created on September 6, 2016, 4:10 PM
 */

#ifndef APP_PUBLIC_H
#define	APP_PUBLIC_H

#include "FreeRTOS.h"
#include "queue.h"
#include "system_definitions.h"

#ifdef	__cplusplus
extern "C" {
#endif

    // TIMER Defines
#define QLENGTH 50
    
    // USART Defines
    
/*#define USART_BAUD 300
#define USART_FLAGS DRV_USART_INIT_FLAG_NONE
#define USART_HANDSHAKE DRV_USART_HANDSHAKE_NONE
#define USART_INTERROR INT_SOURCE_USART_2_ERROR
#define USART_INTRECV INT_SOURCE_USART_2_RECEIVE
#define USART_INTTRANS INT_SOURCE_USART_2_TRANSMIT
#define USART_LINECONTROL DRV_USART_LINE_CONTROL_8NONE1
#define USART_MODE DRV_USART_OPERATION_MODE_NORMAL
#define USART_BRGCLOCK 80000000
#define USART_MODULE_VALUE SYS_MODULE_POWER_RUN_FULL
#define USART_QUEUESIZERX 2
#define USART_QUEUESIZETX 3
#define USART_ID USART_ID_2*/

    // TIMER QUEUE STUFF

    // Inits the queue for this timing system
    QueueHandle_t appInitTimerMQ();

    // Sends current time to queue
    int appSendTimerValToMQ(QueueHandle_t q, unsigned int milliElapsed);
    
    // USART STUFF
    
    // usart initialization
    //DRV_HANDLE usartInit();
    
    
    

#ifdef	__cplusplus
}
#endif

#endif	/* APP_PUBLIC_H */

