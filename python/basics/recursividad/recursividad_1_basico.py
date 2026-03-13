def cuenta_regresiva(numero):
    if numero == 0:
        print("Despegue!")
        return

    print(numero)
    cuenta_regresiva(numero - 1)

print("Cuenta regresiva desde 5:")
cuenta_regresiva(5)
print()

def factorial(n):
    if n <= 1:
        return 1

    return n * factorial(n - 1)

print("Calculando factoriales:")
for i in range(7):
    print(f"  {i}! = {factorial(i)}")

print("\nfactorial(4) = 4 * 3 * 2 * 1 =", factorial(4))
