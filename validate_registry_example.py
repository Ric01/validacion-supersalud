import hcpregistry as hcp

hcp = hcp.HcpRegistry(rut="22603251", nombre="Prueba")


hcp.check_registry()

print(hcp.nombre)
print(hcp.rut)
print(hcp.especialidad)
print(hcp.valid_registry)
