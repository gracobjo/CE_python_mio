notas = {"Ana": 2,"Luis": 4,"Marta": 5,"Pedro": 7,"Laura": 8,"Carlos": 9,"Sofía": 10}
for nombre, nota in notas.items():
   print(f"{nombre}: {nota} - " f"{'Suspenso' if nota < 5 else 'Aprobado' if nota < 7 else 'Notable' if nota < 9 else 'Sobresaliente'}")