#ifdef TWITCH_DATA
#define TWITCH_DATA
#define FOLLOW 0
#define BITS 1

struct twitch_webhook;
struct twitch_api;

union twitch_request {
    struct twitch_webhook webhook;
    struct twitch_api api;
}

struct twitch_webhook {
    unsigned long request_id;
    int request;
    unsigned long username_length;
    char twitch_user[];
}

typedef union twitch_request twitch_message;
#endif
