#include "debug.h"

void initGPIODebug() {
    PLIB_PORTS_DirectionOutputSet(PORTS_ID_0, ERR_GPIO_PORT, 0x00FF);

    PLIB_PORTS_DirectionInputSet(PORTS_ID_0, LFA_GPIO_PORT, LFA_GPIO_PIN_0);
    PLIB_PORTS_DirectionInputSet(PORTS_ID_0, LFA_GPIO_PORT, LFA_GPIO_PIN_1);
}

uint8_t getDebugSetting() {
    uint8_t high = PLIB_PORTS_PinGet(PORTS_ID_0, LFA_GPIO_PORT, LFA_GPIO_PIN_0) << 1;
    uint8_t low = PLIB_PORTS_PinGet(PORTS_ID_0, LFA_GPIO_PORT, LFA_GPIO_PIN_1);

    return (uint8_t) (low | high);
}

void sendGPIOError(uint8_t errCode) {

    PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, 0x00);
    PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, errCode);

    if (errCode != ERR_GOOD) {

        vTaskSuspendAll();
        while (1) {

            PLIB_PORTS_Toggle(PORTS_ID_0, ERR_GPIO_PORT, errCode);

            int x = 0;
            while (x < 1000000) {
                Nop();
                x++;
            }
        }
    }
}

void sendGPIOStatus(uint8_t stat) {
    if (getDebugSetting() == 0x03) {
        PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, 0x00);
        PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, stat);
    }
}

void sendLFAStatus(uint8_t lfastat) {
    if (getDebugSetting() == 0x00) {
        PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, 0x00);
        PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, lfastat);
    }
}

void sendDirStatus(uint8_t dir) {
    if (getDebugSetting() == 0x02) {
        PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, 0x00);
        PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, dir);
    }
}

void sendSpdStatus(uint8_t spd) {
    if (getDebugSetting() == 0x01) {
        PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, 0x00);
        PLIB_PORTS_Write(PORTS_ID_0, ERR_GPIO_PORT, spd);
    }
}

void DEBUG_Puts(char* dbgMsg) {
    if (RVR_Dbg) {
        memset(DbgBuffer, 0, sizeof (DbgBuffer));
        strcpy(DbgBuffer, dbgMsg);
        xQueueSend(debug_queue, DbgBuffer, 0);
    }
}