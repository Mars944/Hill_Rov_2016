

def changeInterval(x, in_min, in_max, out_min, out_max):     # Identical to Arduino map() function
        return int( (x-in_min) * (out_max-out_min) // (in_max-in_min) + out_min )
