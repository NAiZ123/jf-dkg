# jf-dkg
 
jf-dkg is joint-feldman dkg test code.
This program doesn't actually exchange shares with each other and haven't verified the RE phase.
In practice, the feldman VSS process is done in parallel under thr production environment.

# DEMO
 
See this paper
* https://link.springer.com/content/pdf/10.1007/3-540-46416-6_47.pdf
* https://www.researchgate.net/publication/227327292_Secure_Distributed_Key_Generation_for_Discrete-Log_Based_Cryptosystems

# Features
This is for the simplest of experiments joint-feldman dkg code.
p : 1024bit
q : 160 bit

I'm not refactoring. So There is a lot of waste.

# Requirement
 
* import random
* import math
* import time
* import sympy
* from random import randrange
* from hashlib import sha1
* from gmpy2
 
# Installation

please insttall lib (gmpy2,hashlib,sympy)
(mac os)
```bash
brew install gmp
brew install mpfr
brew install libmpc
pip install gmpy2
```
 
# Usage
 
```bash
git clone https://github.com/jf-dkg
cd jf-dkg
python joint-feldman_dkg.py
k = 3
n = 5
.
.
.

pre-share and commitment
id 0
.
.
.
id n

Feldman VSS(pre-share Verify)
id 0
.
.
.
id n

dkg share x : [ id , dkg-share ]
dkg public y : y

elpased_time : 

public commitment :

Combining shares :
# select shares #

Secret recovered from minimum subset of shares:  
Secret recovered a different minimum subset of shares: 

```
 
# Note

Please tell me about my mistakes.
I'm so sorry, The reply is slow.
 
# Author
 
* NAiZ
* I'm a college student.
* twitter  https://twitter.com/WanaNaoki
 
# License
 
"jf-dkg" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
