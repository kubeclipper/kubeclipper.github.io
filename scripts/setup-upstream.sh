#!/bin/sh

git remote add upstream https://github.com/yunionio/docs.git

git checkout --track upstream/release/3.8
git checkout --track upstream/release/3.7
git checkout --track upstream/release/3.6
git checkout --track upstream/release/3.4
git checkout --track upstream/release/3.3
git checkout --track upstream/release/3.2
