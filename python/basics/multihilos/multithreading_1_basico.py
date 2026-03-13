import threading
import time

def hacer_cafe():
    print("Empezando a hacer cafe...")
    time.sleep(3)
    print("Cafe listo!")

def tostar_pan():
    print("Poniendo el pan en la tostadora...")
    time.sleep(2)
    print("Pan tostado listo!")

def hervir_agua():
    print("Poniendo agua a hervir...")
    time.sleep(4)
    print("Agua hirviendo lista!")


print("SIN multithreading (todo en orden):")
inicio = time.time()

hacer_cafe()
tostar_pan()
hervir_agua()

fin = time.time()
print(f"Tiempo total: {fin - inicio:.1f} segundos\n")

print("CON multithreading (todo junto):")
inicio = time.time()

hilo1 = threading.Thread(target=hacer_cafe)
hilo2 = threading.Thread(target=tostar_pan)
hilo3 = threading.Thread(target=hervir_agua)

hilo1.start()
hilo2.start()
hilo3.start()

hilo1.join()
hilo2.join()
hilo3.join()

fin = time.time()
print(f"Tiempo total: {fin - inicio:.1f} segundos")
print("\nCon multithreading todo corrió al mismo tiempo!")
