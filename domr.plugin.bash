__domr="$(cd "${BASH_SOURCE%/*}"; pwd)/domr.py"
type python >/dev/null 2>&1 && alias domr="$__domr" && return
type python3 >/dev/null 2>&1 && alias domr="python3 $__domr"
unset __domr