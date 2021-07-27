build:
	gcc util.c -o libteaiso.so -shared -O3 -s  -fPIC
test:
	gcc util.c test.c -g -Wno-all -o a.out && ./a.out
