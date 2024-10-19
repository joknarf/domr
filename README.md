# domr
DNS resolve from short hostname against multiple domains to get fqdn  
Retrieve fqdn from ip (if reverse DNS avail for ip)

## usage

```
# export DOMR_DOMAINS='domain1.myorg domain2.myorg'
# domr -H myshorthost1 myshorthost2
myshorthost1.domain1.myorg
myshorthost2.domain2.myorg

# domr -H 192.168.1.10 192.168.2.10
myshorthost1.domain1.myorg
myshorthost2.domain2.myorg
```

