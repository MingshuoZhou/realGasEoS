import CoolProp.CoolProp as CP
print(CP.PropsSI("V", "T", 400, "P", 10^7, "C12"))
print(CP.PropsSI("Z", "T", 400, "P", 10^7, "C12"))
print(CP.PropsSI("V", "T", 400, "P", 10^7, "C12")*10**7)
print(CP.PropsSI("Z", "T", 400, "P", 10^7, "C12")*298*400*CP.PropsSI("D", "T", 400, "P", 10^7, "C12"))