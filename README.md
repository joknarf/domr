[![Python versions](https://img.shields.io/badge/python-2.7+%20|%203.x-blue.svg)](https://shields.io/)

# domr
DNS resolve from short hostname against multiple domains to get fqdn (extend limited search in resolv.conf)  
returns first fqdn resolved among list of DNS domains  
Retrieve fqdn from ip (if reverse DNS avail for ip)  
*python2/3 compatible*

## usage

```
# export DOMR_DOMAINS='domain1.myorg domain2.myorg'
# domr -H myshorthost1 myshorthost2
myshorthost1.domain1.myorg
myshorthost2.domain2.myorg

# domr -H myshorthost1 myshorthost2 --getips
192.168.1.10
192.168.2.10

# domr -H 192.168.1.10 192.168.2.10
myshorthost1.domain1.myorg
myshorthost2.domain2.myorg

```
domr first try to resolve using local dns search domains, then using DOMR_DOMAINS.

