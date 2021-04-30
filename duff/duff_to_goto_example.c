// apparently duff machines can get through clightgen

void send(int count)
{
    int n=(count+1)/2;
    switch(count%2){
    case 0: 
lol:
    case 1:     ;
         if(--n>0) goto lol;
        //}while(--n>0);
    }
}

int main () {return 0;}
