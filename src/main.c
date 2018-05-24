#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include "config.h"
#include "data_structures/twitch.h"
#include "data_structures/ipc.h"

pid_t server_pool[3];

int twitch_webhook(void){
    pid_t process_pid;
    process_pid = fork();
    int pool_count = 0;

    switch(process_pid){
        case -1:
            fprintf(stderr, "Err in fork!\n");
            exit(1);
        case 0:
            break;
        default:
            printf("Child PID: %i\n", process_pid);
            for(pool_count; pool_count < 3; pool_count++){
                if(server_pool[pool_count] == NULL){
                    server_pool[pool_count] = process_pid;
                    break;
                }
            }
            return process_pid;
    }

    while(1){
        printf("Launching Python!\n");
        char *argv[1] = {NULL};
        execvp(TWITCH_WEBHOOK_SCRIPT, argv);
        printf("Relaunching Python!\n");
    }
}

int main(int argc, char *argv[]){
    int id = 0;
    struct twitch_webhook *webmsg;
    twitch_message message;
    FILE *websub_fifo = fopen(FIFO_LOCATION, "r+");
    twitch_webhook();
    while(id == 0){
        id = waitpid(server_pool[0], NULL, WNOHANG);
        /* fread( */
    }
    fclose(websub_fifo);
    return 0;
}
