
#define DUFF_DEVICE_8(aCount, aAction)  \
    do {\
        int count_ = (aCount);\
        int times_ = (count_ + 7) >> 3;\
    switch (count_ & 7){\
    case 0: do { aAction;\
    case 7:      aAction;\
    case 6:      aAction;\
    case 5:      aAction;\
    case 4:      aAction;\
    case 3:      aAction;\
    case 2:      aAction;\
    case 1:      aAction;\
        } while (--times_ > 0);\
    }\
} while (0)

int main ()
{
    DUFF_DEVICE_8(2, 1);

    return 0;
}
