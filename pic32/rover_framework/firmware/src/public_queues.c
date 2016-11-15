#include <public_queues.h>

wifly_rx_queue = xQueueCreate(MAX_QUEUE_LENGTH, MAX_QUEUE_ITEM_SIZE);
wifly_tx_queue = xQueueCreate(MAX_QUEUE_LENGTH, MAX_QUEUE_ITEM_SIZE);
lfa_rx_queue = xQueueCreate(MAX_QUEUE_LENGTH, MAX_QUEUE_ITEM_SIZE);
