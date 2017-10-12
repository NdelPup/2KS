#!/bin/bash
#
#script che legge i qr code attraverso zbarcam e ne passa l'output al server dei tornelli
#attraverso un socket tcp in localhost
#

zbarcam --raw --nodisplay | xargs -L1 >/dev/tcp/localhost/55555