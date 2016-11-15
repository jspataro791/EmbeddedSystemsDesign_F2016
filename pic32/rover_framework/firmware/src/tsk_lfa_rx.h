

#ifndef _LFA_RX_H
#define _LFA_RX_H


#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include "system_config.h"
#include "system_definitions.h"

// DOM-IGNORE-BEGIN
#ifdef __cplusplus  // Provide C++ Compatibility

extern "C" {

#endif

typedef enum
{
	/* Application's state machine's initial state. */
	LFA_RX_STATE_INIT=0,
	LFA_RX_STATE_SERVICE_TASKS,

	/* TODO: Define states used by the application state machine. */

} LFA_RX_STATES;



typedef struct
{
    /* The application's current state */
    LFA_RX_STATES state;

    /* TODO: Define any additional data used by the application. */

} LFA_RX_DATA;

void LFA_RX_Initialize ( void );

void LFA_RX_Tasks( void );


#endif /* _LFA_RX_H */

//DOM-IGNORE-BEGIN
#ifdef __cplusplus
}
#endif
//DOM-IGNORE-END

/*******************************************************************************
 End of File
 */

