
#include "tsk_lfa_rx.h"
#include "public_vars.h"
#include "debug.h"

LFA_RX_DATA lfa_rxData;

static int i2cStatus;
uint8_t lfa_rx_i2c_buf;

void IdleI2C1(void) {
    /* Wait until I2C Bus is Inactive */
    while (I2C1CONbits.SEN || I2C1CONbits.PEN || I2C1CONbits.RSEN || I2C1CONbits.RCEN || I2C1CONbits.ACKEN || I2C1STATbits.TRSTAT);
}

void LFA_I2C_ResetRegister() {
    IdleI2C1();

    if (I2CBusIsIdle(I2C1)) {
        i2cStatus = I2CStart(I2C1);
    }

    IdleI2C1();

    i2cStatus = I2CSendByte(I2C1, (0x3E << 1) | I2C_WRITE);

    IdleI2C1();

    if (I2CTransmitterIsReady(I2C1)) {
        i2cStatus = I2CSendByte(I2C1, 0x7D);
        IdleI2C1();
        i2cStatus = I2CSendByte(I2C1, 0x12);
        IdleI2C1();
        I2CStop(I2C1);
    }
}

void LFA_I2C_ResetRegister2() {
    IdleI2C1();

    if (I2CBusIsIdle(I2C1)) {
        i2cStatus = I2CStart(I2C1);
    }

    IdleI2C1();

    i2cStatus = I2CSendByte(I2C1, (0x3E << 1) | I2C_WRITE);

    IdleI2C1();

    if (I2CTransmitterIsReady(I2C1)) {
        i2cStatus = I2CSendByte(I2C1, 0x7D);
        IdleI2C1();
        i2cStatus = I2CSendByte(I2C1, 0x34);
        IdleI2C1();
        I2CStop(I2C1);
    }
}

void LFA_I2C_BankA() {
    IdleI2C1();

    if (I2CBusIsIdle(I2C1)) {
        i2cStatus = I2CStart(I2C1);
    }

    IdleI2C1();

    i2cStatus = I2CSendByte(I2C1, (0x3E << 1) | I2C_WRITE);

    IdleI2C1();

    if (I2CTransmitterIsReady(I2C1)) {
        i2cStatus = I2CSendByte(I2C1, 0x0F);
        IdleI2C1();
        i2cStatus = I2CSendByte(I2C1, 0xFF);
        IdleI2C1();
        I2CStop(I2C1);
    }
}

void LFA_I2C_BankB() {
    IdleI2C1();

    if (I2CBusIsIdle(I2C1)) {
        i2cStatus = I2CStart(I2C1);
    }

    IdleI2C1();

    i2cStatus = I2CSendByte(I2C1, (0x3E << 1) | I2C_WRITE);

    IdleI2C1();

    if (I2CTransmitterIsReady(I2C1)) {
        i2cStatus = I2CSendByte(I2C1, 0x0E);
        IdleI2C1();
        i2cStatus = I2CSendByte(I2C1, 0xFC);
        IdleI2C1();
        I2CStop(I2C1);
    }
}

void LFA_I2C_IRPower() {
    IdleI2C1();

    if (I2CBusIsIdle(I2C1)) {
        i2cStatus = I2CStart(I2C1);
    }

    IdleI2C1();

    i2cStatus = I2CSendByte(I2C1, (0x3E << 1) | I2C_WRITE);

    IdleI2C1();

    if (I2CTransmitterIsReady(I2C1)) {
        i2cStatus = I2CSendByte(I2C1, 0x10);
        IdleI2C1();
        i2cStatus = I2CSendByte(I2C1, 0x00);
        IdleI2C1();
        I2CStop(I2C1);
    }
}

void LFA_I2C_INIT() {

    /* RESET SEQUENCE */

    LFA_I2C_ResetRegister();
    LFA_I2C_ResetRegister2();

    LFA_I2C_BankA();
    LFA_I2C_BankB();
    LFA_I2C_IRPower();

    if (I2C1STATbits.BCL || I2C1STATbits.IWCOL) {
        sendGPIOError(ERR_I2C_BUS_COLLISION);
    }

}

void LFA_I2C_GetByte() {
    IdleI2C1();

    i2cStatus = I2CStart(I2C1);

    IdleI2C1();

    i2cStatus = I2CSendByte(I2C1, (0x3E << 1) | I2C_WRITE);

    IdleI2C1();

    i2cStatus = I2CSendByte(I2C1, 0x11);

    IdleI2C1();

    I2CStop(I2C1);

    IdleI2C1();

    i2cStatus = I2CStart(I2C1);

    IdleI2C1();

    i2cStatus = I2CSendByte(I2C1, (0x3E << 1) | I2C_READ);

    IdleI2C1();

    i2cStatus = I2CReceiverEnable(I2C1, TRUE);

    IdleI2C1();

    while (!I2CReceivedDataIsAvailable(I2C1));

    if (I2CReceivedDataIsAvailable(I2C1)) {
        I2CAcknowledgeByte(I2C1, pdTRUE);
        lfa_rx_i2c_buf = I2CGetByte(I2C1);
    }

    IdleI2C1();

    I2CStop(I2C1);

}

void LFA_RX_Initialize(void) {

    sendGPIOStatus(STAT_LFA_RX_INIT);

    I2CConfigure(I2C1, 0);
    I2CSetFrequency(I2C1, SYS_CLK_BUS_PERIPHERAL_1, 100ul);
    I2CSetSlaveAddress(I2C1, 0x05, 0, I2C_USE_7BIT_ADDRESS);
    I2CEnable(I2C1, pdTRUE);

    LFA_I2C_INIT();
}

int lfaStatEchoTime = 0;

void LFA_RX_Tasks(void) {
    sendGPIOStatus(STAT_LFA_TASK_ENTER);

    LFA_I2C_GetByte();

    if (I2C1STATbits.BCL || I2C1STATbits.IWCOL) {
        sendGPIOError(ERR_I2C_BUS_COLLISION);
    }

    int qsendStat = xQueueSend(lfa_rx_queue, &lfa_rx_i2c_buf, 0);

    if (qsendStat != pdTRUE) {
        //sendGPIOError(ERR_BAD_MQ_SEND);
    }

    sendLFAStatus(lfa_rx_i2c_buf);
    
    if(lfaStatEchoTime > 350) {
        /* echo back LFA data */
        char lfaStat[5] = "LFA";
        lfaStat[3] = (char)lfa_rx_i2c_buf;
        lfaStat[4] = MSG_END_CHAR;
        xQueueSend(debug_queue, lfaStat, 0);
        lfaStatEchoTime = 0;
    }
    
    vTaskDelay(50);
    lfaStatEchoTime += 50;

}



/*******************************************************************************
 End of File
 */
