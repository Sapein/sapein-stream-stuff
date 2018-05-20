#ifdef TWITCH_DATA
#define TWITCH_DATA
enum request_type {FOLLOW, BITS}

struct twitch_request {
    int id;
    enum request_type request;
    char *user;
    int value; /* Only really used for BITS */
}

typedef struct twitch_request twitch_request;
#endif
