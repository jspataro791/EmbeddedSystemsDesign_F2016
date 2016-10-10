

#ifndef SERIALRESPONDS_H    /* Guard against multiple inclusion */
#define SERIALRESPONDS_H

#ifdef __cplusplus
extern "C" {
#endif

#define SERIAL_RESP_NACK "NN"
#define SERIAL_RESP_ACK "ACK"

    /* sound out response on UART0 */
    void serial0Respond(char * resp);


#ifdef __cplusplus
}
#endif

#endif /* _EXAMPLE_FILE_NAME_H */

/* *****************************************************************************
 End of File
 */
