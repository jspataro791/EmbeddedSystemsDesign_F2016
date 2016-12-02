#ifndef _WIFLY_RX_H
#define _WIFLY_RX_H

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include "system_config.h"
#include "system_definitions.h"
#include "public_vars.h"

// DOM-IGNORE-BEGIN
#ifdef __cplusplus  // Provide C++ Compatibility
extern "C" {
#endif

	typedef enum {
		/* Application's state machine's initial state. */
		WIFLY_RX_STATE_INIT = 0,
		WIFLY_RX_STATE_SERVICE_TASKS,

		/* TODO: Define states used by the application state machine. */

	} WIFLY_RX_STATES;

	typedef struct {
		/* The application's current state */
		WIFLY_RX_STATES state;

		/* TODO: Define any additional data used by the application. */

	} WIFLY_RX_DATA;


	void WIFLY_RX_Initialize(void);

	void WIFLY_RX_Tasks(void);


#endif


#ifdef __cplusplus
}
#endif

