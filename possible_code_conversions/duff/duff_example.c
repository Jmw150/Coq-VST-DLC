
#define command() *to = *from++

// a typical duff device
void duff(short *to, short *from, int count)
{
    int n=(count+7)/8;
    switch(count%8){
    case 0: do{ command();
    case 7:     command();
    case 6:     command();
    case 5:     command();
    case 4:     command();
    case 3:     command();
    case 2:     command();
    case 1:     command();
        }while( --n>0);
    }
}

/*
// just crush the loop
void de_duff(short *to, short *from, int count) {
    int n = count;
    do { command(); } while( --n > 0 ); 
}
*/


int main () {return 0;}


