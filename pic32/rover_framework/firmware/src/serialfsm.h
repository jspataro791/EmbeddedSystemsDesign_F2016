

#ifndef SERIALFSM_H    /* Guard against multiple inclusion */
#define SERIALFSM_H

#include "system_definitions.h"
#include "list.h"

#ifdef __cplusplus
extern "C" {
#endif

	typedef enum {
		WAITING_START1, WAITING_START2, WAITING_START3, WAITING_DATA_LENGTH, WAITING_DATA, WAITING_END1, WAITING_END2
	} state_type;

	typedef struct {
		state_type state;

		uint8_t dataBytesPerMsg;

		unsigned char dataBytesReceived;

		unsigned char temporaryBytes[MAX_QUEUE_ITEM_SIZE];


	} SERIAL_DATA;


	SERIAL_DATA serialData;


	void runSerialFrame(unsigned char c);

#ifdef __cplusplus
}
#endif

#endif /* _EXAMPLE_FILE_NAME_H */

/* *****************************************************************************
 End of File
 */
