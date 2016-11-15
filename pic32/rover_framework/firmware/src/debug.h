
#ifndef DEBUG_H    /* Guard against multiple inclusion */
#define DEBUG_H

#include "system_definitions.h"

#ifdef __cplusplus
extern "C" {
#endif


    // initialize GPIO error port
    void initGPIODebug();

    // send error to GPIO
    void sendGPIOError(uint8_t errCode);

    // send status to GPIO
    void sendGPIOStatus(uint8_t stat);

    // toggle LED

#ifdef __cplusplus
}
#endif

#endif /* _EXAMPLE_FILE_NAME_H */

/* *****************************************************************************
 End of File
 */
