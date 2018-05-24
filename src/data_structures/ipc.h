#ifdef TWITCH_PROJECT_IPC
#define TWITCH_PROJECT_IPC
#include "twitch.h"
enum message_type {twitch_webhook, twitch_api};

struct message {
    int id;
    enum message_type message;
    union twitch_message request[]; /* Should ALWAYS be an array of 1. C99 Feature */
}

typedef struct twitch_request twitch_request;
#endif
