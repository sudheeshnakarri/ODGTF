#!/bin/bash
# ODG QA Test Suite

clean_stdin()
{
    while read -e -t 1; do : ; done
}

menu()
{
    echo -e >&2 "\n\t\t\t\tODG QA TestSuite!\n"
    echo -e >&2 "Select Test Catagory:"
    echo -e >&2 "\t\t1 -- User Commands "
    echo -e >&2 "\t\t2 -- Scripts -TODO"
    echo -e >&2 "\t\t3 -- Apks-TODO"
    echo -e >&2 "\t\t0 -- Exit"

    clean_stdin
    read -p "Enter your choice :" chc
    echo "$chc"

}


clear
choice=true
while $choice; do
    clear
    yn=$( menu )
    case $yn in
        "1" ) echo "User Command Tests Selected";  python ./jsonparsor.py;;
        "2" ) echo -e >&2 "\n Development in Progress.Come back Later ! \n";;
        "3" ) echo -e >&2 "\n Development in Progress.Come back Later ! \n";;
        "0" ) exit;;
        * ) echo "Please enter 0 to 3 as choice";;
    esac

    clean_stdin
    read -p "Do you wish to continue ODG Test Suite(Yes- 1 , No -0)" chc
    if [ $chc  -eq "1" ]; then
         choice=true
    else
         choice=false
    fi  
done
