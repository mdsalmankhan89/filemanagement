from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth


class AutoLogout:

  def __init__(self, get_response):
    print("77777777777777777777777777777777777777")
    self.get_response = get_response

  def __call__(self, request):
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    try:
      if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        auth.logout(request)
        del request.session['last_touch']
        return redirect("/")
    except KeyError:
      pass

    request.session['last_touch'] = datetime.now()
    return self.get_response(request)
  

    