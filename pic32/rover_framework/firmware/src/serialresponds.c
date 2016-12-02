#include "serialresponds.h"
#include "system_definitions.h"
#include "queue.h"
#include "public_vars.h"

char s0RespBuffer[MAX_QUEUE_ITEM_SIZE];

void serial0Respond(char * resp) {
    strcpy(s0RespBuffer, resp);
    xQueueSend(wifly_tx_queue, s0RespBuffer, 0);

}

