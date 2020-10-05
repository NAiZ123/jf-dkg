# jf-dkg
 
jf-dkg is joint-feldman test code
 
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

share
id 0
.
.
.
id n

commitment
id 0
.
.
.
id n

dkg share x : [ id , dkg-share ]
dkg public y : y

elpased_time : 

public commitment

```
 
# Note

Please tell me about my mistakes.
I'm so sorry, The reply is slow.
 
# Author
 
* NAiZ
* I'm a student
* twitter  https://twitter.com/WanaNaoki
 
# License
 
"jf-dkg" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
