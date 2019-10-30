import ldap
from ldap.controls import SimplePagedResultsControl, LDAPControl
import sys
import ldap.modlist as modlist

LDAP_SERVER = "ldaps://dc.host.com"
BIND_DN = "Operator@host.com"
BIND_PASS = "password"
USER_FILTER = "(&(objectClass=person)(primaryGroupID=7235))"
USER_BASE = "ou=Special Peeps,ou=My Users,dc=host,dc=com"
PAGE_SIZE = 10

# LDAP connection
try:
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
    ldap_connection = ldap.initialize(LDAP_SERVER)
    ldap_connection.simple_bind_s(BIND_DN, BIND_PASS)
except ldap.LDAPError as e:
    sys.stderr.write('Error connecting to LDAP server: ' + str(e) + '\n')
    sys.exit(1)

# Lookup usernames from LDAP via paged search

control = LDAPControl()
paged_results_control = SimplePagedResultsControl(
    ldap.LDAP, True, (PAGE_SIZE, ''))
accounts = []
pages = 0
while True:
    serverctrls = [paged_results_control]
    try:
        msgid = ldap_connection.search_ext(USER_BASE,
                                           ldap.SCOPE_ONELEVEL,
                                           USER_FILTER,
                                           attrlist=['employeeID',
                                                     'sAMAccountName'],
                                           serverctrls=serverctrls)
    except ldap.LDAPError as e:
        sys.stderr.write('Error performing user paged search: ' +
                         str(e) + '\n')
        sys.exit(1)
    try:
        unused_code, results, unused_msgid, serverctrls = \
            ldap_connection.result3(msgid)
    except ldap.LDAPError as e:
        sys.stderr.write('Error getting user paged search results: ' +
                         str(e) + '\n')
        sys.exit(1)
    for result in results:
        pages += 1
        accounts.append(result)
    cookie = None
    for serverctrl in serverctrls:
        if serverctrl.controlType == ldap.LDAP_CONTROL_PAGE_OID:
            unused_est, cookie = serverctrl.controlValue
            if cookie:
                paged_results_control.controlValue = (PAGE_SIZE, cookie)
            break
    if not cookie:
        break

# LDAP unbind
ldap_connection.unbind_s()

# Make dictionary with user data
user_map = {}
for entry in accounts:
    if 'employeeID' in entry[1] and \
            'sAMAccountName' in entry[1]:
        user_map[entry[1]['employeeID'][0]] = entry[1]['sAMAccountName'][0]
'--- test_login.py\t(original)'

'+++ test_login.py\t(refactored)'
'@@ -1,13 +1,14 @@'
'+from __future__ import absolute_import'
' import ldap'
' from ldap.controls import SimplePagedResultsControl'
' import sys'
' import ldap.modlist as modlist'
' '
'-LDAP_SERVER = "ldaps://dc.host.com"'
'-BIND_DN = "Operator@host.com"'
'-BIND_PASS = "password"'
'-USER_FILTER = "(&(objectClass=person)(primaryGroupID=7235))"'
'-USER_BASE = "ou=Special Peeps,ou=My Users,dc=host,dc=com"'
'+LDAP_SERVER = u"ldaps://dc.host.com"'
'+BIND_DN = u"Operator@host.com"'
'+BIND_PASS = u"password"'
'+USER_FILTER = u"(&(objectClass=person)(primaryGroupID=7235))"'
'+USER_BASE = u"ou=Special Peeps,ou=My Users,dc=host,dc=com"'
' PAGE_SIZE = 10'
' '
' # LDAP connection'
'@@ -16,12 +17,12 @@'
'     ldap_connection = ldap.initialize(LDAP_SERVER)'
'     ldap_connection.simple_bind_s(BIND_DN, BIND_PASS)'
' except ldap.LDAPError, e:'
"-    sys.stderr.write('Error connecting to LDAP server: ' + str(e) + '\\n')"
"+    sys.stderr.write(u'Error connecting to LDAP server: ' + unicode(e) + u'\\n')"
'     sys.exit(1)'
' '
' # Lookup usernames from LDAP via paged search'
' paged_results_control = SimplePagedResultsControl('
"-    ldap.LDAP_CONTROL_PAGE_OID, True, (PAGE_SIZE, ''))"
"+    ldap.LDAP_CONTROL_PAGE_OID, True, (PAGE_SIZE, u''))"
' accounts = []'
' pages = 0'
' while True:'
'@@ -30,19 +31,19 @@'
'         msgid = ldap_connection.search_ext(USER_BASE,'
'                                            ldap.SCOPE_ONELEVEL,'
'                                            USER_FILTER,'
"-                                           attrlist=['employeeID',"
"-                                                     'sAMAccountName'],"
"+                                           attrlist=[u'employeeID',"
"+                                                     u'sAMAccountName'],"
'                                            serverctrls=serverctrls)'
'     except ldap.LDAPError, e:'
"-        sys.stderr.write('Error performing user paged search: ' +"
"-                         str(e) + '\\n')"
"+        sys.stderr.write(u'Error performing user paged search: ' +"
"+                         unicode(e) + u'\\n')"
'         sys.exit(1)'
'     try:'
'         unused_code, results, unused_msgid, serverctrls = \\'
'             ldap_connection.result3(msgid)'
'     except ldap.LDAPError, e:'
"-        sys.stderr.write('Error getting user paged search results: ' +"
"-                         str(e) + '\\n')"
"+        sys.stderr.write(u'Error getting user paged search results: ' +"
"+                         unicode(e) + u'\\n')"
'         sys.exit(1)'
'     for result in results:'
'         pages += 1'
'@@ -63,6 +64,6 @@'
' # Make dictionary with user data'
' user_map = {}'
' for entry in accounts:'
"-    if entry[1].has_key('employeeID') and \\"
"-            entry[1].has_key('sAMAccountName'):"
"-        user_map[entry[1]['employeeID'][0]] = entry[1]['sAMAccountName'][0]"
"+    if entry[1].has_key(u'employeeID') and \\"
"+            entry[1].has_key(u'sAMAccountName'):"
"+        user_map[entry[1][u'employeeID'][0]] = entry[1][u'sAMAccountName'][0]"
