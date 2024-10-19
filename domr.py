#!/usr/bin/env python
# coding: utf-8
# pylint: disable=E1101,R1732,C0301,C0302,W0603
"""
    domr.py resolve from short hostname/ip
    Author: Franck Jouvanceau
"""
import os
import sys
from typing import Optional
from socket import gethostbyname_ex, gethostbyaddr, inet_aton
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

DNS_DOMAINS = os.environ.get("DOMR_DOMAINS") or ""

def parse_args() -> Namespace:
    """argument parse"""
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    __version__="0.1"
    parser = ArgumentParser(
        description=f"domr v{__version__}", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument("-f", "--hostsfile", help="hosts list file")
    parser.add_argument("-H", "--hosts", help="hosts list", nargs="+")
    parser.add_argument("-i", "--getips", action="store_true", help="display resolved ip")
    parser.add_argument("-I", "--getip", action="store_true", help="display first resolved ip")
    return parser.parse_args()


def resolve_hostname(host: str) -> Optional[tuple]:
    """try get fqdn from DNS"""
    try:
        res = gethostbyname_ex(host)
    except OSError:
        return None
    except UnicodeError:
        print(f"Warning: domr: invalid hostname/domain: {host}")
        return None
    return res


def resolve_in_domains(host: str, domains: list) -> tuple:
    """try get fqdn from short hostname in domains"""
    resolved = resolve_hostname(host)
    if resolved:
        return resolved
    for domain in domains:
        resolved = resolve_hostname(f"{host}.{domain}")
        if resolved:
            return resolved
    print(f"Warning: domr: cannot resolve {host}", file=sys.stderr)
    return ()


def resolve_ip(ip: str) -> tuple:
    """try resolve hostname by reverse dns query on ip addr"""
    try:
        resolved = gethostbyaddr(ip)
    except OSError:
        print(f"Warning: domr: cannot resolve {ip}", file=sys.stderr)
        return ()
    return resolved


def is_ip(host: str) -> bool:
    """determine if host is valid ip"""
    try:
        inet_aton(host)
        return True
    except OSError:
        return False


def resolve(host: str, domains: list) -> tuple:
    """resolve hostname from ip / hostname"""
    if is_ip(host):
        return resolve_ip(host)
    return resolve_in_domains(host, domains)


def resolve_hosts(hosts: list, domains: list) -> list:
    """try resolve hosts to get fqdn"""
    return [resolve(host, domains) for host in hosts if host]


def resolve_hosts_disp(hosts: list, domains: list, args: Namespace ) -> None:
    for host in hosts:
        resolved = resolve(host, domains)
        if not resolved:
            continue
        if args.getips:
            print("\n".join(resolved[2]))
        elif args.getip:
            print(resolved[2][0])
        else:
            print(resolved[0])


def get_hosts(hostsfile: str, hosts: list) -> list:
    """returns hosts list from args host or reading hostsfile"""
    if hosts:
        return hosts
    if not hostsfile:
        print("ERROR: domr: No hosts definition", file=sys.stderr)
        sys.exit(1)
    try:
        with open(hostsfile, "r", encoding="UTF-8") as fhosts:
            hosts = list(filter(len, fhosts.read().splitlines()))
    except OSError:
        print(f"ERROR: domr: Cannot open {hostsfile}", file=sys.stderr)
        sys.exit(1)
    return hosts


def readfile(file: str) -> Optional[str]:
    """try read from file"""
    try:
        with open(file, "r", encoding="UTF-8") as fd:
            text = fd.read()
    except OSError:
        return None
    return text.strip()


def main() -> None:
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
