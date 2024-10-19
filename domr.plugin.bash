type python >/dev/null 2>&1 && alias domr="${BASH_SOURCE%.plugin.bash}.py" && return
type python3 >/dev/null 2>&1 && alias domr="python3 ${BASH_SOURCE%.plugin.bash}.py"
