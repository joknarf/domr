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
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose display (fqdn + line for last output)",
    )
    parser.add_argument("-f", "--hostsfile", help="hosts list file")
    parser.add_argument("-H", "--hosts", help="hosts list", nargs="+")
    return parser.parse_args()


def resolve_hostname(host: str) -> Optional[str]:
    """try get fqdn from DNS"""
    try:
        res = gethostbyname_ex(host)
    except OSError:
        return None
    return res[0]


def resolve_in_domains(host: str, domains: list) -> str:
    """try get fqdn from short hostname in domains"""
    fqdn = resolve_hostname(host)
    if fqdn:
        return fqdn
    for domain in domains:
        fqdn = resolve_hostname(f"{host}.{domain}")
        if fqdn:
            return fqdn
    print(f"Warning: domr: cannot resolve {host}", file=sys.stderr)
    return host


def resolve_ip(ip: str) -> str:
    """try resolve hostname by reverse dns query on ip addr"""
    try:
        host = gethostbyaddr(ip)
    except OSError:
        print(f"Warning: domr: cannot resolve {ip}", file=sys.stderr)
        return ip
    return host[0]


def is_ip(host: str) -> bool:
    """determine if host is valid ip"""
    try:
        inet_aton(host)
        return True
    except OSError:
        return False


def resolve(host: str, domains: list) -> str:
    """resolve hostname from ip / hostname"""
    if is_ip(host):
        return resolve_ip(host)
    return resolve_in_domains(host, domains)


def resolve_hosts(hosts: list, domains: list) -> list:
    """try resolve hosts to get fqdn"""
    return [resolve(host, domains) for host in hosts]


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
    print("\n".join(resolve_hosts(hosts, DNS_DOMAINS.split())))

if __name__ == "__main__":
    main()
