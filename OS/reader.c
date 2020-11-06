#include <stdio.h> 
#include <math.h>
#include <sys/ipc.h> 
#include <sys/msg.h> 
  
struct mesg_buffer { 
    long mesg_type; 
    char mesg_text[100]; 
} message; 

float get_result(char* mess, int mess_len) {
    float num1 = 0;
    float num2 = 0;
    int idx = 0;
    int status = 0;
    int operation = -1;
    while (idx < mess_len) {
        char cidx = mess[idx];
        if (status == 0 || status == 2) {
            if (cidx >= '0' && cidx <= '9') {
                float temp;
                if (status == 0) {
                    temp = num1;
                } else {
                    temp = num2;
                }
                temp *= 10;
                temp += cidx - '0';

                if (status == 0) {
                    num1 = temp;
                } else {
                    num2 = temp;
                }
            } else {
                status += 1;
                idx -= 1;
            }
        } else if (status == 1) {
            switch (cidx) {
                case '+':
                    operation = 0;
                    break;
                case '-':
                    operation = 1;
                    break;
                case '*':
                    operation = 2;
                    break;
                case '/':
                    operation = 3;
                    break;
            }
            status += 1;
        } else if (status == 3) {
            // printf("%d", operation);
            switch (operation) {
                case 0:
                    return num1 + num2;
                case 1:
                    return num1 - num2;
                case 2:
                    return num1 * num2;
                case 3:
                    return num1 / num2;
            }
        } else {
            return 0;
        }

        idx += 1;
    }
}
  
void reverse(char* str, int len) 
{ 
    int i = 0, j = len - 1, temp; 
    while (i < j) { 
        temp = str[i]; 
        str[i] = str[j]; 
        str[j] = temp; 
        i++; 
        j--; 
    } 
}

int intToStr(int x, char str[], int d) 
{ 
    int i = 0; 
    while (x) { 
        str[i++] = (x % 10) + '0'; 
        x = x / 10; 
    } 

    while (i < d) 
        str[i++] = '0'; 
  
    reverse(str, i); 
    str[i] = '\0'; 
    return i; 
} 

void ftoa(float n, char* res, int afterpoint) 
{ 
    int ipart = (int)n; 
    float fpart = n - (float)ipart; 
    int i = intToStr(ipart, res, 0); 
    // if (afterpoint != 0) { 
    //     res[i] = '.';
    //     fpart = fpart * pow(10, afterpoint); 
    //     intToStr((int)fpart, res + i + 1, afterpoint); 
    // } 
} 

int main() 
{ 
    key_t key; 
    int msgid; 
    key = ftok("progfile", 65); 

    msgid = msgget(key, 0666 | IPC_CREAT); 
  
    while (1) {
        msgrcv(msgid, &message, sizeof(message), 1, 0); 
    
        printf("Data Received is : %s \n", message.mesg_text);
        float result = get_result(message.mesg_text, sizeof(message));
        printf("Result is: %f \n", result);
        char response[10];
        ftoa(result, response, 3);
        for (int i=0; i<sizeof(message.mesg_text); i++) {
            message.mesg_text[i] = 0;
        }
        for (int i=0; i<10; i++) {
            message.mesg_text[i] = response[i];
        }
        msgsnd(msgid, &message, sizeof(message), 0); 
    }
    
    msgctl(msgid, IPC_RMID, NULL); 
  
    return 0; 
}

