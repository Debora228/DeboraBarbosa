import multiprocessing
import random
import time
import rx
from threading import current_thread
from rx.scheduler import ThreadPoolScheduler
from rx import operators as ops
from rx import create

# calculate cpu count, using which will create a ThreadPoolScheduler
thread_count = multiprocessing.cpu_count()
thread_pool_scheduler = ThreadPoolScheduler(thread_count)
print("Cpu count is : {0}".format(thread_count))

produtos = [
  { 'Tipo': 'presunto', 'Marca' : 'seara', 'Preco': 200},
  { 'Tipo': 'presunto', 'Marca' : 'perdigao', 'Preco': 100},
  { 'Tipo': 'presunto', 'Marca' : 'sadia', 'Preco': 50},
  { 'Tipo': 'carne', 'Marca' : 'friboi', 'Preco': 500},
  { 'Tipo': 'carne', 'Marca' : 'friboi', 'Preco': 10},
  { 'Tipo': 'queijo', 'Marca' : 'mussarela', 'Preco': 200},
  { 'Tipo': 'queijo', 'Marca' : 'perdigao', 'Preco': 90},
  { 'Tipo': 'queijo', 'Marca' : 'sadia', 'Preco': 120},
  { 'Tipo': 'pepino', 'Marca' : 'natural', 'Preco': 120},
  { 'Tipo': 'molho', 'Marca' : 'que bom', 'Preco': 1},
  { 'Tipo': 'molho', 'Marca' : 'quero', 'Preco': 2},
]

def adding_delay(value):
   time.sleep(random.randint(5, 20) * 0.1)
   return value

def formata(produto):
  if (produto['Preco'] <= 0):
      raise Exception('There is error cannot proceed!: {}'.format(produto['Preco'])) 
  else:
    produto = produto["Tipo"] + " " + produto["Marca"] + " - " + str(produto["Preco"])
    return produto

print("Sujestões de pedidos para a pessoa 1")
# Task 1 => não quer presunto
source = rx.from_(produtos)
case1 = source.pipe(
   ops.filter(lambda a:a['Tipo'] != 'presunto' and a['Tipo'] != 'pepino'),
   ops.map(lambda a: formata(a)),
   ops.retry(1),
   ops.map(lambda a: adding_delay(a)),
   ops.subscribe_on(thread_pool_scheduler)
)
case1.subscribe(
   on_next = lambda i: print("Para Pessoa1 - {0}".format(i)),
   on_error = lambda e: print("Error : {0}".format(e)),
   on_completed = lambda: print("Task 1 complete"),
)

# Se uma parar a outra funciona
# Task 2 => é vegetariana então não quer nem presunto nem carne.
print("Sujestões de pedidos para a pessoa 2")
case2 = source.pipe(
  ops.skip_while(lambda a: a['Tipo']== 'carne' or a['Tipo']== 'presunto'),
  ops.map(lambda a: formata(a)),
  ops.retry(1),
  ops.map(lambda a: adding_delay(a)),
  ops.observe_on(thread_pool_scheduler)
)
case2 = case2.subscribe(
   on_next = lambda i: print("Para Pessoa2 - {0}".format(i)),
   on_error = lambda e: print("Error : {0}".format(e)),
   on_completed = lambda: print("Task 2 complete"),
)

input("Press any key to exit\n")