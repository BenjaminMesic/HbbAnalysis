#include <math.h>
double scale_factor_tau21_pt( double pt_t)
{
    return 1.03*log(pt_t/200);
}