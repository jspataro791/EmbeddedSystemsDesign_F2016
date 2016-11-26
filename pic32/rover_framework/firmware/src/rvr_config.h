/* 
 * File:   rvr_config.h
 * Author: john
 *
 * Created on November 15, 2016, 9:39 AM
 */

#ifndef RVR_CONFIG_H
#define	RVR_CONFIG_H

/* rover configuration stuff */
#define RVR_TYPE 0 // 0 for pacman, 1 for ghost

/* rover direction defs */
#define RVR_STRAIGHT 0
#define RVR_LEFT     1
#define RVR_RIGHT    2

/* serial comm stuff */
#define RVR_MSG_END_BYTE 0x7C
#define SERIAL_START_BYTE 254
#define SERIAL_END_BYTE 255
#define SERIAL_DATA_BYTES_PER_MESSAGE 4
#define SERIAL_RESP_NACK "NN"
#define SERIAL_RESP_ACK "ACK"

/* queue stuff */
#define MAX_QUEUE_ITEM_SIZE  32
#define MAX_QUEUE_LENGTH  64

//* MOTOR CONTROL STUFF *//

/* enable = chipkit pin 46, pic32 RF1*/
/* route to motor shield pin 3*/
#define MOTOR_ENABLE_PORT PORT_CHANNEL_F
#define MOTOR_ENABLE_PIN   PORTS_BIT_POS_1

/* motor1 dir = chipkit pin 47, pic32 RD6*/
/* route to motor shield pin 4 */
#define MOTOR1_DIR_PORT PORT_CHANNEL_D
#define MOTOR1_DIR_PIN PORTS_BIT_POS_6

/* motor2 dir = chipkit pin 48, pic32 RD8*/
/* route to motor shield pin 34 */
#define MOTOR2_DIR_PORT PORT_CHANNEL_D
#define MOTOR2_DIR_PIN PORTS_BIT_POS_8

//* DEBUG STUFF *//


    // GPIO PORT AND PIN
/* err = chipkit pins 30 through 37 */
#define ERR_GPIO_PORT PORT_CHANNEL_E

#define LFA_GPIO_PORT PORT_CHANNEL_C
#define LFA_GPIO_PIN_0  PORTS_BIT_POS_2
#define LFA_GPIO_PIN_1  PORTS_BIT_POS_3

    // GPIO ERROR DEFINES
#define ERR_GOOD                0xFE
#define ERR_GENERIC_BAD         0xFF
#define ERR_BAD_MQ_RECV         0x01
#define ERR_BAD_MQ_SEND         0x02
#define ERR_BAD_MQ_CREATE       0x03
#define ERR_BAD_TIMER_INIT      0x04
#define ERR_BAD_TASK_STATE      0x05
#define ERR_I2C_BUS_COLLISION   0xF0

    // GPIO STATUS DEFINES

#define STAT_SYS_INIT               0x06
#define STAT_SYS_TASK_CREATE        0x07

#define STAT_WIFLY_RX_INIT          0x08
#define STAT_WIFLY_RX_TASK_ENTER    0x09
#define STAT_WIFLY_RX_GOOD          0x0A
    
#define STAT_SERIAL_ACK             0x0B
#define STAT_SERIAL_NACK            0x0C
    
#define STAT_WIFLY_TX_INIT          0x0D
#define STAT_WIFLY_TX_TASK_ENTER    0x0E
#define STAT_WIFLY_TX_GOOD          0x0F
    
#define STAT_RVRSTATUS_INIT         0x10
#define STAT_RVRSTATUS_TASK_ENTER   0x11

#define STAT_DEBUG_INIT             0x12
#define STAT_DEBUG_TASK_ENTER       0x13

#define STAT_LFA_RX_INIT            0x14
#define STAT_LFA_TASK_ENTER         0x15


#endif	/* RVR_CONFIG_H */

