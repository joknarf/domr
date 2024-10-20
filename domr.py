#!/usr/bin/env python
# coding: utf-8
# pylint: disable=E1101,R1732,C0301,C0302,W0603
"""
    domr.py resolve from short hostname/ip
    Author: Franck Jouvanceau
"""
import os
import sys
from socket import gethostbyname_ex, gethostbyaddr, inet_aton, inet_ntoa, error
from argparse import ArgumentParser, RawTextHelpFormatter

DNS_DOMAINS = os.environ.get("DOMR_DOMAINS") or ""

def parse_args():
    """argument parse"""
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    parser = ArgumentParser(
        description="domr v1.0", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument("-f", "--hostsfile", help="hosts list file")
    parser.add_argument("-H", "--hosts", help="hosts list", nargs="+")
    parser.add_argument("-i", "--getips", action="store_true", help="display resolved ips")
    parser.add_argument("-I", "--getip", action="store_true", help="display first resolved ip")
    parser.add_argument("-a", "--all", action="store_true", help="display short/name resolved/fqdn/aliases/ips")
    return parser.parse_args()


def resolve_hostname(host):
    """try get fqdn from DNS"""
    try:
        res = gethostbyname_ex(host)
    except OSError:
        return None
    except UnicodeError:
        print("Warning: domr: invalid hostname/domain: " + host)
        return None
    return res


def resolve_in_domains(host, domains):
    """try get fqdn from short hostname in domains"""
    resolved = resolve_hostname(host)
    if resolved:
        return list(resolved) + [host]
    for domain in domains:
        resolved = resolve_hostname(host + "." + domain)
        if resolved:
            return list(resolved) + [host + "." + domain]
    sys.stderr.write("Warning: domr: cannot resolve " + host + "\n")
    return []


def resolve_ip(ip):
    """try resolve hostname by reverse dns query on ip addr"""
    ip = inet_ntoa(inet_aton(ip))
    try:
        return list(gethostbyaddr(ip))+ [ip]
    except (OSError, error):
        sys.stderr.write("Warning: domr: cannot resolve " + ip + "\n")
    return []


def is_ip(host):
    """determine if host is valid ip"""
    try:
        inet_aton(host)
        return True
    except (OSError, error):
        return False


def resolve(host, domains):
    """resolve hostname from ip / hostname"""
    if is_ip(host):
        return resolve_ip(host)
    return resolve_in_domains(host, domains)


def resolve_hosts(hosts, domains):
    """try resolve hosts to get fqdn"""
    return [resolve(host, domains) for host in hosts if host]


def resolve_hosts_disp(hosts, domains, args):
    for host in hosts:
        resolved = resolve(host, domains)
        if not resolved:
            continue
        if args.getips:
            print("\n".join(resolved[2]))
        elif args.getip:
            print(resolved[2][0])
        elif args.all:
            print(host, resolved[3], resolved[0], " ".join(resolved[1]), " ".join(resolved[2]), sep="\t")
        else:
            print(resolved[0])


def get_hosts(hostsfile, hosts):
    """returns hosts list from args host or reading hostsfile"""
    if hosts:
        return hosts
    if not hostsfile:
        sys.stderr.write("ERROR: domr: No hosts definition\n")
        sys.exit(1)
    if hostsfile == "-":
        return list(filter(len, sys.stdin.read().split()))
    try:
        with open(hostsfile, "r", encoding="UTF-8") as fhosts:
            hosts = list(filter(len, fhosts.read().split()))
    except OSError:
        sys.stderr.write("ERROR: domr: Cannot open " + hostsfile + "\n")
        sys.exit(1)
    return hosts


def main():
    """argument read / read hosts file / prepare commands / launch jobs"""
    global MAX_DOTS
    args = parse_args()

    if args.hostsfile:
        hostsfile = os.path.basename(args.hostsfile)
    else:
        hostsfile = "parameter"
    hosts = get_hosts(args.hostsfile, args.hosts)
    resolve_hosts_disp(hosts, DNS_DOMAINS.split(), args)

if __name__ == "__main__":
    main()
