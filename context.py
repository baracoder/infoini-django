from status import get_all

def glob(request):
    ist_offen = get_all()['tuer_offen']
    return {'ist_offen':ist_offen}
