_VPATH	+=:$(ROOT)/i2c/source

PROCOBJ	+= I2CPrivate.o
PROCOBJ	+= I2CAcknowledgeByte.o
PROCOBJ	+= I2CAcknowledgeHasCompleted.o
PROCOBJ	+= I2CBusIsIdle.o
PROCOBJ	+= I2CByteWasAcknowledged.o
PROCOBJ	+= I2CClearStatus.o
PROCOBJ	+= I2CConfigure.o
PROCOBJ	+= I2CEnable.o
PROCOBJ	+= I2CGetByte.o
PROCOBJ	+= I2CGetStatus.o
PROCOBJ	+= I2CReceivedByteIsAnAddress.o
PROCOBJ	+= I2CReceivedDataIsAvailable.o
PROCOBJ	+= I2CReceiverEnable.o
PROCOBJ	+= I2CRepeatStart.o
PROCOBJ	+= I2CSendByte.o
PROCOBJ	+= I2CSetFrequency.o
PROCOBJ	+= I2CSetSlaveAddress.o
PROCOBJ	+= I2CSlaveClockHold.o
PROCOBJ	+= I2CSlaveClockRelease.o
PROCOBJ	+= I2CSlaveDataReadRequested.o
PROCOBJ	+= I2CStart.o
PROCOBJ	+= I2CStop.o
PROCOBJ	+= I2CTransmissionHasCompleted.o
PROCOBJ	+= I2CTransmitterIsReady.o

