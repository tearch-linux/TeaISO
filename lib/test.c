#include <stdio.h>
char* get_argument_value(char* arg, char* val);
int main(){
  /*Test some stuff*/
  warn("this is warning","x");
  out("this is output");
  err("this is error","y");
  disable_color();
  err("this is error (nocolor)","z");
  run("cat /etc/os-release | grep ^NAME=");
}
