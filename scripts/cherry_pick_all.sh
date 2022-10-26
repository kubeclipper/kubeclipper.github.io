#!/bin/bash

find_git_branch() {
  # Based on: http://stackoverflow.com/a/13003854/170413
  local branch
  if branch=$(git rev-parse --abbrev-ref HEAD 2> /dev/null); then
    if [[ "$branch" == "HEAD" ]]; then
      branch='detached*'
    fi
    echo "$branch"
  else
    echo ""
  fi
}

find_git_dirty() {
  local status=$(git status --porcelain 2> /dev/null | pcregrep -v "^\?\? ")
  if [[ "$status" != "" ]]; then
    echo '*'
  else
    echo ''
  fi
}

DIRTY=$(find_git_dirty)

if [[ "$DIRTY" == "*" ]]; then
    echo "Repository is dirty, quit"
    exit 1
fi

CUR_BRANCH=$(find_git_branch)

if [[ "$CUR_BRANCH" != "master" ]]; then
    echo "Please execute the script on master branch!"
    exit 1
fi

git fetch upstream

for dir in content assets static layouts
do
    rm -fr ".${dir}"
    cp -r "${dir}" ".${dir}"
done

for BR in $(git branch -a | grep 'remotes/upstream/release/' | sort -r )
do
    BR=${BR:8}
    LOCAL_BR=${BR:9}
    echo "Synchronize $BR"
    git branch -D $LOCAL_BR
    git checkout -b $LOCAL_BR $BR

    rsync -a --delete \
        --exclude 'swagger' \
        --exclude 'setup' \
        --exclude 'quickstart' \
        --exclude 'howto' \
        --exclude 'changelog' \
        --exclude 'ui' \
        .content/* \
        content/

    rsync -a --delete .assets/* assets/

    rsync -a --delete .static/* static/

    rsync -a --delete .layouts/* layouts/

    if [[ $(find_git_dirty) == "*" ]]; then
        TS=$(date '+%Y%m%d%H%M')
        BRNAME="fix/${LOCAL_BR}-${TS}"
        git checkout -b "$BRNAME"
        git add content static assets layouts
        git commit -m "Merge common files to $LOCAL_BR"
        echo -n "$LOCAL_BR has a modification, should we do a PR? (y/N)"
        read YES
        if [[ "$YES" == "y" ]]; then
            git push origin HEAD
        fi
        git checkout ${LOCAL_BR}
        git branch -D "$BRNAME"
    fi
done

rm -fr .content .assets .static .layouts

git checkout $CUR_BRANCH
