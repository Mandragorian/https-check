#Https-check

A simple python script to check https support of a site's subdomains.

##Usage

Https-check takes as input a yaml file. This file must define a list of
dictionairies. Each dictionairy has to have a binding for key 'base\_dir'
which must be the base directory of the site you want to check. It must also
have a binding for key 'subdomains' which must be a list of the subdomains
you want to check.

###Example

```yaml
-   base_dir:
      ntua.gr
    subdomains:
      - shmmy
      - ece
      - chemeng
      - users
      - mycourses
      - ftp
      - central
      - softlab
      - semfe
      - physics
      - metal
      - lib
      - itia
      - civil
      - arch
      - mech
      - epu
      - cslab
      - webmail
      - survey
      - login
      - noc
      - my
      - icbnet
      - dbnet
      - math
      - lme
      - foss
      - dblab
      - cn
      - wireless
      - netmode
      - naval
      - microlab
      - map
      - image
      - 11hstam
```
