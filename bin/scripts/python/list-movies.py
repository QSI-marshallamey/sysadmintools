#!/usr/bin/env python3

import os
for root, dir, files in os.walk( "/Users/mjadmin/pCloud Drive/Media/Movies" ) :  
        files.sort()
        for filename in files:
          
            print( f"{filename}" )
