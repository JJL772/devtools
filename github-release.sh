#!/bin/bash

# Extremely simple upload script for github releases

if [ -z $GITHUB_TOKEN ]; then
        GITHUB_TOKEN="$(cat /srv/github-token)"
fi

[ -z $GITHUB_TOKEN ] && echo "GITHUB_TOKEN envvar is not set." && exit 1

PRERELEASE="false";

for arg in $@; do
        case $arg in
                --token=*)
                        GITHUB_TOKEN=$(echo $arg | sed "s/--token=//g")
                        shift;
                        ;;
                --branch=*)
                        BRANCH=$(echo $arg | sed "s/--branch=//g")
                        shift;
                        ;;
                --name=*)
                        NAME=$(echo $arg | sed "s/--name=//g")
                        shift;
                        ;;
                --relnotes=*)
                        RELNOTES=$(echo $arg | sed "s/--relnotes=//g")
                        shift;
                        ;;
                --username=*)
                        USERNAME=$(echo $arg | sed "s/--username=//g")
                        shift;
                        ;;
                --repo=*)
                        REPO=$(echo $arg | sed "s/--repo=//g")
                        shift;
                        ;;
                --prerelease)
                        PRERELEASE="true";
                        shift;
                        ;;
                --artifact=*)
                        ARTIFACT="$ARTIFACT $(echo $arg | sed "s/--artifact=//g")"
                        shift;
                        ;;
                --tag=*)
                        TAG=$(echo $arg | sed "s/--tag=//g")
                        shift
                        ;;
                --help|-h)
                        echo "USAGE: github-upload.sh --branch=* --name=* --relnotes=* --username=* --repo=* --artifact=*"
                        exit 0
                        ;;
                *)
                        echo "Unknown arg '$arg'" && exit 1
                        ;;
        esac
done 

[ -z $REPO ] && echo "--repo is not specified" && exit 1
[ -z $USERNAME ] && echo "--username is not specified" && exit 1
[ -z $BRANCH ] && BRANCH=master
[ -z $RELNOTES ] && RELNOTES="Autobuild"
[ -z $TAG ] && echo "Invalid tag" && exit 1

echo "Creating release..."

RELEASE=$(curl -XPOST -H "Authorization:token $GITHUB_TOKEN" --data "{ \"tag_name\": \"$TAG\", \"target_commitish\": \"$BRANCH\", \"name\": \"$NAME\", \"body\": \"$RELNOTES\", \"draft\": false, \"prerelease\": $PRERELEASE}" https://api.github.com/repos/$USERNAME/$REPO/releases)

echo "Get release ID..."

ID=$(echo "$RELEASE" | sed -n -e 's/"id":\ \([0-9]\+\),/\1/p' | head -n 1 | sed 's/[[:blank:]]//g')

echo "Uploading artifacts." 

for art in $ARTIFACT; do
        echo "Uploading $art" 
        curl -XPOST -H "Authorization:token $GITHUB_TOKEN" -H "Content-Type:application/octet-stream" --data-binary @$art https://uploads.github.com/repos/$USERNAME/$REPO/releases/$ID/assets?name=$art > /dev/null 
done 
