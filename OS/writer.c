#include <stdio.h> 
#include <sys/ipc.h> 
#include <sys/msg.h> 
  
struct mesg_buffer { 
    long mesg_type; 
    char mesg_text[100]; 
} message; 
  
int main() 
{ 
    char c[100];
    int line_count = 0;
    FILE *fptr;
    FILE *resf;
    key_t key; 
    int msgid;
    char* rmv_end = "=";

    key = ftok("progfile", 65);
    msgid = msgget(key, 0666 | IPC_CREAT); 
    message.mesg_type = 1; 

    if ((fptr = fopen("calculating.txt", "r")) == NULL) {
        printf("Error opening target file");
        return 0;
    }

    if ((resf = fopen("result.txt", "w")) == NULL) {
        printf("Error opening destination file");
        return 0;
    }

    while (fgets(c, 10, fptr))
    {
        for (int i=0; i<10; i++) {
            if (c[i] != '\n')
                message.mesg_text[i] = c[i];
            else
                break;
        }

        msgsnd(msgid, &message, sizeof(message), 0);
        printf("Data send is : %s \n", message.mesg_text);
        fputs(message.mesg_text, resf);
        msgrcv(msgid, &message, sizeof(message), 1, 0);
        printf("Data Received is : %s \n", message.mesg_text);
        fputs("=", resf);
        fputs(message.mesg_text, resf);
        fputs("\n", resf);

        for (int i=0; i<10; i++)
            message.mesg_text[i] = 0;
    }
    fclose(fptr);
    return 0; 
} 