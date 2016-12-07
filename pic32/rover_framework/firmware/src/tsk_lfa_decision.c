
#include "tsk_lfa_decision.h"
#include "public_vars.h"
#include "rvr_config.h"


LFA_DECISION_DATA lfaDecData;
uint8_t lfa;

void
LFA_DECISION_Initialize() {
    lfaDecData.decState = STRAIGHT;
}

uint8_t lfaDecBuffer;

uint8_t
lfa_recv() {
    int QRcvChk = xQueueReceive(lfa_rx_queue, &lfaDecBuffer, portMAX_DELAY);

    if (QRcvChk == pdTRUE) {

        return lfaDecBuffer;

    } else {
        sendGPIOError(ERR_BAD_MQ_RECV);
    }
}

void
mtr_send(char motorctrl) {
    int sendGood = xQueueSend(motor_ctrl_queue, &motorctrl, 0);

    if (sendGood == pdTRUE) {
        return;
    } else {
        sendGPIOError(ERR_BAD_MQ_SEND);
    }

}

uint8_t leftTurnAvailable = pdFALSE;
uint8_t rightTurnAvailable = pdFALSE;
uint8_t straightAvailable = pdFALSE;

int time = 0;

void
LFA_DECISION_Tasks() {
    switch (lfaDecData.decState) {

        case STRAIGHT:

            lfa = lfa_recv();

            if (RVR_CurSpeed == 0) {
                mtr_send(MOTOR_CTRL_STOP);
                lfaDecData.decState = STRAIGHT;
                break;
            }

            if (lfa & 0b10000001) {
                lfaDecData.decState = TWOWAY_TURN;
            } else if ((lfa & 0b11000000) && !(lfa & 0b00000011)) {
                lfaDecData.decState = LEFT_TURN;
            } else if ((lfa & 0b00000011) && !(lfa & 0b11000000)) {
                lfaDecData.decState = RIGHT_TURN;
            } else if (lfa == LFA_LEFTISH) {
                mtr_send(MOTOR_CTRL_RIGHT);
            } else if (lfa == LFA_RIGHTISH) {
                mtr_send(MOTOR_CTRL_LEFT);
            } else if (lfa == LFA_NONE) {
                lfaDecData.decState = RIGHT_TURN;
            } else {
                mtr_send(MOTOR_CTRL_STRAIGHT);
            }
            break;

        case LEFT_TURN:

            leftTurnAvailable = pdTRUE;
            rightTurnAvailable = pdFALSE;

            lfaDecData.decState = TURN_STAGING;
            mtr_send(MOTOR_CTRL_STRAIGHT);

            time = 0;

            /* WHAT THE FUCK IS THIS?! */
            while (time < 1000) {
                lfa_recv();
                time += 50;
            }

            break;

        case RIGHT_TURN:

            leftTurnAvailable = pdFALSE;
            rightTurnAvailable = pdTRUE;

            lfaDecData.decState = TURN_STAGING;
            mtr_send(MOTOR_CTRL_STRAIGHT);

            time = 0;

            /* WHAT THE FUCK IS THIS?! */
            while (time < 1000) {
                lfa_recv();
                time += 50;
            }

            break;


        case TWOWAY_TURN:

            leftTurnAvailable = pdTRUE;
            rightTurnAvailable = pdTRUE;

            lfaDecData.decState = TURN_STAGING;
            mtr_send(MOTOR_CTRL_STRAIGHT);

            time = 0;

            /* WHAT THE FUCK IS THIS?! */
            while (time < 1000) {
                lfa_recv();
                time += 50;
            }

            break;

        case TURN_STAGING:

            mtr_send(MOTOR_CTRL_STOP);

            lfa = lfa_recv();

            if (lfa & 0b00111100) {
                straightAvailable = pdTRUE;
            } else if (lfa == 0b00000000) {
                straightAvailable = pdFALSE;
            }


            lfaDecData.decState = TURN_EXECUTE;
            break;

        case TURN_EXECUTE:

            if (RVR_CurDirection == RVR_LEFT && leftTurnAvailable == pdTRUE) {
                mtr_send(MOTOR_CTRL_LEFT);
                lfaDecData.decState = TURN_FINISH_LEFT;
            } else if (RVR_CurDirection == RVR_RIGHT && rightTurnAvailable == pdTRUE) {
                mtr_send(MOTOR_CTRL_RIGHT);
                lfaDecData.decState = TURN_FINISH_RIGHT;
            } else if (straightAvailable == pdTRUE) {
                mtr_send(MOTOR_CTRL_STRAIGHT);
                lfaDecData.decState = STRAIGHT;
            } else {

                if (leftTurnAvailable == pdTRUE) {
                    mtr_send(MOTOR_CTRL_LEFT);
                    lfaDecData.decState = TURN_FINISH_LEFT;
                } else if (rightTurnAvailable == pdTRUE) {
                    mtr_send(MOTOR_CTRL_RIGHT);
                    lfaDecData.decState = TURN_FINISH_RIGHT;
                } else {

                }

            }
            break;

        case TURN_FINISH_LEFT:

            lfa = lfa_recv();

            if (lfa & (uint8_t) 0b1000000) {
                lfaDecData.decState = TURN_STRAIGHTEN;
            }

            break;

        case TURN_FINISH_RIGHT:
            lfa = lfa_recv();

            if (lfa & (uint8_t) 0b00000001) {
                lfaDecData.decState = TURN_STRAIGHTEN;
            }

            break;

        case TURN_STRAIGHTEN:

            lfa = lfa_recv();

            if (lfa & (uint8_t) 0b00011000) {
                lfaDecData.decState = STRAIGHT;
                leftTurnAvailable = pdFALSE;
                rightTurnAvailable = pdFALSE;
                straightAvailable = pdFALSE;

                time = 0;
                while (time < ((-188 * (RVR_CurSpeed + 1)) + 3196)) {
                    lfa_recv();
                    time += 50;
                }


            }
            break;

    }


}
