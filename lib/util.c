#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// run command 
int run(char* cmd){
  char* ncmd;
  if (strlen(cmd)<1){
    return 0;
  }if(strstr(cmd,"chroot||")){
      ncmd = malloc(strlen(cmd)*(sizeof(char)+1));
      for(int i=8;i<strlen(cmd);i++){
        ncmd[i-8]=cmd[i];
      }
      ncmd[strlen(cmd)-7]='\0';
  }else{
    ncmd = cmd;
  }
  return system(ncmd);
}
// logging
void err(char* msg){
  fprintf(stderr,"\x1b[31;1m%s\x1b[;0m\n",msg);
}
void inf(char* msg){
  fprintf(stdout,"\x1b[34;1m%s\x1b[;0m\n",msg);
}
void out(char* msg){
  fprintf(stdout,"%s\n",msg);
}
void warn(char* msg){
  fprintf(stderr,"\x1b[32;1m%s\x1b[;0m\n",msg);
}

char* colorize(char* msg, char* num){
    char* ret = malloc(strlen(msg)*(sizeof(char)+13));
    strcpy(ret,"\x1b[");
    strcat(ret,num);
    strcat(ret,"m");
    strcat(ret,msg);
    strcat(ret,"\x1b[;0m");
    return ret;
}
char* get_argument_value(char* arg, char* val){
  char* ret = malloc((strlen(arg)*(sizeof(char)+1)));
    for(int i=0;i<strlen(arg)-strlen(val);i++){
      ret[i] = arg[i+strlen(val)+1];
    }
    ret[strlen(arg)-strlen(val)]='\0';
  return ret;
}/*
int main(){
  out(colorize(colorize("out=aa","32"),"1"));
}*/
