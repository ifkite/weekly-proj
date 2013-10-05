#include <stdio.h>
#define PHY_CLCLE 23
#define EMO_CLCLE 28
#define INT_CLCLE 33
int main(){
    int phy_start, emo_start, int_start, day_start, iter, day_past, cmpIntEmo, cmpIntPhy;
    int gapEmoInt = emo_start - int_start;
    int gapPhyInt = phy_start - int_start; 
    while(scanf("%d %d %d %d", &phy_start, &emo_start, &int_start, &day_start)){
        if(phy_start == -1)
            break;
        for(day_past = INT_CLCLE; day_past <= PHY_CLCLE * EMO_CLCLE * INT_CLCLE; day_past += INT_CLCLE){
           cmpIntEmo = day_past  + gapEmoInt;
           if(!(cmpIntEmo % EMO_CLCLE)){
               cmpIntPhy = day_past  + gapPhyInt;
               if(!(cmpIntPhy % PHY_CLCLE)){
                   printf("%d\n", day_past - int_start - day_start);
                   break;
               }
           }
        }
    }
    return 0;
}
