
#ifndef DEBUG_H    /* Guard against multiple inclusion */
#define DEBUG_H

#include "system_definitions.h"

#ifdef __cplusplus
extern "C" {
#endif


    // initialize GPIO error port
    void initGPIODebug();
    
    uint8_t getDebugSetting();

    // send error to GPIO
    void sendGPIOError(uint8_t errCode);

    // send status to GPIO
    void sendGPIOStatus(uint8_t stat);

    // lfa status
    void sendLFAStatus(uint8_t lfastat);
    
    // direction status
    void sendDirStatus(uint8_t dir);
    
    // speed status
    void sendSpdStatus(uint8_t spd);
#ifdef __cplusplus
}
#endif

#endif /* _EXAMPLE_FILE_NAME_H */

/* *****************************************************************************
 End of File
 */
