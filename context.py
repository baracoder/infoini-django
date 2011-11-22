from status import ist_offen

def glob(request):
    return {'ist_offen':ist_offen()}
