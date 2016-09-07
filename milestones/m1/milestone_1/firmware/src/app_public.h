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

#ifdef	__cplusplus
extern "C" {
#endif

#define QLENGTH 50

    // Inits the queue for this timing system
    QueueHandle_t appInitTimerMQ();

    // Sends current time to queue
    int appSendTimerValToMQ(QueueHandle_t q, unsigned int milliElapsed); 
    

#ifdef	__cplusplus
}
#endif

#endif	/* APP_PUBLIC_H */

