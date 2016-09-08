/* 
 * File:   debug.h
 * Author: john
 *
 * Created on September 6, 2016, 5:04 PM
 */

#ifndef DEBUG_H
#define	DEBUG_H

#include "system_definitions.h"


#ifdef	__cplusplus
extern "C" {
#endif

    // LED DEBUG PORT AND PIN
#define DBG_LED_PORT PORT_CHANNEL_A
#define DBG_LED_PIN PORTS_BIT_POS_3
    
    // GPIO ERROR DEFINES
#define ERR_GOOD 0xFF
#define ERR_GENERIC_BAD 0x00
#define ERR_BAD_MQ_RECV 1
#define ERR_BAD_MQ_CREATE 2
#define ERR_BAD_TIMER_INIT 3
  
    // GPIO PORT AND PIN
#define ERR_GPIO_PORT PORT_CHANNEL_E
    
    // initialize GPIO error port
    void initGPIOError();

    // send error to GPIO
    void sendGPIOError(uint8_t errCode);
    

#ifdef	__cplusplus
}
#endif

#endif	/* DEBUG_H */

