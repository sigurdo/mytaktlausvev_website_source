#!/usr/bin/fish
cd (pwd)/(dirname (status --current-filename))/../ # Set working directory to project root

argparse --name=migrate.fish 'h/help' 'squash' 'no-make' 'no-migrate' -- $argv

if test $status != 0
    set _flag_help "--help"
end

if test "$_flag_help" != ""
    echo "Make migrations and migrate"
    echo "Options:"
    echo "--help       - Print this message"
    echo "--squash     - Squash unstaged migrations"
    echo "--no-make    - Do not run makemigrations"
    echo "--no-migrate - Do not run migrate"
    exit 0
end

docker-compose down

if test "$_flag_squash" = "--squash"
    echo "squash"

    set git_status (string split " " (git status -s -- site/**/migrations/*.py))

    set index 1
    while true
        if test $index -gt (count $git_status)
            break
        end

        set offset 1
        while test $git_status[(math $index + $offset)] = ""
            set offset (math $offset + 1)
        end

        if test $git_status[$index] = "??"
            set unstaged $git_status[(math $index + $offset)]
            echo "Squashing unstaged migration:" $unstaged
            rm $unstaged
        end
        set index (math $index + $offset + 1)
    end
end

if not test "$_flag_no_make" = "--no-make"
    echo "make"
    sh scripts/run.sh python site/manage.py makemigrations
end

if not test "$_flag_no_migrate" = "--no-migrate"
    echo "migrate"
    sh scripts/run.sh python site/manage.py migrate
end
