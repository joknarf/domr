__domr="$(cd "${.sh.file%/*}";pwd)/domr.py"
type python3 >/dev/null 2>&1 && alias domr="python3 $__domr" || alias domr="$__domr"
unset __domr
