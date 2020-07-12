from django.contrib import admin
from myproject.bill.models import *

admin.site.register([tblexpenses, tblbill,tbladditionalbill,postedbill,oldbill,billsession])
