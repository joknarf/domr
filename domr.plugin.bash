__domr="$(cd "${BASH_SOURCE%/*}"; pwd)/domr.py"
type python3 >/dev/null 2>&1 && alias domr="python3 $__domr" || alias domr="$__domr"
unset __domr