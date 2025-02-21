# Translations

A repository for all the translation strings for our various projects.

## How to contribute

It's verry simple

1. Create a fork of this repository (top right of the github page)

2. Clone your fork and push your modifications (Codespaces are great if you don't have git installed)

3. Create a pull request to this repository (the forked repository should prompt you to "contribute" on the github page)

4. A member of our development team will accapt or deny your pull request and may ask for changes if required

Some basic rules to follow to get a request approved:
- All translation languages must start as a copy of the `./en` folder so that the unfinished translations will default to english
- Folders must be named based on the S&amp;Box [Documentation](https://sbox.game/dev/doc/ui/localization/)
- There must not be any new string added unless you have spoken to a member of the development team.

Tips: Run `python validate.py` to check for our missing languages and for any errors you may have that will not get your pull request approved.
