#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include "config.h"
#include "data_structures/twitch.h"

int twitch_webhook(void){
    pid_t process_pid;
    process_pid = fork();
    switch(process_pid){
        case -1: 
            fprintf(stderr, "Err in fork!\n");
            exit(1);
        case 0:
            break;
        default:
            printf("Child PID: %i\n", process_pid);
            wait(NULL);
            return process_pid;
    }
    while(1){
        printf("Launching Python!\n");
        char *argv[1];
        /* argv[0] = TWITCH_WEBHOOK_SCRIPT; */
        argv[0] = "/home/chanku/random_projs/twitch_stuff/src/twitch_api/twitch_callback.py";
        /* execv("/usr/bin/python3", argv); */
        execv("/usr/bin/python3" , argv);
        printf("Relaunching Python!\n");
        break;
    }
}

int main(int argc, char *argv[]){
    twitch_webhook();
    return 0;
}
