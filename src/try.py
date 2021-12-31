import CoolProp.CoolProp as CP
CP.apply_simple_mixing_rule('decane', 'CYCLOHEX', 'linear')
CP.apply_simple_mixing_rule('decane', 'toluene', 'linear')
CP.apply_simple_mixing_rule('CYCLOHEX', 'toluene', 'linear')
print(CP.PropsSI("D", "T", 400, "P", 6000000, 'decane[0.78]&CYCLOHEX[0.098]&toluene[0.122]'))
print(0.78*CP.PropsSI("D", "T", 400, "P", 6000000, 'decane')+0.098*CP.PropsSI("D", "T", 400, "P", 6000000, 'CYCLOHEX')+0.122*CP.PropsSI("D", "T", 400, "P", 6000000, 'toluene'))
# print(CP.PropsSI("V", "T", 400, "P", 10^7, "C12"))

# print(CP.PropsSI("Z", "T", 400, "P", 10^7, "C12"))
# print(CP.PropsSI("V", "T", 400, "P", 10^7, "C12")*10**7)
# print(CP.PropsSI("Z", "T", 400, "P", 10^7, "C12")*298*400*CP.PropsSI("D", "T", 400, "P", 10^7, "C12"))