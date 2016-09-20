/* 
 * File:   tmr_callbk.h
 * Author: john
 *
 * Created on September 7, 2016, 7:32 PM
 */

#ifndef TMR_CALLBK_H
#define	TMR_CALLBK_H

#ifdef	__cplusplus
extern "C" {
#endif
    
#include "system_definitions.h"
#include "app_public.h"
#include "debug.h"

/* Application's Timer Callback Function */
void vTimerCallback1(TimerHandle_t xTimer);


#ifdef	__cplusplus
}
#endif

#endif	/* TMR_CALLBK_H */

