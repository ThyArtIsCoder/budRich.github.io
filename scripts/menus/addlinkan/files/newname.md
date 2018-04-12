#!/bin/bash

NAME="addlink"
VERSION="0.007"
AUTHOR="budRich"
CONTACT='robstenklippa@gmail.com'
CREATED="2017-12-04"
UPDATED="2018-02-25"

ADD_LINK_FILE="${ADD_LINK_FILE:-$HOME/dox/not/links.note}"
FLD_BAN="/tmp/catbans"

genbans(){
  OFS=${IFS} # save original Field Separor
  LFS=$'\n'  # Separate on lines

  mkdir -p "$FLD_BAN"
  for c in "${lstcats[@]}"; do
    IFS=${LFS}
    banner=($(toilet "${FIG_OPT[@]}" "$c"))
    for l in "${banner[@]}"; do
      [[ $l = "" ]] && continue
      echo "#  $l" >> "${FLD_BAN}/$c"
    done
    IFS=${OFS}
  done
}

main(){
  while getopts :f:vh option; do
    case "${option}" in
      f) FIG_OPT=('-f' ${OPTARG});;
      v) printf '%s\n' \
           "$NAME - version: $VERSION" \
           "updated: $UPDATED by $AUTHOR"
         exit ;;
      h|*) printinfo && exit ;;
    esac
  done

  if [[ ! $1 =~ ^http  ]]; then
    url=$(xclip -o)
    [[ ! $url =~ ^http  ]] && url=""
  else
    url="$1"
  fi

  url=$(rofi -dmenu -filter "$url" -p 'addlink: ')
  [[ ! $url =~ ^http  ]] && exit

  lstcats=($(awk '$1!~"#" && $0!="" && $1!=oca {oca=$1;print $1}' "$ADD_LINK_FILE" | sort -u))
  cat=$(printf '%s\n' "${lstcats[@]}" | rofi -dmenu -p 'category: ')
  [[ -z $cat ]] && exit
  [[ ! $cat =~ ${lstcats[*]} ]] && lstcats+=("$cat")

  genbans &

  ali=$(rofi -dmenu -p 'alias: ')
  [[ -z $ali ]] && exit

  toadd="$cat $ali 1 $url"

  for c in "${lstcats[@]}"; do
    cat "${FLD_BAN}/$c" >> /tmp/tmplnks
    echo >> /tmp/tmplnks
    [[ $cat = "$c" ]] && echo "${toadd}" >> /tmp/tmplnks
    awk -v cat="$c" '$1==cat{print $0}' "$ADD_LINK_FILE" \
      | sort -u >> /tmp/tmplnks
    echo >> /tmp/tmplnks
  done

  echo -e "\n# syntax:ssHash" >> /tmp/tmplnks

  mv -f /tmp/tmplnks "$ADD_LINK_FILE"
  rm -rf "${FLD_BAN}"
}

printinfo(){
  case "$1" in
    m ) printf '%s' "${about}" ;;
    
    f ) 
      printf '%s' "${bouthead}"
      printf '%s' "${about}"
      printf '%s' "${boutfoot}"
    ;;

    ''|* ) 
      printf '%s' "${about}" | awk '
         BEGIN{ind=0}
         $0~/^```/{
           if(ind!="1"){ind="1"}
           else{ind="0"}
           print ""
         }
         $0!~/^```/{
           gsub("[`*]","",$0)
           if(ind=="1"){$0="   " $0}
           print $0
         }
       '
    ;;
  esac
}

bouthead="
${NAME^^} 1 ${CREATED} Linux \"User Manuals\"
=======================================

NAME
----
"

boutfoot="
AUTHOR
------

${AUTHOR} <${CONTACT}>
<https://budrich.github.io>

SEE ALSO
--------

rofi(1), toilet(6)
"

about='
`addlink` - Adds a URL to a file

SYNOPSIS
--------

`SCRIPTNAME` [`-v`|`-h`] [`-f` *figlet-font*] [*URL*]

DESCRIPTION
-----------

`addlink` adds a *URL* to *FLD_LNKS*. If *URL* is not given
selection and clipboard will be searched for *URL*.
User can also modify the *URL* before adding it.
An alias and category is required.

OPTIONS
-------

`-v`
  Show version and exit.

`-h`
  Show help and exit.

`-f` *figlet-font*
  Figlet font to use


FILES
-----
*ADD_LINK_FILE*
  File to store URL'"'"'s in, defualts to: `~/dox/not/links.note`

*FLD_BAN*
  Temporary folder to store temp files in. 
  *FLD_BAN* will be removed when `addlink` exits.

DEPENDENCIES
------------

rofi
toilet
'

if [ "$1" = "md" ]; then
  printinfo m
  exit
elif [ "$1" = "man" ]; then
  printinfo f
  exit
else
  main "${@}"
fi

