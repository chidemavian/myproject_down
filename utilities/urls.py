from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('myproject.utilities.views',
    # Examples:
    url(r'^$', "allaccount"),
    url(r'^trans/$', "transactionsview"),
    #url(r'^accountsearch/$', "accountajax"),
    #url(r'^accountsearchall/$', "accountajaxall"),
    url(r'^deletetransaction/$', "deletetrans"),#Delete Transaction
    url(r'^removetransaction/$', "deletetransbydate"),#Delete Transaction By Date
    #url(r'^oldtonewaccount/$', "newaccview"),#To Change Old account To new
    #url(r'^updateacc/$', "updateacc"),
    #url(r'^uploadsubgroup/$', "uploadaccsubgrp"),
    #url(r'^uploadchartofaccount/$', "uploadchartofacc"),
    #url(r'^uploadcusinfo/$', "uploadcusinfo"),#upload Customer Information
    #url(r'^uploadaccount/$', "uploadaccounts"),#upload Customer Accoumts
    #url(r'^generatecusinfo/$', "gencusinfo"),#Generate Customer Information
    #url(r'^uploadtransactions/$', "uploadtransaction"),#Upload Transactions
    #url(r'^uploadloankeep/$', "uploadloankeep"),#Upload Loan Keep
    #url(r'^uploadcot/$', "uploadcot"),#Upload Loan Keep
    url(r'^promotion/$', "temppromotion"),#temporary promotion
    url(r'^updateassessment/$', "updateassview"),#update assessment
    url(r'^generatepin/$', "generatepin"),#Generate PIN
    url(r'^preparedb/$', "preparedb"),

)
